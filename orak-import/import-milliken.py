#!/usr/bin/env python3
"""
reCarpet — Milliken Import Script
===================================
Läser Millikens produktexport (xlsx) och:
  1. Skapar/uppdaterar produkter i Shopify via Admin API
  2. Sätter metafields (dimensioner, kollektion, färg, installationsmetod, produkttyp)
  3. Genererar SparkLayer-prislistor (appendar till befintliga CSV:er)
  4. Publicerar produkter till SparkLayer B2B-kanal
  5. Lägger till produkter i "Nya golv" (eller angiven) collection

Usage:
    python import-milliken.py --xlsx path/to/Product\ Export.xlsx
    python import-milliken.py --xlsx path/to/Product\ Export.xlsx --dry-run
    python import-milliken.py --xlsx path/to/Product\ Export.xlsx --pricelists-only

Krav:
    pip install pandas requests python-dotenv openpyxl

Obs:
    Milliken-exporten har INGA priser — mock-priser genereras per produkttyp.
    Uppdatera MOCK_PRICES nedan när riktiga priser finns.
    Milliken-exporten har INGEN lagerstatus — sätts till 9999 (alltid i lager).
"""

import os
import sys
import csv
import json
import time
import math
import argparse
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv

# Reuse shared config from import-orak.py's .env
load_dotenv()

# ─── Konfiguration ────────────────────────────────────────────────────────────

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION   = "2024-01"

BASE_DIR       = Path(__file__).parent
OUTPUT_DIR     = BASE_DIR / "output"
SYNC_LOG       = OUTPUT_DIR / "sync-log-milliken.json"
SPARKLAYER_DIR = BASE_DIR.parent / "sparklayer-pricelists"

# SparkLayer pricelist multipliers (same as Orak)
SILVER_MULTIPLIER = 1.00
GULD_MULTIPLIER   = 0.90
KRETS_MULTIPLIER  = 0.80

# Fallback exchange rates
FALLBACK_RATES = {
    "EUR_SEK": 11.20,
    "EUR_NOK": 11.70,
    "EUR_DKK": 7.46,
    "source":  "fallback",
}

# ─── Mock-priser (EUR per m²) — uppdatera med riktiga priser från Milliken ───
# Dessa används tills ni har en prislista från Milliken.
MOCK_PRICES_EUR = {
    "Carpet Tile":            22.00,
    "Luxury Vinyl Tile (LVT)": 30.00,
    "Woven Design Tile":       35.00,
}
MOCK_PRICE_DEFAULT = 25.00

# Mock stock — Milliken är alltid tillgängligt (nyproduktion)
MOCK_STOCK = 9999

# SKU prefix for Milliken
SKU_PREFIX = "Milliken"

# Collection handle for new/Milliken products
MILLIKEN_COLLECTION_HANDLE = "nya-mattor"

# ─── Prisavrundning ───────────────────────────────────────────────────────────
def ceil_price(value, decimals=2):
    """Round a price UP to the given number of decimal places."""
    factor = 10 ** decimals
    return math.ceil(value * factor) / factor


# ─── Shopify API (shared logic with import-orak.py) ──────────────────────────

def api_headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }

def _rate_limit(r):
    limit = r.headers.get("X-Shopify-Shop-Api-Call-Limit", "0/40")
    used, cap = map(int, limit.split("/"))
    if used > cap - 4:
        time.sleep(1.0)

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

def get_location_id():
    data = shopify_get("locations.json")
    return data["locations"][0]["id"]

def get_existing_products_by_sku() -> dict:
    """Hämtar alla produkter med Milliken-SKU:er från Shopify."""
    existing = {}
    params = {"limit": 250, "fields": "id,variants"}
    endpoint = "products.json"
    while True:
        data = shopify_get(endpoint, params)
        for p in data["products"]:
            for v in p["variants"]:
                if v.get("sku", "").startswith(SKU_PREFIX):
                    existing[v["sku"]] = {
                        "product_id": p["id"],
                        "variant_id": v["id"],
                        "inventory_item_id": v.get("inventory_item_id"),
                    }
        link = data.get("products", [])
        if len(data["products"]) < 250:
            break
        params["since_id"] = data["products"][-1]["id"]
    return existing

