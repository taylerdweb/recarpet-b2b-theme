"""
reCarpet — Test Environment Setup
===================================
Skapar en testmiljö med 15 produkter (5 Orak + 5 Milliken + 5 Composil).
Tar bort ALLA befintliga produkter först (utom tjänster).

Usage:
    python setup-test-env.py --dry-run    # Visa vad som händer
    python setup-test-env.py              # Kör på riktigt

Krav:
    pip install requests python-dotenv
"""

import os
import sys
import csv
import time
import json
import math
import re
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION   = "2024-01"

BASE_DIR       = Path(__file__).parent
SPARKLAYER_DIR = BASE_DIR.parent / "sparklayer-pricelists"
PRICELIST_EXCEL = BASE_DIR.parent / "reCarpet-pricelists-master.xlsx"

# Protected SKUs — never deleted
PROTECTED_SKUS = {"RC-SERVICE-MONTERING", "RC-SERVICE-RENGORING"}

# SparkLayer tier multipliers
TIER_MULTIPLIERS = {
    "utloggad": 1.00,
    "member":   1.00,
    "plus":     0.90,
    "premium":  0.90,
}

# Exchange rates (fallback)
RATES = {"EUR_SEK": 11.20, "EUR_NOK": 11.70, "EUR_DKK": 7.46}

COST_MARKUP = 1.40

# SparkLayer channel
SPARKLAYER_CHANNEL_NAME = "SparkLayer B2B & Wholesale"

def ceil_price(value, decimals=2):
    factor = 10 ** decimals
    return math.ceil(value * factor) / factor


# ─── Test Products ───────────────────────────────────────────────────────────

ORAK_PRODUCTS = [
    {"sku": "RCT-O-TEST001", "title": "Composure Diffuse 50x50", "brand": "Interface", "price_eur": 25.20, "qty": 90, "dims": "50x50 cm", "tags": "orak,atervunna-mattor,interface,reemploi"},
    {"sku": "RCT-O-TEST002", "title": "Heuga 727 Dark Orchid", "brand": "Interface", "price_eur": 16.80, "qty": 89, "dims": "50x50 cm", "tags": "orak,atervunna-mattor,interface,reemploi"},
    {"sku": "RCT-O-TEST003", "title": "On Line Cloud 25x100", "brand": "Interface", "price_eur": 28.00, "qty": 49, "dims": "25x100 cm", "tags": "orak,atervunna-mattor,interface,reemploi"},
    {"sku": "RCT-O-TEST004", "title": "Stoneage 160", "brand": "Balsan", "price_eur": 25.20, "qty": 68, "dims": "50x50 cm", "tags": "orak,atervunna-mattor,balsan,reemploi"},
    {"sku": "RCT-O-TEST005", "title": "Karma Sonic Confort 910", "brand": "Balsan", "price_eur": 10.50, "qty": 44, "dims": "50x50 cm", "tags": "orak,atervunna-mattor,balsan,reemploi"},
]

MILLIKEN_PRODUCTS = [
    {"sku": "MILLIKEN-TEST001", "title": "Colour Compositions Volume", "brand": "Milliken", "price_eur": 22.00, "qty": 9999, "dims": "50x50 cm", "tags": "milliken,nya-golv,carpet-tile"},
    {"sku": "MILLIKEN-TEST002", "title": "Freelay Eco Ash", "brand": "Milliken", "price_eur": 22.00, "qty": 9999, "dims": "50x50 cm", "tags": "milliken,nya-golv,carpet-tile"},
    {"sku": "MILLIKEN-TEST003", "title": "Crafted Series Woven Elm", "brand": "Milliken", "price_eur": 35.00, "qty": 9999, "dims": "50x50 cm", "tags": "milliken,nya-golv,woven-design-tile"},
    {"sku": "MILLIKEN-TEST004", "title": "Nordic Stories Fjord Blue", "brand": "Milliken", "price_eur": 30.00, "qty": 9999, "dims": "50x50 cm", "tags": "milliken,nya-golv,luxury-vinyl-tile"},
    {"sku": "MILLIKEN-TEST005", "title": "Consequence Acoustic Sterling", "brand": "Milliken", "price_eur": 22.00, "qty": 9999, "dims": "50x50 cm", "tags": "milliken,nya-golv,carpet-tile"},
]

