"""
reCarpet — Setup Service Products
===================================
Skapar tjänsteprodukter (Montering, Rengöring) och Tjänster-kollektionen i Shopify.
Kör en gång — scriptet kontrollerar om produkterna redan finns via SKU.

Usage:
    python3 setup-services.py
    python3 setup-services.py --dry-run
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION   = "2024-01"

# ─── Tjänsteprodukter ─────────────────────────────────────────────────────────

SERVICE_PRODUCTS = [
    {
        "title": "Montering av mattplattor",
        "sku": "RC-SERVICE-MONTERING",
        "price": "45.00",
        "vendor": "reCarpet",
        "product_type": "Tjänst",
        "tags": "b2b, b2b-only, tjanster, montering",
        "body_html": "<p>Professionell montering av mattplattor. Pris per m². "
                     "Läggs till automatiskt vid produktköp om montering valts.</p>",
    },
    {
        "title": "Rengöring av mattplattor",
        "sku": "RC-SERVICE-RENGORING",
        "price": "30.00",
        "vendor": "reCarpet",
        "product_type": "Tjänst",
        "tags": "b2b, b2b-only, tjanster, rengoring",
        "body_html": "<p>Professionell rengöring av begagnade mattplattor. Pris per m².</p>",
    },
]

COLLECTION_TITLE = "Tjänster"

# ─── API helpers ──────────────────────────────────────────────────────────────

def api_headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }

def shopify_get(endpoint, params=None):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.get(url, headers=api_headers(), params=params)
    time.sleep(0.3)
    r.raise_for_status()
    return r.json()

def shopify_post(endpoint, payload):
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/{endpoint}"
    r = requests.post(url, headers=api_headers(), json=payload)
    time.sleep(0.3)
    r.raise_for_status()
    return r.json()


def get_existing_skus() -> dict:
    """Returnerar {sku: {product_id, variant_id}}"""
    sku_map = {}
    data = shopify_get("products.json", {"limit": 250, "fields": "id,variants"})
    for p in data.get("products", []):
        for v in p.get("variants", []):
            if v.get("sku"):
                sku_map[v["sku"]] = {"product_id": p["id"], "variant_id": v["id"]}
    return sku_map


def find_or_create_collection(title: str, dry_run: bool) -> int | None:
    """Hittar eller skapar en custom collection."""
    data = shopify_get("custom_collections.json", {"limit": 250, "fields": "id,title"})
    for col in data.get("custom_collections", []):
        if col["title"].lower() == title.lower():
            print(f"  Collection '{title}' finns redan (id: {col['id']})")
            return col["id"]

    if dry_run:
        print(f"  [DRY-RUN] Skulle skapa collection '{title}'")
        return None

    result = shopify_post("custom_collections.json", {
        "custom_collection": {"title": title}
    })
    col_id = result["custom_collection"]["id"]
    print(f"  Collection '{title}' skapad (id: {col_id})")
    return col_id


def create_product(product_data: dict) -> dict:
    return shopify_post("products.json", {
        "product": {
            "title": product_data["title"],
            "vendor": product_data["vendor"],
            "product_type": product_data["product_type"],
            "tags": product_data["tags"],
            "body_html": product_data["body_html"],
            "published": True,
            "variants": [{
                "sku": product_data["sku"],
                "price": product_data["price"],
                "inventory_management": None,  # Tjänster har inget lager
                "requires_shipping": False,
                "taxable": True,
            }],
        }
    })["product"]


def add_to_collection(product_id: int, collection_id: int):
    try:
        shopify_post("collects.json", {
            "collect": {"product_id": product_id, "collection_id": collection_id}
        })
    except Exception as e:
        if "422" not in str(e):
            print(f"    Warning: collection-tilldelning misslyckades: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="reCarpet - Setup Service Products")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
        print("Error: set SHOPIFY_SHOP and SHOPIFY_TOKEN in .env")
        sys.exit(1)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"\nreCarpet — Setup Services [{mode}]")
    print(f"  Shop: {SHOPIFY_SHOP}\n")

    # Hämta befintliga SKUs
    existing = get_existing_skus()
    print(f"  {len(existing)} befintliga produkter\n")

    # Skapa / hitta collection
    collection_id = find_or_create_collection(COLLECTION_TITLE, args.dry_run)

    # Skapa tjänsteprodukter
    created_products = []
    for sp in SERVICE_PRODUCTS:
        if sp["sku"] in existing:
            info = existing[sp["sku"]]
            print(f"  EXISTS  {sp['sku']} — {sp['title']} (product_id: {info['product_id']})")
            created_products.append({"sku": sp["sku"], "product_id": info["product_id"], "variant_id": info["variant_id"]})
            continue

        if args.dry_run:
            print(f"  [DRY-RUN] Skulle skapa: {sp['sku']} — {sp['title']} ({sp['price']} kr/m²)")
            continue

        product = create_product(sp)
        product_id = product["id"]
        variant_id = product["variants"][0]["id"]
        print(f"  CREATED {sp['sku']} — {sp['title']} (product_id: {product_id}, variant_id: {variant_id})")
        created_products.append({"sku": sp["sku"], "product_id": product_id, "variant_id": variant_id})

        # Lägg till i Tjänster-collection
        if collection_id:
            add_to_collection(product_id, collection_id)
            print(f"          → Tillagd i '{COLLECTION_TITLE}'")

    # Skriv ut variant-IDs (behövs i theme.liquid för montering-hookup)
    print(f"\n{'='*60}")
    print("Spara dessa variant-IDs — de behövs i theme.liquid:")
    for p in created_products:
        print(f"  {p['sku']}: variant_id = {p.get('variant_id', '?')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
