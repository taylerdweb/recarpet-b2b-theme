"""
reCarpet — Shopify Meta Field Definitions Setup
================================================
Kör detta EN GÅNG för att skapa alla meta field definitions i Shopify.
Efteråt kan import-orak.py sätta värden på dessa fält per produkt.

Usage:
    python setup-metafields.py

Krav: .env med SHOPIFY_SHOP och SHOPIFY_TOKEN
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_SHOP  = os.getenv("SHOPIFY_SHOP")   # t.ex. recarpet.myshopify.com
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION   = "2024-01"

# ─── Meta field definitions ───────────────────────────────────────────────────
# These are created under namespace "recarpet" on the product owner type.
# "name" = display label in Shopify Admin
# "key"  = used in Liquid: product.metafields.recarpet.<key>
# "type" = Shopify metafield type

METAFIELD_DEFINITIONS = [
    # ── From ORAK CSV ─────────────────────────────────────────────────────────
    {
        "name": "Dimensions / Format",
        "namespace": "recarpet",
        "key": "dimensions",
        "type": "single_line_text_field",
        "description": "Tile size, e.g. 50x50 cm",
    },
    {
        "name": "Technical Sheet URL",
        "namespace": "recarpet",
        "key": "technical_sheet_url",
        "type": "url",
        "description": "Link to PDF technical sheet",
    },
    {
        "name": "Product Label",
        "namespace": "recarpet",
        "key": "product_label",
        "type": "single_line_text_field",
        "description": "e.g. Réemploi, Fin de série, Produit à venir",
    },
    # ── Extended specs (populated later) ─────────────────────────────────────
    {
        "name": "Backing / Sous-couche",
        "namespace": "recarpet",
        "key": "backing",
        "type": "single_line_text_field",
        "description": "Tile backing type, e.g. Ecodesigned",
    },
    {
        "name": "Thickness / Épaisseur",
        "namespace": "recarpet",
        "key": "thickness",
        "type": "single_line_text_field",
        "description": "Total thickness, e.g. 6 mm",
    },
    {
        "name": "Fire Rating / Classement feu",
        "namespace": "recarpet",
        "key": "fire_rating",
        "type": "single_line_text_field",
        "description": "e.g. Bfl S1",
    },
    {
        "name": "Acoustic Rating / Isolation phonique",
        "namespace": "recarpet",
        "key": "acoustic_rating",
        "type": "single_line_text_field",
        "description": "e.g. ΔLw: 23 dB",
    },
    {
        "name": "Impact Absorption",
        "namespace": "recarpet",
        "key": "impact_absorption",
        "type": "single_line_text_field",
        "description": "e.g. α: 0.2",
    },
    {
        "name": "LRV",
        "namespace": "recarpet",
        "key": "lrv",
        "type": "single_line_text_field",
        "description": "Light Reflectance Value, e.g. L: 37.3 - Y: 9.7",
    },
    {
        "name": "Minimum Order",
        "namespace": "recarpet",
        "key": "min_order",
        "type": "single_line_text_field",
        "description": "Minimum order quantity, e.g. 5 m²",
    },
    {
        "name": "Delivery Days",
        "namespace": "recarpet",
        "key": "delivery_days",
        "type": "number_integer",
        "description": "Lead time in days, e.g. 15",
    },
    {
        "name": "Installation Service",
        "namespace": "recarpet",
        "key": "pose_service",
        "type": "single_line_text_field",
        "description": "Optional / Included / Not available",
    },
    {
        "name": "Maintenance Service",
        "namespace": "recarpet",
        "key": "maintenance_service",
        "type": "single_line_text_field",
        "description": "Optional / Included / Not available",
    },
]


def headers():
    return {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    }


def get_existing_definitions() -> set:
    """Return set of existing (namespace, key) tuples."""
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/metafield_definitions.json"
    existing = set()
    params = {"owner_type": "PRODUCT", "limit": 250}
    r = requests.get(url, headers=headers(), params=params)
    if r.status_code == 200:
        for d in r.json().get("metafield_definitions", []):
            existing.add((d["namespace"], d["key"]))
    return existing


def create_definition(definition: dict) -> bool:
    """Create a single metafield definition via GraphQL (required for definitions)."""
    url = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}/graphql.json"

    query = """
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
          id
          name
          namespace
          key
          type { name }
        }
        userErrors {
          field
          message
          code
        }
      }
    }
    """

    variables = {
        "definition": {
            "name": definition["name"],
            "namespace": definition["namespace"],
            "key": definition["key"],
            "type": definition["type"],
            "ownerType": "PRODUCT",
            "description": definition.get("description", ""),
        }
    }

    r = requests.post(url, headers=headers(), json={"query": query, "variables": variables})
    r.raise_for_status()
    data = r.json()

    errors = data.get("data", {}).get("metafieldDefinitionCreate", {}).get("userErrors", [])
    if errors:
        for e in errors:
            # CODE: TAKEN = already exists under a different definition type (ok to skip)
            if e.get("code") == "TAKEN":
                return True  # already exists, that's fine
            print(f"    ⚠ {e['field']}: {e['message']}")
        return False

    created = data.get("data", {}).get("metafieldDefinitionCreate", {}).get("createdDefinition")
    return created is not None


def main():
    if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
        print("✗ Sätt SHOPIFY_SHOP och SHOPIFY_TOKEN i .env")
        return

    print(f"\n🔧 reCarpet — Meta Field Setup")
    print(f"   Butik: {SHOPIFY_SHOP}")
    print(f"   Definitions att skapa: {len(METAFIELD_DEFINITIONS)}\n")

    existing = get_existing_definitions()
    print(f"   Befintliga definitions: {len(existing)}\n")

    created_count = 0
    skipped_count = 0

    for d in METAFIELD_DEFINITIONS:
        key = (d["namespace"], d["key"])
        if key in existing:
            print(f"  ↩  {d['namespace']}.{d['key']} — finns redan")
            skipped_count += 1
            continue

        success = create_definition(d)
        if success:
            print(f"  ✅ Skapade: {d['namespace']}.{d['key']} ({d['type']})")
            created_count += 1
        else:
            print(f"  ✗  Misslyckades: {d['namespace']}.{d['key']}")

        time.sleep(0.3)  # Respektera rate limit

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅  Klart
    Skapade:  {created_count}
    Hoppade:  {skipped_count}

Nästa steg: python import-orak.py --csv ../../../uploads/Produits\ Mars\ 2026\ -\ orak.csv
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    main()