COMPOSIL_PRODUCTS = [
    {"sku": "RCT-C-TEST001", "title": "EcoTile Classic Grey 500", "brand": "Composil", "price_eur": 18.50, "qty": 200, "dims": "50x50 cm", "tags": "composil,atervunna-mattor,reemploi"},
    {"sku": "RCT-C-TEST002", "title": "EcoTile Urban Charcoal", "brand": "Composil", "price_eur": 19.00, "qty": 150, "dims": "50x50 cm", "tags": "composil,atervunna-mattor,reemploi"},
    {"sku": "RCT-C-TEST003", "title": "EcoTile Nature Beige 320", "brand": "Composil", "price_eur": 17.50, "qty": 180, "dims": "50x50 cm", "tags": "composil,atervunna-mattor,reemploi"},
    {"sku": "RCT-C-TEST004", "title": "EcoTile Ocean Blue 410", "brand": "Composil", "price_eur": 20.00, "qty": 120, "dims": "50x50 cm", "tags": "composil,atervunna-mattor,reemploi"},
    {"sku": "RCT-C-TEST005", "title": "EcoTile Forest Green 550", "brand": "Composil", "price_eur": 21.00, "qty": 95, "dims": "50x50 cm", "tags": "composil,atervunna-mattor,reemploi"},
]

SERVICE_PRODUCTS = [
    {"sku": "RC-SERVICE-MONTERING", "sek_price": 45.00},
    {"sku": "RC-SERVICE-RENGORING", "sek_price": 30.00},
]

ALL_TEST_PRODUCTS = ORAK_PRODUCTS + MILLIKEN_PRODUCTS + COMPOSIL_PRODUCTS


# ─── Shopify API ─────────────────────────────────────────────────────────────

def api_headers():
    return {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}

def rate_limit(r):
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 2))
        print(f"  Rate limited, waiting {wait}s...")
        time.sleep(wait)
    else:
        header = r.headers.get("X-Shopify-Shop-Api-Call-Limit", "")
        if header:
            used, total = map(int, header.split("/"))
            if used / total > 0.8:
                time.sleep(0.5)
        else:
            time.sleep(0.25)

def shopify_get(endpoint, params=None):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.get(url, headers=api_headers(), params=params)
    rate_limit(r)
    r.raise_for_status()
    return r.json()

def shopify_post(endpoint, payload):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.post(url, headers=api_headers(), json=payload)
    rate_limit(r)
    r.raise_for_status()
    return r.json()

def shopify_put(endpoint, payload):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.put(url, headers=api_headers(), json=payload)
    rate_limit(r)
    r.raise_for_status()
    return r.json()

def graphql(query, variables=None):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/graphql.json"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(url, headers=api_headers(), json=payload)
    rate_limit(r)
    r.raise_for_status()
    return r.json()

def get_sparklayer_publication_gid():
    query = """query { publications(first: 20) { edges { node { id name } } } }"""
    try:
        result = graphql(query)
        edges = (result.get("data") or {}).get("publications", {}).get("edges", [])
        for edge in edges:
            if SPARKLAYER_CHANNEL_NAME.lower() in edge["node"]["name"].lower():
                return edge["node"]["id"]
    except Exception as e:
        print(f"  Warning: SparkLayer GID ej hittad: {e}")
    return None

def publish_to_sparklayer(product_id, publication_gid):
    mutation = """
    mutation publishablePublish($id: ID!, $input: [PublicationInput!]!) {
      publishablePublish(id: $id, input: $input) { userErrors { field message } }
    }"""
    graphql(mutation, {"id": f"gid://shopify/Product/{product_id}", "input": [{"publicationId": publication_gid}]})


# ─── Delete all products ─────────────────────────────────────────────────────

def count_products():
    """Quick count of all products in the store."""
    data = shopify_get("products/count.json")
    return data.get("count", 0)


def fetch_product_batch(limit=250):
    """Fetch one batch of products (oldest first)."""
    data = shopify_get("products.json", {"limit": limit, "fields": "id,title,variants"})
    return data.get("products", [])


