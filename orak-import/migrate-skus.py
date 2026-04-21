"""
reCarpet — SKU Migration Script
================================
Byter SKU-prefix på alla Orak-produkter i Shopify:
  RC-ORAK-*  →  RCT-O-*

Usage:
    python migrate-skus.py --dry-run     # Visa vad som ändras (inga ändringar)
    python migrate-skus.py               # Kör migreringen på riktigt

Krav:
    pip install requests python-dotenv
"""

import os
import sys
import time
import requests
import re
import argparse
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION   = "2024-01"

OLD_PREFIX = "RC-ORAK-"
NEW_PREFIX = "RCT-O-"


def api_headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }


def rate_limit(response):
    if response.status_code == 429:
        wait = int(response.headers.get("Retry-After", 2))
        print(f"  Rate limited, waiting {wait}s...")
        time.sleep(wait)
    else:
        header = response.headers.get("X-Shopify-Shop-Api-Call-Limit", "")
        if header:
            used, total = map(int, header.split("/"))
            if used / total > 0.8:
                time.sleep(0.5)
        else:
            time.sleep(0.25)


def get_all_products():
    """Hämtar alla produkter med paginering."""
    print(f"Hämtar alla produkter från {SHOPIFY_SHOP}...")
    products = []
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/products.json?limit=250&fields=id,title,variants"
    while url:
        r = requests.get(url, headers=api_headers())
        rate_limit(r)
        r.raise_for_status()
        batch = r.json().get("products", [])
        products.extend(batch)
        # Paginering via Link header
        link = r.headers.get("Link", "")
        m = re.search(r'<([^>]+)>; rel="next"', link)
        url = m.group(1) if m else None
    print(f"  {len(products)} produkter hämtade\n")
    return products


def migrate_sku(old_sku):
    """Konverterar RC-ORAK-xxx till RCT-O-xxx."""
    if not old_sku:
        return None
    if old_sku.startswith(OLD_PREFIX):
        return NEW_PREFIX + old_sku[len(OLD_PREFIX):]
    return None


def update_variant_sku(variant_id, new_sku):
    """Uppdaterar SKU på en variant i Shopify."""
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/variants/{variant_id}.json"
    r = requests.put(url, headers=api_headers(), json={
        "variant": {"id": variant_id, "sku": new_sku}
    })
    rate_limit(r)
    r.raise_for_status()
    return r.json()


def main():
    parser = argparse.ArgumentParser(description="Migrate Orak SKUs: RC-ORAK-* → RCT-O-*")
    parser.add_argument("--dry-run", action="store_true", help="Visa ändringar utan att köra dem")
    args = parser.parse_args()

    if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
        print("Error: SHOPIFY_SHOP och SHOPIFY_TOKEN måste vara satta i .env")
        sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"\n{'='*50}")
    print(f"reCarpet — SKU Migration [{mode}]")
    print(f"  {OLD_PREFIX}*  →  {NEW_PREFIX}*")
    print(f"  Shopify: {SHOPIFY_SHOP}")
    print(f"{'='*50}\n")

    products = get_all_products()

    to_migrate = []
    for product in products:
        for variant in product.get("variants", []):
            old_sku = variant.get("sku", "")
            new_sku = migrate_sku(old_sku)
            if new_sku:
                to_migrate.append({
                    "product_id": product["id"],
                    "product_title": product["title"],
                    "variant_id": variant["id"],
                    "old_sku": old_sku,
                    "new_sku": new_sku,
                })

    print(f"Hittade {len(to_migrate)} produkter med {OLD_PREFIX}* SKU att migrera\n")

    if not to_migrate:
        print("Inget att migrera!")
        return

    # Visa förhandsvisning
    print(f"{'Gammal SKU':<35} → {'Ny SKU':<30} Produkt")
    print("-" * 90)
    for item in to_migrate[:10]:
        print(f"  {item['old_sku']:<33} → {item['new_sku']:<28} {item['product_title'][:40]}")
    if len(to_migrate) > 10:
        print(f"  ... och {len(to_migrate) - 10} till\n")

    if args.dry_run:
        print(f"\n[DRY-RUN] Inga ändringar gjorda. Kör utan --dry-run för att migrera.")
        return

    # Kör migreringen
    print(f"\nMigrerar {len(to_migrate)} SKUs...")
    migrated = errors = 0

    for i, item in enumerate(to_migrate, 1):
        try:
            update_variant_sku(item["variant_id"], item["new_sku"])
            print(f"  [{i}/{len(to_migrate)}] OK  {item['old_sku']} → {item['new_sku']}")
            migrated += 1
        except Exception as e:
            print(f"  [{i}/{len(to_migrate)}] ERROR  {item['old_sku']}: {e}")
            errors += 1

    print(f"""
{'='*50}
Migration klar!
  Migrerade: {migrated}
  Fel:       {errors}
  Totalt:    {len(to_migrate)}
{'='*50}

Nästa steg:
  1. Ladda upp nya SparkLayer-prislistor (sparklayer-pricelists/*.csv)
  2. Uppdatera Shopify Flow-villkor om de refererar gamla SKU-prefix
  3. Kör verify-skus.py för att verifiera matchning
""")


if __name__ == "__main__":
    main()
