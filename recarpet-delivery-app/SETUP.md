# ReCarpet Leveransdatum — Shopify Admin App

## Vad appen gör

En embedded Shopify admin-app som låter ReCarpet bekräfta leveransdatum per artikel
på orderutkast och ordrar. Kunden ser sedan bekräftade datum.

### Flödet:
1. **Kund** väljer önskat leveransdatum i SparkLayer checkout → sparas i order notes
2. **ReCarpet** öppnar orderutkastet i Shopify admin → ser kundens önskade datum
3. **ReCarpet** sätter bekräftat leveransdatum per artikel via admin block
4. **Kund** ser bekräftade datum (via kontosida eller orderbekräftelse-mail)

## Struktur

```
recarpet-delivery-app/
├── app/                            # Remix app (backend + admin UI)
│   ├── routes/
│   │   ├── app._index.jsx          # Översikt: alla orderutkast med leveransstatus
│   │   ├── app.order.$id.jsx       # Ordervy: datepicker per line item
│   │   ├── api.proxy.*.jsx         # App Proxy: endpoint för kundsidan
│   │   ├── auth.*.jsx              # Shopify OAuth
│   │   └── app.jsx                 # Layout med Polaris
│   ├── shopify.server.js           # Shopify API-konfiguration
│   └── db.server.js                # Prisma/SQLite session storage
├── extensions/
│   └── delivery-dates/             # Admin UI Extension
│       └── src/
│           ├── BlockExtension.jsx        # Block i orderutkast-vyn
│           └── OrderBlockExtension.jsx   # Block i order-vyn
├── prisma/
│   └── schema.prisma               # Session-lagring
├── shopify.app.toml                # App-konfiguration
└── package.json
```

## Setup (steg för steg)

### 1. Förberedelser
```bash
# Kräver Node.js 18+
node --version

# Installera Shopify CLI (om det saknas)
npm install -g @shopify/cli
```

### 2. Skapa appen i Partners Dashboard
1. Gå till https://partners.shopify.com
2. Apps → Create app → "Create app manually"
3. Namn: "ReCarpet Leveransdatum"
4. Kopiera Client ID och Client Secret

### 3. Konfigurera & installera
```bash
cd recarpet-delivery-app

# Installera dependencies
npm install

# Länka till din Shopify Partners-app
shopify app config link

# Sätt upp databasen
npx prisma generate
npx prisma migrate dev --name init

# Starta dev-servern
shopify app dev
```

Shopify CLI skapar automatiskt en tunnel och konfigurerar OAuth.

### 4. Ändra metafield-typ
I Shopify Admin → Settings → Metafält → Ordrar:
- Om du redan har "Leveransdatum" som Datum-typ: **ta bort den**
- Skapa ny definition:
  - Namn: `Bekräftade leveransdatum`
  - Namespace/key: `custom.confirmed_delivery_dates`
  - Typ: **JSON**

### 5. Gör samma för Orderutkast
- Gå till Settings → Metafält → Orderutkast
- Skapa samma definition:
  - Namn: `Bekräftade leveransdatum`
  - Namespace/key: `custom.confirmed_delivery_dates`
  - Typ: **JSON**

### 6. Deploya
```bash
shopify app deploy
```

### 7. Installera på butiken
```bash
# Öppna installationslänken
shopify app dev --store recarpet-b2b.myshopify.com
```

## Data-format (JSON metafield)

```json
{
  "updated_at": "2026-05-12T14:30:00.000Z",
  "line_items": [
    {
      "line_item_id": "123456",
      "title": "Textilplatta Grå 50x50",
      "variant": "Återbrukad",
      "sku": "TP-GRA-50",
      "quantity": 100,
      "delivery_date": "2026-06-20"
    },
    {
      "line_item_id": "789012",
      "title": "Textilplatta Blå 50x50",
      "variant": "Ny - Milliken",
      "sku": "TP-BLA-50",
      "quantity": 50,
      "delivery_date": "2026-07-01"
    }
  ]
}
```

## Visa bekräftade datum för kunden

### Alternativ A: I orderbekräftelse-mail
Lägg till i Shopify Admin → Settings → Notifications → Order confirmation:

```liquid
{% assign delivery_meta = order.metafields.custom.confirmed_delivery_dates %}
{% if delivery_meta %}
  {% assign delivery_data = delivery_meta.value | parse_json %}
  <h3>Bekräftade leveransdatum</h3>
  <table>
    <tr><th>Artikel</th><th>Leveransdatum</th></tr>
    {% for item in delivery_data.line_items %}
      {% if item.delivery_date != blank %}
        <tr>
          <td>{{ item.title }}{% if item.variant != blank %} — {{ item.variant }}{% endif %}</td>
          <td>{{ item.delivery_date }}</td>
        </tr>
      {% endif %}
    {% endfor %}
  </table>
{% endif %}
```

### Alternativ B: Via App Proxy (kontosida)
Appen exponerar `/apps/delivery-dates/api/proxy/delivery-dates?order_id=123`
som returnerar JSON. Kan anropas från kundens kontosida via fetch.