def delete_all_products(dry_run=False):
    total = count_products()
    print(f"\n  Totalt i butiken: {total} produkter")

    if dry_run:
        # In dry-run, just show what would be deleted
        all_products = []
        params = {"limit": 250, "fields": "id,title,variants"}
        while True:
            data = shopify_get("products.json", params)
            products = data.get("products", [])
            if not products:
                break
            all_products.extend(products)
            if len(products) < 250:
                break
            params["since_id"] = products[-1]["id"]

        protected = sum(1 for p in all_products
                        if any(v.get("sku", "") in PROTECTED_SKUS for v in p.get("variants", [])))
        print(f"  Ska tas bort: {len(all_products) - protected}")
        print(f"  Skyddade (tjänster): {protected}")
        print("  [DRY-RUN] Inga produkter togs bort.")
        return

    # Live mode: keep fetching + deleting until only protected remain
    deleted = errors = 0
    round_num = 0
    while True:
        round_num += 1
        batch = fetch_product_batch(250)
        if not batch:
            break

        # Filter out protected products
        to_delete = []
        for p in batch:
            skus = [v.get("sku", "") for v in p.get("variants", [])]
            if any(s in PROTECTED_SKUS for s in skus):
                continue
            to_delete.append(p)

        if not to_delete:
            # Only protected products left
            break

        print(f"  Omgång {round_num}: raderar {len(to_delete)} produkter...")
        for p in to_delete:
            try:
                url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/products/{p['id']}.json"
                r = requests.delete(url, headers=api_headers())
                rate_limit(r)
                if r.status_code in (200, 204):
                    deleted += 1
                else:
                    print(f"    WARN: {p['title']} → HTTP {r.status_code}")
                    errors += 1
            except Exception as e:
                print(f"    ERROR: {p['title']} → {e}")
                errors += 1

        # Brief pause between rounds to let Shopify catch up
        time.sleep(1)

    # Verification
    remaining = count_products()
    print(f"\n  Borttagna: {deleted}, Fel: {errors}")
    print(f"  Kvar i butiken: {remaining} produkter (ska vara ~{len(PROTECTED_SKUS)} tjänster)")
    if remaining > len(PROTECTED_SKUS) + 1:
        print("  ⚠  Fler produkter kvar än väntat — kör scriptet igen om det behövs.")


# ─── Create test products ────────────────────────────────────────────────────

def create_test_products(dry_run=False):
    print(f"\n  Skapar {len(ALL_TEST_PRODUCTS)} testprodukter...")

    location_id = shopify_get("locations.json")["locations"][0]["id"] if not dry_run else None
    sparklayer_gid = get_sparklayer_publication_gid() if not dry_run else None

    created = errors = 0
    for p in ALL_TEST_PRODUCTS:
        sek_price = ceil_price(p["price_eur"] * COST_MARKUP * RATES["EUR_SEK"])
        supplier = p["sku"].split("-")[0] + "-" + p["sku"].split("-")[1]

        if dry_run:
            print(f"  [DRY-RUN] CREATE  {p['sku']}  {p['title']}  SEK {sek_price:.2f}  qty:{p['qty']}")
            continue

        try:
            product_type = "Carpet Tile"
            payload = {
                "product": {
                    "title": p["title"],
                    "vendor": p["brand"],
                    "product_type": product_type,
                    "tags": p["tags"],
                    "published": True,
                    "variants": [{
                        "sku": p["sku"],
                        "price": f"{sek_price:.2f}",
                        "inventory_management": "shopify",
                        "requires_shipping": False,
                        "taxable": True,
                    }],
                }
            }
            result = shopify_post("products.json", payload)["product"]
            product_id = result["id"]
            variant = result["variants"][0]

            # Set inventory
            shopify_post("inventory_levels/set.json", {
                "location_id": location_id,
                "inventory_item_id": variant["inventory_item_id"],
                "available": p["qty"],
            })

            # Set metafields
            metafields = [
                {"namespace": "recarpet", "key": "dimensions", "value": p["dims"], "type": "single_line_text_field"},
            ]
            for mf in metafields:
                try:
                    shopify_post(f"products/{product_id}/metafields.json", {"metafield": mf})
                except:
                    pass

            # Publish to SparkLayer
            if sparklayer_gid:
                publish_to_sparklayer(product_id, sparklayer_gid)

            print(f"  CREATED  {p['sku']}  {p['title']}  SEK {sek_price:.2f}  qty:{p['qty']}")
            created += 1

        except Exception as e:
            print(f"  ERROR  {p['sku']}: {e}")
            errors += 1

    print(f"\n  Skapade: {created}, Fel: {errors}")


# ─── Generate pricelists ─────────────────────────────────────────────────────

