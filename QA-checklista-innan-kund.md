# ReCarpet B2B — QA-checklista innan kundöverlämning

---

## 1. KUNDGRUPPER & BEHÖRIGHETER

Testa varje kundnivå genom att logga in med testkonton som har rätt taggar.

### Utloggad (ingen inloggning)
- [ ] Ser Milliken-produkter och kan lägga i varukorg
- [ ] Ser återbrukade produkter men kan INTE köpa (CTA "Ansök om konto" visas)
- [ ] Ser bruttopris (utloggad-tier)
- [ ] Storbatch-produkter: ser men kan ej köpa
- [ ] Tjänster (Montering/Rengöring): EJ synliga
- [ ] Navigation visar rätt undertexter (Återbrukade textilplattor, Tjänster, Milliken, Överproduktion)

### Pending (inloggad, ingen member-tagg)
- [ ] Ser "ansökan granskas"-banner
- [ ] Kan INTE köpa någon produkt
- [ ] Omdirigeras eller visas info om att kontot inväntar godkännande

### Member (tagg: `b2b-member-sek`)
- [ ] Kan köpa återbrukade produkter
- [ ] Kan köpa Milliken-produkter
- [ ] Ser member-pris (0% rabatt, bruttopris)
- [ ] Storbatch (qty > 300): ser "Endast för Plus-medlemmar" — kan EJ köpa
- [ ] Tjänster: EJ synliga/köpbara
- [ ] Montering som tillval: EJ tillgängligt

### Member Plus (taggar: `b2b-plus-sek`)
- [ ] Ser plus-pris (10% rabatt)
- [ ] Kan köpa storbatch-produkter (qty > 300)
- [ ] Kan köpa alla vanliga produkter
- [ ] Tjänster: EJ synliga/köpbara
- [ ] Montering: EJ tillgängligt

### Member Premium (taggar: `b2b-premium-sek`)
- [ ] Ser premium-pris (10% rabatt)
- [ ] Kan köpa storbatch
- [ ] Ser och kan köpa tjänster (Montering, Rengöring)
- [ ] Montering som tillval: tillgängligt
- [ ] Full access till allt

### Krets (taggar: `b2b-premium-sek` + `krets`)
- [ ] Samma access som Premium
- [ ] Krets-tagg visas korrekt (om relevant i UI)

---

## 2. PRODUKTER & LAGER

### Testprodukter (15 st)
- [ ] Alla 5 Orak-produkter visas med bilder och korrekt lager
- [ ] Alla 5 Milliken-produkter visas med bilder och korrekt lager
- [ ] Alla 5 Composil-produkter visas med bilder och korrekt lager
- [ ] Inga produkter visar "Slut i lager" felaktigt (kontrollera inventory)

### Produktserier (Collections)
- [ ] "Återbrukade mattor"/"Återbrukade textilplattor" — innehåller Orak + Composil-produkter
- [ ] "Överproduktion" — innehåller tilldelade Orak + Composil-produkter
- [ ] "Milliken" — innehåller alla 5 Milliken-produkter
- [ ] Tjänsteprodukter syns i rätt sammanhang

### Produktsidor (PDP)
- [ ] Pris visas per m² med korrekt valuta
- [ ] Produktkod (SKU) visas korrekt
- [ ] Format/dimensioner visas (50x50 cm etc)
- [ ] Lagersaldo visas (In stock X m²)
- [ ] "I LAGER"-badge visas korrekt
- [ ] Storbatch-produkt (Ember 5T226, qty 642): visar lås för Member, öppet för Plus/Premium

---

## 3. SPARKLAYER & PRISSÄTTNING

- [ ] Bulk-prislista uppladdad i SparkLayer Admin → Price Lists
- [ ] SparkLayer-prismodul laddar på produktsidan (ej tom)
- [ ] Rätt pris per kundnivå:
  - Utloggad: utloggad-pris
  - Member: member-pris (= samma som utloggad)
  - Plus: 10% rabatt
  - Premium: 10% rabatt
- [ ] Rätt valuta beroende på kund-tagg (-sek, -nok, -dkk, -eur)
- [ ] Varukorg visar korrekt SparkLayer-pris (ej Shopify-listpris)
- [ ] Checkout beräknar korrekt summa

---

## 4. CHECKOUT & BESTÄLLNING

- [ ] Lägg en testorder som Member → orderbekräftelse fungerar
- [ ] Lägg en testorder som Plus → korrekt rabatterat pris
- [ ] Kontrollera att checkout-fält finns:
  - Företagsnamn
  - Organisationsnummer
  - Faktura-epost
  - Referensnummer/märkning
  - "Er referens"
- [ ] Order skapas korrekt i Shopify Admin → Ordrar

---

## 5. MEJLFLÖDEN (KLAVIYO)

### Ansökan mottagen
- [ ] Triggas vid ny kundregistrering
- [ ] Mejl levereras (ej spam)
- [ ] Innehåll korrekt (svenska)

