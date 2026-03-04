# reCarpet — Orak Import

Skript som omvandlar Oraks produktexport till en Shopify-klar importfil.

---

## Mapstruktur

```
orak-import/
├── import-orak.py          ← Huvudskript
├── product-specs.xlsx      ← Tekniska specs per modell (reCarpet underhåller)
├── .env                    ← Shopify-credentials (skapa från .env.example)
├── sample-delivery/        ← Exempelleverans från Orak
│   ├── stock.xlsx          ← Oraks standardexport (oförändrad)
│   ├── prices.csv          ← Prislista från Orak
│   └── photos/             ← Bilder namngivna efter GIZ-nummer
└── output/
    ├── shopify-import.csv  ← Genererad fil — ladda upp i Shopify
    └── image-upload-log.json
```

---

## Vad Orak skickar varje gång

| Fil | Format | Beskrivning |
|-----|--------|-------------|
| `stock.xlsx` | Excel | Deras befintliga export (oförändrad) |
| `prices.csv` | CSV | Två kolumner: `giz_id` och `price_per_sqm` |
| `photos/` | Mapp | JPG/PNG namngivna efter GIZ-nummer |

### prices.csv format
```
giz_id,price_per_sqm
GIZ2202010,299.00
GIZ2203001,249.00
```

### Bildnamngivning
```
GIZ2202010.jpg      ← huvudbild (obligatorisk)
GIZ2202010_2.jpg    ← extrabild (valfri)
GIZ2202010_3.jpg    ← extrabild (valfri)
```

---

## Installation (en gång)

```bash
pip install openpyxl pandas requests python-dotenv
```

---

## Användning

### Utan bilduppladdning (snabbt)
```bash
python import-orak.py --delivery namn-pa-leveransmapp
```
Bilder hanteras manuellt i Shopify admin efteråt.

### Med automatisk bilduppladdning (rekommenderat)
```bash
python import-orak.py --delivery namn-pa-leveransmapp --upload-images
```
Bilder laddas upp till Shopify CDN automatiskt. Kräver `.env`-fil med API-credentials.

---

## Konfigurera Shopify API (för bilduppladdning)

1. Kopiera `.env.example` → `.env`
2. Gå till Shopify Admin → **Settings → Apps → Develop apps**
3. Klicka **Create an app** → ge den ett namn (t.ex. "reCarpet Import")
4. Gå till **Configuration** → lägg till scope: `write_products`, `write_files`
5. Klicka **Install app** → kopiera **Admin API access token**
6. Klistra in token i `.env`

---

## Månatlig arbetsflöde

1. Orak skickar: `stock.xlsx` + `prices.csv` + mapp med bilder
2. Lägg filerna i en ny mapp, t.ex. `leverans-2026-04/`
3. Kör skriptet:
   ```bash
   python import-orak.py --delivery leverans-2026-04 --upload-images
   ```
4. Öppna Shopify Admin → **Produkter → Importera**
5. Välj `output/shopify-import.csv` → Importera
6. Produkter som inte längre finns i exporten får lager = 0 automatiskt

---

## product-specs.xlsx — underhåll

Filen innehåller tekniska specs per modell (Interface Composure, Balsan Stoneage etc).
Specs är samma för alla lot av samma modell och behöver **bara uppdateras när en ny modell dyker upp**.

- Kolumnerna C–L är de du fyller i
- MARQUE + MODELE måste matcha exakt vad Orak skriver i sin export
- Lämna tomt om du inte har informationen — det är OK

---

## Felsökning

| Problem | Lösning |
|---------|---------|
| `ModuleNotFoundError` | Kör `pip install openpyxl pandas requests python-dotenv` |
| Pris saknas för produkt | Lägg till GIZ-numret i `prices.csv` |
| Spec saknas för modell | Lägg till raden i `product-specs.xlsx` |
| Bild laddas inte upp | Kontrollera `.env` och att bildnamnet börjar med GIZ-numret |