def generate_pricelists():
    print("\n  Genererar SparkLayer-prislistor...")
    SPARKLAYER_DIR.mkdir(exist_ok=True)

    CURRENCY_RATES = {
        "sek": RATES["EUR_SEK"],
        "nok": RATES["EUR_NOK"],
        "dkk": RATES["EUR_DKK"],
        "eur": 1.0,
    }

    LISTS = {
        f"sparklayer-{tier}-{cur}.csv": (mult, CURRENCY_RATES[cur])
        for tier, mult in TIER_MULTIPLIERS.items()
        for cur in CURRENCY_RATES
    }

    list_rows = {name: [] for name in LISTS}

    # Add test products
    for p in ALL_TEST_PRODUCTS:
        eur_price = p["price_eur"]
        for name, (mult, rate) in LISTS.items():
            price = ceil_price(eur_price * COST_MARKUP * rate * mult)
            list_rows[name].append([p["sku"], 1, f"{price:.2f}"])

    # Add service products
    for sp in SERVICE_PRODUCTS:
        sek_price = sp["sek_price"]
        for name, (mult, rate) in LISTS.items():
            if rate == 1.0:  # EUR
                svc_price = ceil_price(sek_price / RATES["EUR_SEK"])
            elif rate == RATES["EUR_NOK"]:
                svc_price = ceil_price(sek_price * (RATES["EUR_NOK"] / RATES["EUR_SEK"]))
            elif rate == RATES["EUR_DKK"]:
                svc_price = ceil_price(sek_price * (RATES["EUR_DKK"] / RATES["EUR_SEK"]))
            else:
                svc_price = sek_price
            list_rows[name].append([sp["sku"], 1, f"{svc_price:.2f}"])

    for name, rows in list_rows.items():
        path = SPARKLAYER_DIR / name
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sku", "quantity", "price"])
            writer.writerows(rows)
        print(f"  OK  {name}  ({len(rows)} SKUs)")

    # Bulk upload CSV
    bulk_path = SPARKLAYER_DIR / "sparklayer-bulk-upload.csv"
    with open(bulk_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SKU", "PRICE", "PRICE_LIST_SLUG"])
        for p in ALL_TEST_PRODUCTS:
            for tier, mult in TIER_MULTIPLIERS.items():
                for cur, rate in CURRENCY_RATES.items():
                    price = ceil_price(p["price_eur"] * COST_MARKUP * rate * mult)
                    writer.writerow([p["sku"], price, f"{tier}-{cur}"])
        for sp in SERVICE_PRODUCTS:
            sek_price = sp["sek_price"]
            for tier in TIER_MULTIPLIERS:
                for cur, rate in CURRENCY_RATES.items():
                    if rate == 1.0:
                        svc_price = ceil_price(sek_price / RATES["EUR_SEK"])
                    elif rate == RATES["EUR_NOK"]:
                        svc_price = ceil_price(sek_price * (RATES["EUR_NOK"] / RATES["EUR_SEK"]))
                    elif rate == RATES["EUR_DKK"]:
                        svc_price = ceil_price(sek_price * (RATES["EUR_DKK"] / RATES["EUR_SEK"]))
                    else:
                        svc_price = sek_price
                    writer.writerow([sp["sku"], svc_price, f"{tier}-{cur}"])

    total_rows = (len(ALL_TEST_PRODUCTS) + len(SERVICE_PRODUCTS)) * len(LISTS)
    print(f"  OK  sparklayer-bulk-upload.csv  ({total_rows} rader)")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="reCarpet — Setup Test Environment")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without changes")
    args = parser.parse_args()

    if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
        print("Error: set SHOPIFY_SHOP and SHOPIFY_TOKEN in .env")
        sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"""
{'='*55}
reCarpet — Test Environment Setup [{mode}]
  Shop: {SHOPIFY_SHOP}
  Products: 5 Orak + 5 Milliken + 5 Composil = 15
  SKU prefixes: RCT-O- / MILLIKEN- / RCT-C-
{'='*55}
""")

    # Step 1: Delete all products
    print("STEG 1: Ta bort alla befintliga produkter")
    if not args.dry_run:
        print("  (Väntar 5s — Ctrl+C för att avbryta)")
        time.sleep(5)
    delete_all_products(dry_run=args.dry_run)

    # Step 2: Create test products
    print("\nSTEG 2: Skapa testprodukter")
    create_test_products(dry_run=args.dry_run)

    # Step 3: Generate pricelists
    print("\nSTEG 3: Generera SparkLayer-prislistor")
    generate_pricelists()

    print(f"""
{'='*55}
Klart!

Nästa steg:
  1. Ladda upp prislistor i SparkLayer → Price Lists
     (sparklayer-pricelists/*.csv)
  2. Testa att lägga en order med Orak-produkt (RCT-O-*)
     → ska trigga b2b_supplier_order_orak i Shopify Flow
  3. Testa Composil-order (RCT-C-*)
     → ska trigga b2b_supplier_order_composil
{'='*55}
""")


if __name__ == "__main__":
    main()
