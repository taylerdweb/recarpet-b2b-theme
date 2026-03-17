# reCarpet — ORAK Import

Synkar ORAKs CSV-export direkt mot Shopify via API.
Skapar/uppdaterar produkter, publicerar till SparkLayer B2B-kanal och lägger in produkterna i rätt serie.

---

## Förberedelse (en gång)

### 1. Installera beroenden
```bash
pip3 install pandas requests python-dotenv
```

### 2. Skapa .env-fil
Skapa en fil som heter `.env` i mappen `orak-import/` med följande innehåll:
```
SHOPIFY_SHOP=recarpet.myshopify.com
SHOPIFY_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxx
```

**Hämta token:**
Shopify Admin → Settings → Apps → Develop apps → Create an app
→ Configuration → scopes: `write_products`, `write_inventory`, `read_publications`
→ Install app → kopiera "Admin API access token"

### 3. Kontrollera collection-handle
Scriptet lägger alla produkter i "Återbrukade mattor". Verifiera att handlen stämmer:
Shopify Admin → Collections → klicka "Återbrukade mattor" → scrolla ner till "Sökmotor-lista"
→ notera URL-handlen (t.ex. `atervunna-mattor` eller `mattor`)

Om handlen är annorlunda, öppna `import-orak.py` och ändra rad:
```python
ATERVUNNA_HANDLE = "atervunna-mattor"   # ← ändra till rätt handle om nödvändigt
```

---

## Köra scriptet

### Torrkörning (se vad som händer utan att skriva något)
```bash
cd orak-import
python3 import-orak.py --csv "Produits Mars 2026 - orak.csv" --dry-run
```
Perfekt att köra först för att verifiera att allt ser rätt ut.

### Skarp körning (skriver till Shopify)
```bash
cd orak-import
python3 import-orak.py --csv "Produits Mars 2026 - orak.csv"
```

### Generera SparkLayer-prislistor utan att ladda upp produkter
```bash
python3 import-orak.py --csv "Produits Mars 2026 - orak.csv" --pricelists-only
```

---

## Vad scriptet gör vid körning

För varje produkt i CSV:n:

1. **Skapar** produkten om SKU:n inte finns sedan tidigare
   — eller **uppdaterar** pris och lagersaldo om den redan finns

2. **Publicerar** produkten till SparkLayer B2B & Wholesale-kanalen automatiskt

3. **Lägger in** produkten i "Återbrukade mattor"-collection

4. **Taggar:**
   - Alla produkter: `b2b`, `b2b-only`, `orak`, `atervunna-mattor`, varumärket
   - Produkter av typen "Produit à venir" (väntar på rengöring): + `kommande`

5. **Genererar** uppdaterade SparkLayer-prislistor i `../sparklayer-pricelists/`

---

## Produkttyper från ORAK → Shopify

| ORAK-etikett | Shopify-collection | Extra tagg |
|---|---|---|
| Réemploi | Återbrukade mattor | – |
| Fin de série | Återbrukade mattor | – |
| Produit à venir | Återbrukade mattor | `kommande` |

---

## Felsökning

| Symptom | Lösning |
|---|---|
| `ModuleNotFoundError` | Kör `pip install pandas requests python-dotenv` |
| `Error: set SHOPIFY_SHOP and SHOPIFY_TOKEN` | Skapa `.env`-filen enligt steg 2 ovan |
| `– SparkLayer (ej konfigurerad)` i loggen | Kontrollera att kanalens namn i Shopify är exakt "SparkLayer B2B & Wholesale" |
| `– atervunna-mattor (collection saknas)` | Kontrollera handle enligt steg 3 ovan — ändra `ATERVUNNA_HANDLE` i scriptet |
| Produkt skapas men hamnar inte i collection | Kör scriptet igen — collection-tilldelning är idempotent (skadas inte av att köras igen) |

---

## Efter körning

- Ladda upp de genererade prislistorna i SparkLayer Admin:
  `../sparklayer-pricelists/sparklayer-member-sek.csv`
  `../sparklayer-pricelists/sparklayer-entrepreneur-sek.csv`

- Loggfil sparas i `output/sync-log.json` — innehåller Shopify product/variant-ID per SKU