def create_product(title, vendor, product_type, tags, price, sku, image_url, body_html="") -> dict:
    payload = {
        "product": {
            "title": title,
            "vendor": vendor,
            "product_type": product_type,
            "tags": tags,
            "body_html": body_html,
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

def update_product(product_id, variant_id, title, vendor, product_type, tags, price, image_url, body_html=""):
    payload = {
        "product": {
            "id": product_id,
            "title": title,
            "vendor": vendor,
            "product_type": product_type,
            "tags": tags,
            "body_html": body_html,
            "variants": [{"id": variant_id, "price": f"{price:.2f}"}],
        }
    }
    if image_url:
        payload["product"]["images"] = [{"src": image_url, "alt": title}]
    shopify_put(f"products/{product_id}.json", payload)

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

def get_sparklayer_publication_gid():
    query = """{ publications(first: 20) { edges { node { id name } } } }"""
    try:
        r = requests.post(
            f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/graphql.json",
            headers=api_headers(),
            json={"query": query},
        )
        r.raise_for_status()
        for edge in r.json()["data"]["publications"]["edges"]:
            if "sparklayer" in edge["node"]["name"].lower():
                return edge["node"]["id"]
    except Exception:
        pass
    return None

def publish_to_sparklayer(product_id, publication_gid):
    mutation = """
    mutation($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) { userErrors { field message } }
    }
    """
    variables = {
        "id": f"gid://shopify/Product/{product_id}",
        "input": [{"publicationId": publication_gid}],
    }
    try:
        requests.post(
            f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/graphql.json",
            headers=api_headers(),
            json={"query": mutation, "variables": variables},
        )
    except Exception:
        pass

def get_collection_id_map() -> dict:
    """Hämtar alla collections och mappar handle+title → id."""
    result = {}
    params = {"limit": 250, "fields": "id,handle,title"}
    for kind in ("custom_collections", "smart_collections"):
        try:
            data = shopify_get(f"{kind}.json", params)
            for c in data[kind]:
                result[c["handle"]] = c["id"]
                result[c["title"].lower()] = c["id"]
        except Exception:
            pass
    return result

def add_product_to_collection(product_id, collection_id):
    try:
        shopify_post("collects.json", {
            "collect": {"product_id": product_id, "collection_id": collection_id}
        })
    except Exception:
        pass


# ─── Data loading ─────────────────────────────────────────────────────────────

def load_milliken_xlsx(path: Path) -> list:
    """
    Läser Millikens xlsx-export och omvandlar till standardiserat format.

    Milliken-fält → reCarpet-mappning:
      - Collection Name + ColourCodeParse + ColourNameParse → title
      - ProductID → sku (Milliken-{ProductID})
      - FullSizeImageFilename → image_url
      - ProductLengthCM × ProductWidthCM → dimensions
      - Product Types → product_type
      - Collection Name → collection_name (metafield)
      - Design Name → design_name (metafield)
      - ColourCodeParse → colour_code (metafield)
      - ColourNameParse → colour_name (metafield)
      - Approved Installation Methods → installation_methods (metafield)
      - Market → market (metafield)
    """
    df = pd.read_excel(path)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Filter to Europe market only
    df = df[df["Marketing Regions"].str.contains("Europe", case=False, na=False)]

    # Drop rows without ProductID
    df = df[df["ProductID"].notna()]

    # Deduplicate by ProductID (keep first)
    df = df.drop_duplicates(subset="ProductID", keep="first")

    products = []
    for _, row in df.iterrows():
        collection = str(row.get("Collection Name", "")).strip()
        colour_code = str(row.get("ColourCodeParse", "")).strip()
        colour_name = str(row.get("ColourNameParse", "")).strip()
        design_name = str(row.get("Design Name", "")).strip()
        product_id = str(int(row["ProductID"]))
        product_type_raw = str(row.get("Product Types", "Carpet Tile")).strip()

        # Title: "Collection — ColourCode ColourName"
        # e.g. "Clerkenwell — CLE205 Navigate"
        title = f"{collection} — {colour_code} {colour_name}".strip()

        # SKU: Milliken-{ProductID}
        sku = f"{SKU_PREFIX}-{product_id}"

        # Dimensions from ProductLengthCM × ProductWidthCM
        length = row.get("ProductLengthCM")
        width = row.get("ProductWidthCM")
        dims = ""
        if pd.notna(length) and pd.notna(width):
            dims = f"{int(length)} × {int(width)}"

        # Image URL
        image_url = str(row.get("FullSizeImageFilename", "")).strip()
        if not image_url or image_url == "nan":
            image_url = ""

        # Installation methods (pipe-separated → comma-separated)
        install_raw = str(row.get("Approved Installation Methods", "")).strip()
        install_methods = install_raw.replace("|", ", ") if install_raw and install_raw != "nan" else ""

        # Mock price based on product type
        eur_price = MOCK_PRICES_EUR.get(product_type_raw, MOCK_PRICE_DEFAULT)

        # Map Milliken product types to Shopify product types
        shopify_product_type = product_type_raw

        products.append({
            "sku": sku,
            "title": title,
            "brand": "Milliken",
            "product_type": shopify_product_type,
            "price": eur_price,
            "quantity": MOCK_STOCK,
            "image_url": image_url,
            "dimensions": dims,
            "collection_name": collection,
            "design_name": design_name,
            "colour_code": colour_code,
            "colour_name": colour_name,
            "installation_methods": install_methods,
            "product_type_raw": product_type_raw,
        })

    print(f"  Loaded {len(products)} Milliken products from {path.name}")
    return products


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


# ─── Exchange rates ───────────────────────────────────────────────────────────

def fetch_exchange_rates() -> dict:
    try:
        r = requests.get(
            "https://api.frankfurter.app/latest?from=EUR&to=SEK,NOK,DKK",
            timeout=5
        )
        r.raise_for_status()
        data = r.json()["rates"]
        rates = {
            "EUR_SEK": round(data["SEK"], 4),
            "EUR_NOK": round(data["NOK"], 4),
            "EUR_DKK": round(data["DKK"], 4),
            "source": "live",
            "date": r.json().get("date", "okänt"),
        }
        print(f"  Valutakurser ({rates['date']}): 1 EUR = {rates['EUR_SEK']} SEK | {rates['EUR_NOK']} NOK | {rates['EUR_DKK']} DKK")
        return rates
    except Exception as e:
        print(f"  Warning: live-kurser ej tillgängliga ({e}). Använder fallback.")
        return FALLBACK_RATES.copy()


# ─── SparkLayer pricelists ────────────────────────────────────────────────────

def generate_pricelists(products: list, rates: dict):
    """
    Genererar Milliken-rader och APPENDAR till befintliga SparkLayer-prislistor.
    Om prislistorna inte finns skapas de med header.
    """
    SPARKLAYER_DIR.mkdir(exist_ok=True)

    eur_sek = rates["EUR_SEK"]
    eur_nok = rates["EUR_NOK"]
    eur_dkk = rates["EUR_DKK"]

    LISTS = {
        "sparklayer-member-sek.csv":       (SILVER_MULTIPLIER, eur_sek),
        "sparklayer-member-nok.csv":       (SILVER_MULTIPLIER, eur_nok),
        "sparklayer-member-dkk.csv":       (SILVER_MULTIPLIER, eur_dkk),
        "sparklayer-member-eur.csv":       (SILVER_MULTIPLIER, 1.0),
        "sparklayer-entrepreneur-sek.csv": (GULD_MULTIPLIER,   eur_sek),
        "sparklayer-entrepreneur-nok.csv": (GULD_MULTIPLIER,   eur_nok),
        "sparklayer-entrepreneur-dkk.csv": (GULD_MULTIPLIER,   eur_dkk),
        "sparklayer-entrepreneur-eur.csv": (GULD_MULTIPLIER,   1.0),
        "sparklayer-krets-sek.csv":        (KRETS_MULTIPLIER,  eur_sek),
    }

    list_rows = {name: [] for name in LISTS}

    for p in products:
        sku = p["sku"]
        eur_price = p["price"]
        if eur_price <= 0:
            continue

        for name, (mult, rate) in LISTS.items():
            price = ceil_price(eur_price * rate * mult)
            list_rows[name].append([sku, 1, f"{price:.2f}"])

    def append_csv(filename, rows):
        path = SPARKLAYER_DIR / filename
        # Read existing SKUs to avoid duplicates
        existing_skus = set()
        if path.exists():
            with open(path, "r") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    if row:
                        existing_skus.add(row[0])

        new_rows = [r for r in rows if r[0] not in existing_skus]

        if not path.exists():
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["sku", "quantity", "price"])
                writer.writerows(new_rows)
        else:
            with open(path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(new_rows)

        print(f"  OK  {filename}  (+{len(new_rows)} Milliken SKUs, {len(existing_skus)} existing)")

    print("\n  Appendar Milliken-priser till SparkLayer-prislistor...")
    for name, rows in list_rows.items():
        append_csv(name, rows)

    print(f"\n  Pricelists uppdaterade i {SPARKLAYER_DIR}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Import Milliken products to Shopify + SparkLayer")
    parser.add_argument("--xlsx", required=True, help="Path to Milliken Product Export.xlsx")
    parser.add_argument("--dry-run", action="store_true", help="Visa vad som skulle göras utan att ändra något")
    parser.add_argument("--pricelists-only", action="store_true", help="Generera bara prislistor, ingen Shopify-sync")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx)
    if not xlsx_path.exists():
        print(f"  FEL: Filen {xlsx_path} hittades inte.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  reCarpet — Milliken Import")
    print(f"  Fil: {xlsx_path.name}")
    print(f"{'='*60}\n")

    # 1. Load products
    products = load_milliken_xlsx(xlsx_path)
    if not products:
        print("  Inga produkter hittade. Avslutar.")
        sys.exit(0)

    # 2. Fetch exchange rates
    print("\nHämtar valutakurser...")
    rates = fetch_exchange_rates()

    # 3. Generate pricelists
    generate_pricelists(products, rates)

    if args.pricelists_only:
        print("\n  --pricelists-only: Hoppar över Shopify-sync.")
        return

    # 4. Setup Shopify (skip API calls in dry-run)
    location_id = None
    sync_log = {}
    existing = {}
    sparklayer_pub_id = None
    collection_id = None

    if args.dry_run:
        print("\n  --dry-run: Hoppar över Shopify API-anrop.")
    else:
        if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
            print("  FEL: SHOPIFY_SHOP och SHOPIFY_TOKEN måste sättas i .env")
            sys.exit(1)

        print("\nHämtar Shopify-data...")
        location_id = get_location_id()
        print(f"  Location ID: {location_id}")

        sync_log = load_sync_log()
        existing = get_existing_products_by_sku()
        existing.update(sync_log)
        print(f"  Befintliga Milliken-produkter i Shopify: {len(existing)}")

        sparklayer_pub_id = get_sparklayer_publication_gid()
        collection_id_map = get_collection_id_map()

        collection_id = (
            collection_id_map.get(MILLIKEN_COLLECTION_HANDLE)
            or collection_id_map.get("nya mattor")
            or collection_id_map.get("nya-mattor")
            or collection_id_map.get("milliken")
        )
        if collection_id:
            print(f"  Collection: {MILLIKEN_COLLECTION_HANDLE} (id:{collection_id})")
        else:
            print(f"  OBS: Collection '{MILLIKEN_COLLECTION_HANDLE}' ej hittad. Skapa den i Shopify Admin.")

    created = updated = skipped = errors = 0

    print(f"\nSyncing {len(products)} Milliken products to Shopify...")
    for p in products:
        sku = p["sku"]
        title = p["title"]
        brand = p["brand"]
        product_type = p["product_type"]
        image_url = p["image_url"]
        dims = p["dimensions"]
        eur_price = p["price"]

        price = ceil_price(eur_price * rates["EUR_SEK"])
        quantity = MOCK_STOCK

        # Tags
        tags = ",".join(filter(None, [
            "b2b", "b2b-only", "milliken", "nya-golv",
            p["product_type_raw"].lower().replace(" ", "-"),
            p["collection_name"].lower().replace(" ", "-").replace(".", ""),
        ]))

        # Body HTML — kort beskrivning
        body_parts = []
        if p["collection_name"]:
            body_parts.append(f"<p><strong>Kollektion:</strong> {p['collection_name']}</p>")
        if p["design_name"]:
            body_parts.append(f"<p><strong>Design:</strong> {p['design_name']}</p>")
        if dims:
            body_parts.append(f"<p><strong>Format:</strong> {dims} cm</p>")
        if p["installation_methods"]:
            body_parts.append(f"<p><strong>Installationsmetoder:</strong> {p['installation_methods']}</p>")
        body_html = "\n".join(body_parts)

        # Metafields — Milliken-specifika fält utöver Orak-standarderna
        metafields = [
            {"namespace": "recarpet", "key": "supplier_sku",          "value": f"Milliken-PID-{p['sku'].replace(SKU_PREFIX + '-', '')}",  "type": "single_line_text_field"},
        ]
        if dims:
            metafields.append({"namespace": "recarpet", "key": "dimensions",             "value": dims,                      "type": "single_line_text_field"})
        if p["collection_name"]:
            metafields.append({"namespace": "recarpet", "key": "collection_name",        "value": p["collection_name"],       "type": "single_line_text_field"})
        if p["design_name"]:
            metafields.append({"namespace": "recarpet", "key": "design_name",            "value": p["design_name"],           "type": "single_line_text_field"})
        if p["colour_code"]:
            metafields.append({"namespace": "recarpet", "key": "colour_code",            "value": p["colour_code"],           "type": "single_line_text_field"})
        if p["colour_name"]:
            metafields.append({"namespace": "recarpet", "key": "colour_name",            "value": p["colour_name"],           "type": "single_line_text_field"})
        if p["installation_methods"]:
            metafields.append({"namespace": "recarpet", "key": "installation_methods",   "value": p["installation_methods"],  "type": "single_line_text_field"})
        if p["product_type_raw"]:
            metafields.append({"namespace": "recarpet", "key": "product_label",          "value": p["product_type_raw"],      "type": "single_line_text_field"})

        is_new = sku not in existing

        if args.dry_run:
            action = "CREATE" if is_new else "UPDATE"
            print(f"  [{action}] {sku}  {title}  price:{price:.2f} SEK  type:{product_type}")
            skipped += 1
            continue

        try:
            if is_new:
                product = create_product(title, brand, product_type, tags, price, sku, image_url, body_html)
                product_id = product["id"]
                variant_id = product["variants"][0]["id"]
                inv_item_id = product["variants"][0]["inventory_item_id"]

                set_inventory(inv_item_id, location_id, quantity)
                set_metafields(product_id, metafields)

                if sparklayer_pub_id:
                    publish_to_sparklayer(product_id, sparklayer_pub_id)

                if collection_id:
                    add_product_to_collection(product_id, collection_id)

                sync_log[sku] = {"product_id": product_id, "variant_id": variant_id, "inventory_item_id": inv_item_id}
                existing[sku] = sync_log[sku]

                pub_ok = "✓ SparkLayer" if sparklayer_pub_id else "– SparkLayer (ej konfigurerad)"
                col_ok = f"✓ {MILLIKEN_COLLECTION_HANDLE}" if collection_id else "– collection ej hittad"
                print(f"  CREATED  {sku} — {title}  [{pub_ok}] [{col_ok}]")
                created += 1
            else:
                info = existing[sku]
                update_product(
                    info["product_id"], info["variant_id"],
                    title, brand, product_type, tags, price, image_url, body_html
                )
                if info.get("inventory_item_id"):
                    set_inventory(info["inventory_item_id"], location_id, quantity)
                set_metafields(info["product_id"], metafields)

                if sparklayer_pub_id:
                    publish_to_sparklayer(info["product_id"], sparklayer_pub_id)
                if collection_id:
                    add_product_to_collection(info["product_id"], collection_id)

                print(f"  UPDATED  {sku} — {title}  price:{price:.2f}")
                updated += 1

        except Exception as e:
            print(f"  ERROR    {sku} — {title}: {e}")
            errors += 1

    save_sync_log(sync_log)

    print(f"\n{'='*60}")
    print(f"  Milliken Import Klar!")
    print(f"  Created: {created}  |  Updated: {updated}  |  Skipped: {skipped}  |  Errors: {errors}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
