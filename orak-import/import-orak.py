"""
reCarpet — Orak Import Script (Full API)
=========================================
Skapar/uppdaterar Shopify-produkter direkt via API — ingen manuell CSV-uppladdning.
Laddar automatiskt upp bilder, sätter metafält och uppdaterar SparkLayer-prislistorna.

Användning:
    python import-orak.py --delivery leverans-2026-04

    Flaggor:
    --delivery <mapp>   Mapp med Oraks filer (default: sample-delivery)
    --dry-run           Testa utan att skriva till Shopify eller Excel

Krav:
    pip install openpyxl pandas requests python-dotenv

Setup:
    1. Kopiera .env.example → .env och fyll i Shopify-credentials
    2. Lägg Oraks filer i en leveransmapp: stock.xlsx, prices.csv, photos/
    3. Kör skriptet
"""

import os
import re
import sys
import csv
import json
import time
import base64
import argparse
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

load_dotenv()

# ─── Konfiguration ────────────────────────────────────────────────────────────

SHOPIFY_SHOP    = os.getenv("SHOPIFY_SHOP")       # t.ex. recarpet.myshopify.com
SHOPIFY_TOKEN   = os.getenv("SHOPIFY_TOKEN")       # Admin API access token
API_VERSION     = "2024-01"

BASE_DIR        = Path(__file__).parent
SPECS_FILE      = BASE_DIR / "product-specs.xlsx"
OUTPUT_DIR      = BASE_DIR / "output"
SYNC_LOG        = OUTPUT_DIR / "sync-log.json"    # Håller koll på GIZ → Shopify product ID

PRICELISTS_EXCEL = BASE_DIR.parent / "reCarpet-pricelists-master.xlsx"
SPARKLAYER_DIR   = BASE_DIR.parent / "sparklayer-pricelists"

# SparkLayer-priser per kundgrupp (multiplier från Oraks baspris per m²)
# qty_tiers: minimikvantitet för varje prisnivå (i m²)
QTY_TIERS = [1, 5, 10]

MEMBER_MULTIPLIERS       = [1.00, 0.95, 0.90]   # standard, -5%, -10%
ENTREPRENEUR_MULTIPLIERS = [0.90, 0.82, 0.75]   # -10%, -18%, -25%


# ─── Shopify API ──────────────────────────────────────────────────────────────

def shopify_headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }


def shopify_get(endpoint: str, params: dict = None) -> dict:
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.get(url, headers=shopify_headers(), params=params)
    _handle_rate_limit(r)
    r.raise_for_status()
    return r.json()


def shopify_post(endpoint: str, payload: dict) -> dict:
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.post(url, headers=shopify_headers(), json=payload)
    _handle_rate_limit(r)
    r.raise_for_status()
    return r.json()


def shopify_put(endpoint: str, payload: dict) -> dict:
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.put(url, headers=shopify_headers(), json=payload)
    _handle_rate_limit(r)
    r.raise_for_status()
    return r.json()


def _handle_rate_limit(response):
    """Vänta om vi når API-gränsen."""
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 2))
        print(f"    ⏳ Rate limit — väntar {wait}s...")
        time.sleep(wait)
    else:
        # Respektera leaky bucket: sakta ner om vi är nära gränsen
        limit_header = response.headers.get("X-Shopify-Shop-Api-Call-Limit", "")
        if limit_header:
            used, total = map(int, limit_header.split("/"))
            if used / total > 0.8:
                time.sleep(0.5)
        else:
            time.sleep(0.3)  # säker standardfördröjning


def get_existing_products_by_sku() -> dict:
    """Hämta alla befintliga produkter från Shopify, indexerade på variant-SKU."""
    print("  🔍 Hämtar befintliga produkter från Shopify...")
    sku_map = {}
    params = {"limit": 250, "fields": "id,title,variants"}
    while True:
        data = shopify_get("products.json", params)
        for product in data.get("products", []):
            for variant in product.get("variants", []):
                if variant.get("sku"):
                    sku_map[variant["sku"]] = {
                        "product_id":  product["id"],
                        "variant_id":  variant["id"],
                        "inventory_item_id": variant.get("inventory_item_id"),
                    }
        # Pagination
        link = data.get("link", "")
        if 'rel="next"' not in str(link):
            break
        params["page_info"] = re.search(r'page_info=([^&>]+)', link).group(1) if re.search(r'page_info=([^&>]+)', link) else None
        if not params["page_info"]:
            break
    print(f"    {len(sku_map)} befintliga produkter hittades")
    return sku_map


def create_product(product_data: dict) -> dict:
    return shopify_post("products.json", {"product": product_data})["product"]


