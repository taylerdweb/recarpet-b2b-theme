"""
reCarpet — Orak Import Script (New CSV Format)
===============================================
Läser ORAKs standard CSV-export och:
  1. Skapar/uppdaterar produkter i Shopify via Admin API
  2. Sätter meta fields (dimensioner, teknisk spec, etc.)
  3. Genererar SparkLayer-prislistor för Silver (0%) och Guld (-10%)
  4. Publicerar produkter till SparkLayer B2B-kanal automatiskt
  5. Lägger till produkter i rätt produktserie (collection)

Usage:
    python import-orak.py --csv path/to/orak.csv
    python import-orak.py --csv path/to/orak.csv --dry-run
    python import-orak.py --csv path/to/orak.csv --pricelists-only

Krav:
    pip install pandas requests python-dotenv

Setup:
    1. Kopiera .env.example → .env och fyll i credentials
    2. Kör setup-metafields.py en gång för att skapa meta field definitions
    3. Kör detta script med ORAKs CSV-fil
"""

import os
import sys
import csv
import json
import time
import argparse
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Konfiguration ────────────────────────────────────────────────────────────

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")    # t.ex. recarpet.myshopify.com
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")   # Admin API access token
API_VERSION   = "2024-01"

BASE_DIR   = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
SYNC_LOG   = OUTPUT_DIR / "sync-log.json"

SPARKLAYER_DIR = BASE_DIR.parent / "sparklayer-pricelists"

# SparkLayer pricelist multipliers
# Brons (public): no pricelist — sees standard Shopify price
# Silver (member): netto x 1.00 (0% discount)
# Guld (entrepreneur): netto x 0.90 (10% discount)
SILVER_MULTIPLIER = 1.00
GULD_MULTIPLIER   = 0.90

# SparkLayer sales channel name (exact title as it appears in Shopify Admin → Settings → Sales channels)
SPARKLAYER_CHANNEL_NAME = "SparkLayer B2B & Wholesale"

# Produktserie — alla ORAK-produkter hamnar i "Återbrukade mattor"
# OBS: handlen ändras INTE när du byter namn i Shopify Admin.
# Kolla rätt handle: Admin → Collections → klicka samlingen → rulla ner till "Sökmotor"-sektionen
ATERVUNNA_HANDLE = "atervunna-mattor"  # ändra om handlen är annorlunda, t.ex. "mattor"

# "Produit à venir" = återbrukade mattor under rengöring → publiceras direkt men märks med tagg "kommande"
KOMMANDE_LABELS = {"produit a venir", "a venir"}

# ORAK CSV column → internal key mapping
COLUMN_MAP = {
    "title":             "title",
    "brand":             "brand",
    "productType":       "product_label",
    "identificationID":  "sku",
    "dimensions":        "dimensions",
    "pricePerUnit":      "price",
    "quantityAvailable": "quantity",
    "mainImage":         "image_url",
    "technicalSheetURL": "technical_sheet_url",
}


# ─── Shopify API ──────────────────────────────────────────────────────────────

def api_headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }


def shopify_get(endpoint, params=None):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.get(url, headers=api_headers(), params=params)
    _rate_limit(r)
    r.raise_for_status()
    return r.json()


def shopify_post(endpoint, payload):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.post(url, headers=api_headers(), json=payload)
    _rate_limit(r)
    r.raise_for_status()
    return r.json()


def shopify_put(endpoint, payload):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.put(url, headers=api_headers(), json=payload)
    _rate_limit(r)
    r.raise_for_status()
    return r.json()


def _rate_limit(response):
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 2))
        print(f"    Waiting {wait}s (rate limit)...")
        time.sleep(wait)
    else:
        header = response.headers.get("X-Shopify-Shop-Api-Call-Limit", "")
        if header:
            used, total = map(int, header.split("/"))
            if used / total > 0.8:
                time.sleep(0.5)
        else:
            time.sleep(0.25)


def get_sparklayer_publication_id() -> int | None:
    """Hämtar publication_id för SparkLayer-kanalen."""
    try:
        data = shopify_get("publications.json")
        for pub in data.get("publications", []):
            if SPARKLAYER_CHANNEL_NAME.lower() in pub.get("name", "").lower():
                print(f"  SparkLayer publication_id: {pub['id']}  ({pub['name']})")
                return pub["id"]
        names = [p.get("name") for p in data.get("publications", [])]
        print(f"  Warning: SparkLayer channel ej hittad. Tillgängliga: {names}")
    except Exception as e:
        print(f"  Warning: kunde inte hämta publications: {e}")
    return None