### Konto godkänt
- [ ] Triggas när kund tilldelas b2b-member/plus/premium-tagg
- [ ] Rätt variant skickas beroende på tier + valuta/språk:
  - Member SEK → svensk text
  - Plus NOK → norsk text
  - Premium EUR → engelsk text
- [ ] Mejl levereras (ej spam)

### Orderbekräftelse
- [ ] Triggas vid ny order
- [ ] Rätt språkvariant baserat på kundtagg (-sek/-nok/-dkk/-eur)
- [ ] Orderdetaljer visas korrekt (produktnamn, antal, pris, leveransadress)

### Intern ordernotifiering (till ReCarpet)
- [ ] Triggas vid ny B2B-order
- [ ] Skickas till rätt intern mottagare
- [ ] Innehåller orderdetaljer

### Leverantörsnotifiering — Orak
- [ ] Triggas via Shopify Flow vid order med RCT-O-* SKU
- [ ] Skickas till Oraks kontaktperson
- [ ] Mejlet innehåller: artikelnummer, mängd, leveransadress, leveransdatum, avi-namn, avi-telefon
- [ ] Mejlet är på engelska

### Leverantörsnotifiering — Composil
- [ ] Triggas via Shopify Flow vid order med RCT-C-* SKU
- [ ] Skickas till Composils kontaktperson
- [ ] Samma format som Orak (engelska)

### Generellt e-post
- [ ] Sändande domän autentiserad i Klaviyo (DKIM/SPF DNS-poster)
  - Om ej: mejl hamnar i skräppost!
  - Klaviyo → Settings → Email → Domains → lägg till recarpet.se
- [ ] Testa att mejl INTE hamnar i spam (skicka till Gmail/Outlook)

---

## 6. SHOPIFY FLOW

### Leverantörsnotifiering (for-each loop)
- [ ] Flow triggas vid Draft Order / Order
- [ ] For-each loop på lineItems fungerar
- [ ] SKU-villkor matchar nya prefix: `RCT-O-` (Orak), `RCT-C-` (Composil)
- [ ] Track Event skickar korrekt data till Klaviyo:
  - `b2b_supplier_order_orak` för Orak-produkter
  - `b2b_supplier_order_composil` för Composil-produkter
- [ ] Event properties inkluderar: order_name, line_item_sku, line_item_quantity, shipping_address, customer_name, customer_phone

### Kundregistrering
- [ ] Ny registrering → taggas "pending" / "guest"
- [ ] Klaviyo-event triggas för "Ansökan mottagen"-flow

### Kontogodkännande
- [ ] Admin lägger till b2b-member/plus/premium-tagg → Klaviyo-event triggas → "Konto godkänt"-mejl

---

## 7. NAVIGATION & DESIGN

- [ ] Mega-meny visar korrekta kategorier med undertexter:
  - Återbrukade textilplattor — "Vårt eget sortiment av återbrukade kvalitetsmattor"
  - Tjänster — "Inventering, demontering, montering och service av textilplattor"
  - Milliken — "Nyproducerade textilplattor från Milliken"
  - Överproduktion — "Överskottslager av kvalitetsmattor till reducerat pris"
- [ ] Alla meny-länkar fungerar och leder till rätt collection/sida
- [ ] Mobilmeny fungerar och visar samma kategorier
- [ ] Footer-länkar fungerar

---

## 8. KÄNDA PROBLEM ATT FIXA INNAN ÖVERLÄMNING

- [ ] **E-post i spam** — Sätt upp dedicated sending domain i Klaviyo (DKIM/SPF DNS på recarpet.se)
- [ ] **Shopify Flow supplier notification** — Debugga att for-each loop + SKU-villkor faktiskt triggar Track Event
- [ ] **Inventory timing** — Verifiera att testprodukter har korrekt lagersaldo (ej "Slut i lager")
- [ ] **Duplicerade SKU-varningar** — Kontrollera att inga gamla varianter finns kvar med samma SKU
- [ ] **"50x50 cm cm"** — Dimensions-metafältet visar "50x50 cm cm" (dubbel enhet) — ta bort "cm" från metafield-värdet ELLER från temat

---

## 9. ADMIN-GUIDE FÖR KUNDEN

Förbered en kort guide till kunden om hur de:
- [ ] Godkänner en ny kund (lägger till b2b-member/plus/premium-tagg i Shopify Admin → Kunder)
- [ ] Ser inkommande ordrar i Shopify Admin
- [ ] Ändrar en kunds tier (byter tagg)
- [ ] Ser e-postflöden i Klaviyo
- [ ] Laddar upp uppdaterade prislistor i SparkLayer

---

## 10. SLUTKONTROLL

- [ ] Alla testordrar raderade/arkiverade
- [ ] Inga test-mejladresser kvar i Klaviyo-flows som hård-kodade mottagare
- [ ] Sidan ser professionell ut utan placeholder-innehåll
- [ ] Alla produktbilder laddas korrekt
- [ ] Sidan fungerar i Chrome, Safari, Firefox
- [ ] Mobilvy fungerar korrekt