def update_product(product_id: int, variant_id: int, updates: dict) -> None:
    """Uppdatera lager och pris på befintlig produkt."""
    shopify_put(f"products/{product_id}.json", {
        "product": {
            "id": product_id,
            "variants": [{"id": variant_id, **updates}]
        }
    })


def upload_product_image(product_id: int, image_path: Path, position: int = 1, alt: str = "") -> None:
    """Ladda upp bild direkt till Shopify-produkt via base64."""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    try:
        shopify_post(f"products/{product_id}/images.json", {
            "image": {
                "attachment": encoded,
                "filename": image_path.name,
                "position": position,
                "alt": alt,
            }
        })
    except Exception as e:
        print(f"      ⚠ Bild misslyckades ({image_path.name}): {e}")


def set_product_metafields(product_id: int, metafields: list) -> None:
    """Sätt metafält på en produkt."""
    for mf in metafields:
        try:
            shopify_post(f"products/{product_id}/metafields.json", {"metafield": mf})
        except Exception as e:
            print(f"      ⚠ Metafält {mf['key']} misslyckades: {e}")


# ─── Datainläsning ────────────────────────────────────────────────────────────

def load_stock(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, header=0)
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)

    col_map = {
        # French (Orak legacy)
        "N° DE GIZ":    "giz_id",
        "STOCK M² EBS": "stock_sqm",
        "MARQUE":       "brand",
        "MODELE":       "model",
        "COLORIS":      "colorway",
        "ORIGINE":      "origin",
        "DESCRIPTION":  "description",
        "CODE BARRE":   "barcode",
        # English (new standard)
        "GIZ_ID":       "giz_id",
        "GIZ ID":       "giz_id",
        "STOCK_SQM":    "stock_sqm",
        "STOCK SQM":    "stock_sqm",
        "BRAND":        "brand",
        "MODEL":        "model",
        "COLORWAY":     "colorway",
        "ORIGIN":       "origin",
        "BARCODE":      "barcode",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    df["brand"]    = df["brand"].astype(str).str.strip().str.upper()
    df["model"]    = df["model"].astype(str).str.strip().str.upper()
    df["colorway"] = df["colorway"].astype(str).str.strip()
    df["giz_id"]   = df["giz_id"].astype(str).str.strip()

    df = df[df["giz_id"].notna() & (df["giz_id"] != "nan")]
    df = df[df["brand"].notna() & (df["brand"] != "NAN")]

    def extract_format(desc):
        if pd.isna(desc): return ""
        m = re.search(r"(\d+[xX×]\d+\s*cm)", str(desc), re.IGNORECASE)
        return m.group(1).replace("X","×").replace("x","×") if m else ""

    df["format"] = df["description"].apply(extract_format)
    return df


def load_prices(path: Path) -> dict:
    prices = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            giz   = str(row.get("giz_id", "")).strip()
            price = str(row.get("price_per_sqm", "")).strip().replace(",", ".")
            if giz and price:
                try: prices[giz] = float(price)
                except ValueError: pass
    return prices


def load_specs(path: Path) -> dict:
    df = pd.read_excel(path, sheet_name="Specs", header=3, skiprows=[4])
    df.columns = [str(c).strip() for c in df.columns]
    spec_cols = ["thickness","fire_rating","acoustic_rating","impact_absorption",
                 "lrv","backing","ecodesigned","min_order_sqm","delivery_days","technical_sheet"]
    specs = {}
    for _, row in df.iterrows():
        brand = str(row.get("MARQUE","")).strip().upper()
        model = str(row.get("MODELE","")).strip().upper()
        if brand and brand != "NAN" and model and model != "NAN":
            specs[(brand, model)] = {c: row.get(c,"") for c in spec_cols}
    return specs


def find_photos(photos_dir: Path) -> dict:
    photos = {}
    if not photos_dir.exists(): return photos
    for f in sorted(photos_dir.iterdir()):
        if f.suffix.lower() in {".jpg",".jpeg",".png",".webp"}:
            m = re.match(r"(GIZ\w+?)(?:_\d+)?\.(?:jpg|jpeg|png|webp)", f.name, re.IGNORECASE)
            if m:
                giz = m.group(1).upper()
                photos.setdefault(giz, []).append(f)
    return photos


# ─── SparkLayer-prislista ─────────────────────────────────────────────────────

def update_pricelists(new_products: list, dry_run: bool = False) -> None:
    """
    Lägg till nya GIZ-produkter i reCarpet-pricelists-master.xlsx och
    regenerera de 8 SparkLayer-CSV-filerna.

    new_products: lista av dict med {giz_id, price_per_sqm}
    """
    if not new_products:
        print("  ✓ Inga nya produkter att lägga till i prislistorna")
        return

    if not PRICELISTS_EXCEL.exists():
        print(f"  ⚠ {PRICELISTS_EXCEL} hittades inte — hoppar över prisliste-uppdatering")
        return

    print(f"\n📊 Uppdaterar prislistor ({len(new_products)} nya produkter)...")

    if dry_run:
        for p in new_products:
            print(f"  [dry-run] Skulle lägga till {p['giz_id']} @ {p['price_per_sqm']} SEK")
        return

    wb = load_workbook(PRICELISTS_EXCEL)

    def thin():
        s = Side(style='thin', color='CCCCCC')
        return Border(left=s, right=s, top=s, bottom=s)

    def append_rows(ws, sku, tier_prices, color_flag):
        """Lägg till rader för ett SKU med 3 kvantitetsnivåer."""
        # Hitta sista raden med data (efter header-rader 1-4)
        last_row = 4
        for row in ws.iter_rows(min_row=5):
            if row[0].value is not None:
                last_row = row[0].row

        bg = "F5F5F5"  # växlande bakgrund
        for i, (qty, price) in enumerate(zip(QTY_TIERS, tier_prices)):
            r = last_row + 1 + i
            row_bg = bg if (last_row // 3) % 2 == 0 else "FFFFFF"

            # SKU (A), Qty (B), SEK (C)
            for col, val, txt_color in [
                (1, sku,   "000000"),
                (2, qty,   "000000"),
                (3, round(price, 2), "0000FF"),
            ]:
                c = ws.cell(row=r, column=col, value=val)
                c.font = Font(name="Arial", color=txt_color, size=10)
                c.fill = PatternFill("solid", start_color=row_bg)
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = "#,##0.00" if col == 3 else "0"
                c.border = thin()

            # NOK (D), DKK (E), EUR (F) — formler som refererar Exchange Rates
            for col, rate_row in [(4, 4), (5, 5), (6, 6)]:
                c = ws.cell(row=r, column=col)
                c.value = f"=ROUND(C{r}*'Exchange Rates'!$C${rate_row},2)"
                c.font = Font(name="Arial", color="008000", size=10)
                c.fill = PatternFill("solid", start_color=row_bg)
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = "#,##0.00"
                c.border = thin()

            # Export-kolumner G–J
            for ecol, pcol in [(7, 3), (8, 4), (9, 5), (10, 6)]:
                pl = get_column_letter(pcol)
                c = ws.cell(row=r, column=ecol)
                c.value = f"=A{r}&\",\"&B{r}&\",\"&TEXT({pl}{r},\"0.00\")"
                c.font = Font(name="Arial", color="555555", size=9)
                c.fill = PatternFill("solid", start_color="EFEFEF")
                c.alignment = Alignment(horizontal="left", vertical="center")
                c.border = thin()
                ws.row_dimensions[r].height = 17

    for p in new_products:
        giz       = p["giz_id"]
        base_price = p["price_per_sqm"]

        member_prices       = [round(base_price * m, 2) for m in MEMBER_MULTIPLIERS]
        entrepreneur_prices = [round(base_price * m, 2) for m in ENTREPRENEUR_MULTIPLIERS]

        # Kolla om GIZ redan finns i Member-arket
        ws_mem = wb["Members"]
        existing_skus = [ws_mem.cell(row=r, column=1).value for r in range(5, ws_mem.max_row + 1)]
        if giz in existing_skus:
            print(f"  ↩  {giz} finns redan i prislistorna")
            continue

        append_rows(wb["Members"],      giz, member_prices,       "member")
        append_rows(wb["Entrepreneur"], giz, entrepreneur_prices,  "entrepreneur")
        print(f"  +  {giz}  →  member: {member_prices[0]} SEK  /  entrepreneur: {entrepreneur_prices[0]} SEK")

    wb.save(PRICELISTS_EXCEL)
    print(f"  💾 Sparat: {PRICELISTS_EXCEL.name}")

    # Regenerera SparkLayer-CSV:er
    regenerate_sparklayer_csvs()


def regenerate_sparklayer_csvs() -> None:
    """Regenerera 8 SparkLayer-CSV:er från det uppdaterade Excel-arket."""
    if not PRICELISTS_EXCEL.exists():
        return

    SPARKLAYER_DIR.mkdir(exist_ok=True)
    wb = load_workbook(PRICELISTS_EXCEL, data_only=True)

    ws_rates = wb["Exchange Rates"]
    rates = {
        "sek": 1.0,
        "nok": ws_rates.cell(row=4, column=3).value or 0.97,
        "dkk": ws_rates.cell(row=5, column=3).value or 0.67,
        "eur": ws_rates.cell(row=6, column=3).value or 0.089,
    }

    exports = [
        ("sparklayer-entrepreneur-sek.csv", "Entrepreneur", "sek"),
        ("sparklayer-entrepreneur-nok.csv", "Entrepreneur", "nok"),
        ("sparklayer-entrepreneur-dkk.csv", "Entrepreneur", "dkk"),
        ("sparklayer-entrepreneur-eur.csv", "Entrepreneur", "eur"),
        ("sparklayer-member-sek.csv",       "Members",      "sek"),
        ("sparklayer-member-nok.csv",       "Members",      "nok"),
        ("sparklayer-member-dkk.csv",       "Members",      "dkk"),
        ("sparklayer-member-eur.csv",       "Members",      "eur"),
    ]

    print("\n💱 Regenererar SparkLayer-prislistor...")
    for filename, sheet_name, currency in exports:
        ws    = wb[sheet_name]
        rate  = rates[currency]
        path  = SPARKLAYER_DIR / filename
        count = 0
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sku", "quantity", "price"])
            row = 5
            while True:
                sku = ws.cell(row=row, column=1).value
                qty = ws.cell(row=row, column=2).value
                sek = ws.cell(row=row, column=3).value
                if sku is None: break
                if sek is not None:
                    writer.writerow([sku, qty, f"{round(float(sek) * rate, 2):.2f}"])
                    count += 1
                row += 1
        print(f"  ✓  {filename}  ({count} rader)")


# ─── Hjälpfunktioner ──────────────────────────────────────────────────────────

def safe(val, fallback="") -> str:
    if pd.isna(val) or str(val).upper() in {"NAN","NONE",""}: return fallback
    return str(val).strip()


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text)


def build_title(brand: str, model: str, colorway: str) -> str:
    parts = [p.strip().title() for p in [brand, model, colorway]
             if p and p.upper() not in {"NAN","NONE",""}]
    return " — ".join(parts) if parts else "Okänd produkt"


def load_sync_log() -> dict:
    if SYNC_LOG.exists():
        with open(SYNC_LOG) as f: return json.load(f)
    return {}


def save_sync_log(log: dict) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(SYNC_LOG, "w") as f: json.dump(log, f, indent=2)


# ─── Huvudlogik ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delivery", default="sample-delivery")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulera utan att skriva till Shopify")
    args = parser.parse_args()

    # Validera
    if not args.dry_run:
        if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
            print("✗ SHOPIFY_SHOP och SHOPIFY_TOKEN måste sättas i .env")
            sys.exit(1)

    delivery_dir = BASE_DIR / args.delivery
    errors = []
    for f, name in [(delivery_dir/"stock.xlsx","stock.xlsx"),
                    (delivery_dir/"prices.csv","prices.csv"),
                    (SPECS_FILE,"product-specs.xlsx")]:
        if not f.exists(): errors.append(f"  • {name} saknas")
    if errors:
        print("✗ Saknade filer:\n" + "\n".join(errors)); sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"\n🚀 reCarpet Orak Import [{mode}]")
    print(f"   Leverans: {delivery_dir.name}")
    print(f"   Shopify:  {SHOPIFY_SHOP or '(dry-run)'}\n")

    # Ladda data
    print("📂 Laddar data...")
    stock  = load_stock(delivery_dir / "stock.xlsx")
    prices = load_prices(delivery_dir / "prices.csv")
    specs  = load_specs(SPECS_FILE)
    photos = find_photos(delivery_dir / "photos")
    print(f"   {len(stock)} produkter · {len(prices)} priser · {len(specs)} modeller · {len(photos)} bildmappar")

    # Hämta befintliga Shopify-produkter
    existing = {}
    sync_log = load_sync_log()
    if not args.dry_run:
        existing = get_existing_products_by_sku()

    # Stats
    created = updated = skipped = errors_count = 0
    new_for_pricelists = []

    print(f"\n🏗️  Synkroniserar produkter...")
    for _, row in stock.iterrows():
        giz      = safe(row.get("giz_id"))
        brand    = safe(row.get("brand"))
        model    = safe(row.get("model"))
        colorway = safe(row.get("colorway"))
        origin   = safe(row.get("origin"))
        fmt      = safe(row.get("format"))
        stock_m2 = row.get("stock_sqm", 0)
        price    = prices.get(giz)

        if not giz or not brand: continue

        title = build_title(brand, model, colorway)

        # Specs-uppslag
        spec = specs.get((brand, model), {})
        if not spec:
            clean = re.sub(r"[^A-Z0-9 ]", "", model)
            for (b, m), s in specs.items():
                if b == brand and re.sub(r"[^A-Z0-9 ]", "", m) == clean:
                    spec = s; break

        # Bygg metafält
        metafields = [
            {"namespace":"recarpet","key":"giz_id",           "value":giz,                          "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"brand",            "value":brand.title(),                 "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"model",            "value":model.title(),                 "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"colorway",         "value":colorway,                      "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"format",           "value":fmt,                           "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"origin",           "value":origin,                        "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"stock_sqm",        "value":str(round(float(stock_m2),2)), "type":"number_decimal"},
            {"namespace":"recarpet","key":"min_order_sqm",    "value":str(safe(spec.get("min_order_sqm"),"5")),   "type":"number_decimal"},
            {"namespace":"recarpet","key":"delivery_days",    "value":str(safe(spec.get("delivery_days"),"15")),  "type":"number_integer"},
            {"namespace":"recarpet","key":"thickness",        "value":safe(spec.get("thickness")),    "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"fire_rating",      "value":safe(spec.get("fire_rating")),  "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"acoustic_rating",  "value":safe(spec.get("acoustic_rating")), "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"impact_absorption","value":safe(spec.get("impact_absorption")), "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"lrv",              "value":safe(spec.get("lrv")),          "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"backing",          "value":safe(spec.get("backing")),      "type":"single_line_text_field"},
            {"namespace":"recarpet","key":"technical_sheet",  "value":safe(spec.get("technical_sheet")), "type":"url"},
            {"namespace":"recarpet","key":"ecodesigned",      "value":str(safe(spec.get("ecodesigned","false"))).lower(), "type":"boolean"},
        ]
        # Ta bort tomma metafält
        metafields = [m for m in metafields if m["value"]]

        is_new = giz not in existing

        if args.dry_run:
            action = "SKAPA" if is_new else "UPPDATERA"
            print(f"  [{action}] {giz} — {title} @ {price or '?'} SEK, {stock_m2} m²")
            if is_new and price:
                new_for_pricelists.append({"giz_id": giz, "price_per_sqm": price})
            skipped += 1
            continue

        try:
            if is_new:
                # Skapa ny produkt
                product_data = {
                    "title":        title,
                    "vendor":       brand.title(),
                    "product_type": "Moquette de réemploi",
                    "tags":         f"b2b,{brand.lower()},{fmt}".strip(","),
                    "published":    True,
                    "body_html":    f"<p><strong>Ursprung:</strong> {origin}</p>" if origin else "",
                    "variants": [{
                        "sku":                  giz,
                        "price":                f"{price:.2f}" if price else "0.00",
                        "inventory_management": "shopify",
                        "inventory_quantity":   int(float(stock_m2)) if stock_m2 else 0,
                        "requires_shipping":    False,
                        "taxable":              True,
                    }],
                }
                product = create_product(product_data)
                product_id = product["id"]
                variant_id = product["variants"][0]["id"]

                sync_log[giz] = {"product_id": product_id, "variant_id": variant_id}
                existing[giz] = {"product_id": product_id, "variant_id": variant_id}

                # Metafält
                set_product_metafields(product_id, metafields)

                # Bilder
                img_paths = photos.get(giz.upper(), [])
                for i, img_path in enumerate(img_paths, start=1):
                    upload_product_image(product_id, img_path, position=i, alt=title)

                print(f"  ✅ SKAPADE  {giz} — {title}")
                created += 1

                if price:
                    new_for_pricelists.append({"giz_id": giz, "price_per_sqm": price})

            else:
                # Uppdatera befintlig produkt
                info = existing[giz]
                update_product(info["product_id"], info["variant_id"], {
                    "inventory_quantity": int(float(stock_m2)) if stock_m2 else 0,
                    "price": f"{price:.2f}" if price else None,
                })
                print(f"  🔄 UPPDATERADE {giz} — {stock_m2} m²")
                updated += 1

        except Exception as e:
            print(f"  ✗ FEL för {giz}: {e}")
            errors_count += 1

    # Spara sync-log
    if not args.dry_run:
        save_sync_log(sync_log)

    # Uppdatera prislistor + SparkLayer-CSV:er
    update_pricelists(new_for_pricelists, dry_run=args.dry_run)

    # Sammanfattning
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅  Klart [{mode}]
    Skapade:    {created}
    Uppdaterade:{updated}
    Hoppade:    {skipped}
    Fel:        {errors_count}
    Prislistor: {len(new_for_pricelists)} nya produkter tillagda
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    main()