def publish_to_sparklayer(product_id: int, publication_id: int):
    """Publicerar en produkt till SparkLayer-kanalen."""
    try:
        shopify_post(
            f"products/{product_id}/publications.json",
            {"publish": {"publication_id": publication_id}},
        )
    except Exception as e:
        print(f"      Warning: SparkLayer-publicering misslyckades för {product_id}: {e}")


def get_collection_id_map() -> dict:
    """Returnerar {handle: collection_id} för alla custom collections."""
    id_map = {}
    try:
        data = shopify_get("custom_collections.json", {"limit": 250, "fields": "id,handle,title"})
        for col in data.get("custom_collections", []):
            id_map[col["handle"]] = col["id"]
    except Exception as e:
        print(f"  Warning: kunde inte hämta collections: {e}")
    return id_map


def add_product_to_collection(product_id: int, collection_id: int):
    """Lägger till en produkt i en collection (skapar collect om den inte finns)."""
    try:
        shopify_post("collects.json", {
            "collect": {"product_id": product_id, "collection_id": collection_id}
        })
    except Exception as e:
        # 422 = redan i collection, ignorera
        if "422" not in str(e):
            print(f"      Warning: collection-tilldelning misslyckades: {e}")


def get_existing_skus() -> dict:
    print("  Fetching existing products from Shopify...")
    sku_map = {}
    params = {"limit": 250, "fields": "id,title,variants"}
    data = shopify_get("products.json", params)
    for product in data.get("products", []):
        for variant in product.get("variants", []):
            if variant.get("sku"):
                sku_map[variant["sku"]] = {
                    "product_id": product["id"],
                    "variant_id": variant["id"],
                    "inventory_item_id": variant.get("inventory_item_id"),
                }
    print(f"    {len(sku_map)} existing products found")
    return sku_map


def get_first_location_id() -> int:
    locations = shopify_get("locations.json")
    return locations["locations"][0]["id"]


def create_product(title, vendor, product_type, tags, price, sku, image_url) -> dict:
    payload = {
        "product": {
            "title": title,
            "vendor": vendor,
            "product_type": product_type,
            "tags": tags,
            "published": True,
            "variants": [{
                "sku": sku,
                "price": f"{price:.2f}",
                "inventory_management": "shopify",
                "requires_shipping": False,
                "taxable": True,
            }],
        }
    }
    if image_url:
        payload["product"]["images"] = [{"src": image_url, "alt": title}]
    return shopify_post("products.json", payload)["product"]


def update_variant_price(variant_id, price):
    shopify_put(f"variants/{variant_id}.json", {
        "variant": {"id": variant_id, "price": f"{price:.2f}"}
    })


def set_inventory(inventory_item_id, location_id, quantity):
    shopify_post("inventory_levels/set.json", {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": int(quantity),
    })


def set_metafields(product_id, metafields: list):
    for mf in metafields:
        if not mf.get("value"):
            continue
        try:
            shopify_post(f"products/{product_id}/metafields.json", {"metafield": mf})
        except Exception as e:
            print(f"      Warning: metafield '{mf['key']}' failed: {e}")


# ─── Data loading ─────────────────────────────────────────────────────────────

def load_orak_csv(path: Path) -> list:
    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    df = df.rename(columns=COLUMN_MAP)

    def fix_url(x):
        if isinstance(x, str) and x.startswith("//"):
            return "https:" + x
        return x

    if "image_url" in df.columns:
        df["image_url"] = df["image_url"].apply(fix_url)
    if "technical_sheet_url" in df.columns:
        df["technical_sheet_url"] = df["technical_sheet_url"].apply(fix_url)

    df = df[df["sku"].notna() & (df["sku"].astype(str).str.strip() != "")]
    df = df[df["title"].notna() & (df["title"].astype(str).str.strip() != "")]
    return df.to_dict("records")


def safe(val, fallback="") -> str:
    if pd.isna(val) if hasattr(pd, 'isna') else val != val:
        return fallback
    s = str(val).strip()
    return fallback if s in {"nan", "None", ""} else s


# ─── Sync log ─────────────────────────────────────────────────────────────────

