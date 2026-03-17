"""
Verifierar att SKUs i Shopify matchar SKUs i SparkLayer-prislistorna.
Kör: python3 verify-skus.py
"""
import requests, pandas as pd, os, re
from dotenv import load_dotenv
load_dotenv()

SHOP  = os.getenv("SHOPIFY_SHOP")
TOKEN = os.getenv("SHOPIFY_TOKEN")
headers = {"X-Shopify-Access-Token": TOKEN}

print(f"Hämtar produkter från {SHOP}...")
all_skus = {}
url = f"https://{SHOP}/admin/api/2024-01/products.json?limit=250&fields=id,title,variants"
while url:
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for p in r.json()["products"]:
        for v in p["variants"]:
            if v.get("sku"):
                all_skus[v["sku"].strip()] = p["title"]
    link = r.headers.get("Link", "")
    m = re.search(r'<([^>]+)>; rel="next"', link)
    url = m.group(1) if m else None

print(f"Shopify: {len(all_skus)} produkter\n")

base = os.path.dirname(os.path.abspath(__file__))
pricelist_path = os.path.join(base, "..", "sparklayer-pricelists", "sparklayer-member-sek.csv")
df = pd.read_csv(pricelist_path)
pricelist_skus = set(df["sku"].astype(str).str.strip())
shopify_set    = set(all_skus.keys())

in_both       = shopify_set & pricelist_skus
only_shopify  = shopify_set - pricelist_skus
only_price    = pricelist_skus - shopify_set

print(f"Matchar:                    {len(in_both)}")
print(f"I Shopify men EJ pricelist: {len(only_shopify)}")
print(f"I pricelist men EJ Shopify: {len(only_price)}")

if only_shopify:
    print(f"\n⚠ Shopify-SKUs som SAKNAS i pricelist (dessa får inget SparkLayer-pris):")
    for sku in sorted(only_shopify):
        print(f"  '{sku}'  →  {all_skus[sku]}")