def load_sync_log() -> dict:
    if SYNC_LOG.exists():
        with open(SYNC_LOG) as f:
            return json.load(f)
    return {}


def save_sync_log(log: dict):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(SYNC_LOG, "w") as f:
        json.dump(log, f, indent=2)


# ─── SparkLayer pricelists ─────────────────────────────────────────────────────

def generate_pricelists(products: list):
    """
    Generate SparkLayer pricelist CSVs.
    Format: sku, quantity, price  (quantity=1 means any quantity)
    """
    SPARKLAYER_DIR.mkdir(exist_ok=True)

    silver_rows = []
    guld_rows   = []

    for p in products:
        sku = safe(p.get("sku"))
        try:
            base = float(p.get("price", 0) or 0)
        except (ValueError, TypeError):
            continue
        if not sku or base <= 0:
            continue

        silver_rows.append([sku, 1, f"{round(base * SILVER_MULTIPLIER, 2):.2f}"])
        guld_rows.append(  [sku, 1, f"{round(base * GULD_MULTIPLIER,   2):.2f}"])

    def write_csv(filename, rows):
        path = SPARKLAYER_DIR / filename
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sku", "quantity", "price"])
            writer.writerows(rows)
        print(f"  OK  {filename}  ({len(rows)} SKUs)")

    print("\n  Generating SparkLayer pricelists...")
    write_csv("sparklayer-member-sek.csv",       silver_rows)
    write_csv("sparklayer-entrepreneur-sek.csv", guld_rows)
    print(f"""
  Silver  (member):      netto x {SILVER_MULTIPLIER:.0%}  (0% discount)
  Guld    (entrepreneur): netto x {GULD_MULTIPLIER:.0%}   (-{int((1-GULD_MULTIPLIER)*100)}% discount)
  Upload CSVs in SparkLayer -> Price Lists
""")


# ─── Main ─────────────────────────────────────────────────────────────────────

PRODUCT_TYPE_MAP = {
    "reemploi":        "Carpet Tile - Reemploi",
    "reemploi":        "Carpet Tile - Reemploi",
    "fin de serie":    "Carpet Tile - Fin de serie",
    "produit a venir": "Carpet Tile - A venir",
}


def normalise_label(s: str) -> str:
    """Remove accents for map lookup."""
    replacements = {"é": "e", "è": "e", "ê": "e", "à": "a", "â": "a", "ô": "o", "û": "u", "î": "i"}
    result = s.lower()
    for k, v in replacements.items():
        result = result.replace(k, v)
    return result


def main():
    parser = argparse.ArgumentParser(description="reCarpet - ORAK Product Import")
    parser.add_argument("--csv",             required=True,      help="Path to ORAK CSV file")
    parser.add_argument("--dry-run",         action="store_true", help="Simulate without writing to Shopify")
    parser.add_argument("--pricelists-only", action="store_true", help="Only generate SparkLayer CSVs")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)

    if not args.dry_run and not args.pricelists_only:
        if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
            print("Error: set SHOPIFY_SHOP and SHOPIFY_TOKEN in .env")
            sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else ("PRICELISTS ONLY" if args.pricelists_only else "LIVE")
    print(f"\nreCarpet - ORAK Import [{mode}]")
    print(f"  CSV: {csv_path.name}")
    print(f"  Shopify: {SHOPIFY_SHOP or '(not active)'}\n")

    print("Loading ORAK data...")
    products = load_orak_csv(csv_path)
    print(f"  {len(products)} products loaded\n")

    # Always generate pricelists
    generate_pricelists(products)

    if args.pricelists_only:
        return

    sync_log = load_sync_log()
    existing = {}
    location_id = None
    sparklayer_pub_id = None
    collection_id_map = {}

    if not args.dry_run:
        existing          = get_existing_skus()
        location_id       = get_first_location_id()
        sparklayer_pub_id = get_sparklayer_publication_id()
        collection_id_map = get_collection_id_map()
        if not collection_id_map:
            print("  OBS: Inga collections hittade. Skapa dem i Shopify Admin först.")
        else:
            print(f"  Collections hittade: {list(collection_id_map.keys())}")

    created = updated = skipped = errors = 0

    print("Syncing products to Shopify...")
    for p in products:
        sku       = safe(p.get("sku"))
        title     = safe(p.get("title"))
        brand     = safe(p.get("brand"), "Unknown")
        label     = safe(p.get("product_label"), "")
        dims      = safe(p.get("dimensions"), "")
        image_url = safe(p.get("image_url"), "")
        tech_url  = safe(p.get("technical_sheet_url"), "")

        try:
            price    = float(p.get("price", 0) or 0)
            quantity = int(float(p.get("quantity", 0) or 0))
        except (ValueError, TypeError):
            price, quantity = 0.0, 0

        if not sku:
            skipped += 1
            continue

        product_type = PRODUCT_TYPE_MAP.get(normalise_label(label), "Carpet Tile")

        # Taggar: alla ORAK-produkter får "atervunna-mattor"; "Produit à venir" får dessutom "kommande"
        label_key = normalise_label(label) if label else ""
        extra_tags = ["kommande"] if label_key in KOMMANDE_LABELS else []
        tags = ",".join(filter(None, [
            "b2b", "b2b-only", "orak", "atervunna-mattor",
            brand.lower(),
            label_key.replace(" ", "-") if label_key else "",
        ] + extra_tags))

        metafields = []
        if dims:
            metafields.append({"namespace": "recarpet", "key": "dimensions",         "value": dims,     "type": "single_line_text_field"})
        if tech_url:
            metafields.append({"namespace": "recarpet", "key": "technical_sheet_url","value": tech_url, "type": "url"})
        if label:
            metafields.append({"namespace": "recarpet", "key": "product_label",      "value": label,    "type": "single_line_text_field"})

        is_new = sku not in existing

        # Alla ORAK-produkter → "Återbrukade mattor"
        collection_id = collection_id_map.get(ATERVUNNA_HANDLE)
        kommande_note = " [kommande]" if label_key in KOMMANDE_LABELS else ""

        if args.dry_run:
            action = "CREATE" if is_new else "UPDATE"
            print(f"  [{action}] {sku}  {title}  price:{price:.2f}  qty:{quantity}  → {ATERVUNNA_HANDLE}{kommande_note}")
            skipped += 1
            continue

        try:
            if is_new:
                product     = create_product(title, brand, product_type, tags, price, sku, image_url)
                product_id  = product["id"]
                variant_id  = product["variants"][0]["id"]
                inv_item_id = product["variants"][0]["inventory_item_id"]

                set_inventory(inv_item_id, location_id, quantity)
                set_metafields(product_id, metafields)

                # Publicera till SparkLayer
                if sparklayer_pub_id:
                    publish_to_sparklayer(product_id, sparklayer_pub_id)

                # Lägg till i rätt produktserie
                if collection_id:
                    add_product_to_collection(product_id, collection_id)

                sync_log[sku] = {"product_id": product_id, "variant_id": variant_id, "inventory_item_id": inv_item_id}
                existing[sku] = sync_log[sku]

                pub_ok = "✓ SparkLayer" if sparklayer_pub_id else "– SparkLayer (ej konfigurerad)"
                col_ok = f"✓ {ATERVUNNA_HANDLE}" if collection_id else f"– {ATERVUNNA_HANDLE} (collection saknas — kolla handle)"
                print(f"  CREATED  {sku} - {title}{kommande_note}  [{pub_ok}] [{col_ok}]")
                created += 1
            else:
                info = existing[sku]
                update_variant_price(info["variant_id"], price)
                if info.get("inventory_item_id"):
                    set_inventory(info["inventory_item_id"], location_id, quantity)
                set_metafields(info["product_id"], metafields)

                # Publicera till SparkLayer (idempotent — skadas inte av att köras igen)
                if sparklayer_pub_id:
                    publish_to_sparklayer(info["product_id"], sparklayer_pub_id)

                # Säkerställ att produkten finns i "Återbrukade mattor"
                if collection_id:
                    add_product_to_collection(info["product_id"], collection_id)

                print(f"  UPDATED  {sku} - qty:{quantity}  price:{price:.2f}{kommande_note}")
                updated += 1

        except Exception as e:
            print(f"  ERROR {sku}: {e}")
            errors += 1

    if not args.dry_run:
        save_sync_log(sync_log)

    print(f"""
-------------------------------------
Done [{mode}]
  Created:  {created}
  Updated:  {updated}
  Skipped:  {skipped}
  Errors:   {errors}
-------------------------------------
""")


if __name__ == "__main__":
    main()
