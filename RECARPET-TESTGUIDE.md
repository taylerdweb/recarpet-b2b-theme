# reCarpet B2B — Testguide & Checklista

*Syfte: Denna guide hjälper er att bekanta er med sidan, förstå alla flöden och systematiskt testa att allt fungerar korrekt innan lansering.*

---

## 1. Så fungerar sidan — Kundperspektiv

### 1.1 Kundnivåer (tiers)

Sidan har fem kundnivåer. Vilken nivå en kund tillhör bestäms av taggar på kundprofilen i Shopify:

| Nivå | Tagg i Shopify | Vad kunden kan göra |
|------|---------------|---------------------|
| **Gäst** (utloggad) | Ingen | Bläddra i katalogen, se bruttopriser, beställa Milliken-prover. Kan inte köpa. |
| **Väntande** (inloggad, ej godkänd) | Ingen b2b-tagg | Ser "Ditt konto granskas"-banner. Kan inte köpa. |
| **Member** | `b2b-member-sek` | Kan köpa vanliga produkter och återbrukade. Ser bruttopriser (0% rabatt). Kan inte köpa storbatcher eller tjänster. |
| **Plus** | `b2b-plus-sek` | Allt som Member + kan köpa storbatcher. 10% rabatt. |
| **Premium / Krets** | `b2b-premium-sek` (+ ev. `krets`) | Allt som Plus + kan lägga till montering och köpa tjänsteprodukter. 10% rabatt. |

*Valutasuffixet (`-sek`, `-nok`, `-dkk`, `-eur`) styr vilken prislista kunden får.*

### 1.2 Kundflödet steg för steg

**Ny kund registrerar sig:**
1. Går till `/pages/b2b-login` (eller klickar "Logga in" i headern)
2. Fyller i ansökningsformuläret: företagsnamn, e-post, telefon, org.nr, moms-nr, roll (Arkitekt/Byggare/etc)
3. Skickar in → ser bekräftelse "Vi återkommer inom 1–2 arbetsdagar"
4. En admin granskar ansökan i Shopify → lägger till rätt kundtagg
5. Kunden kan nu logga in och handla enligt sin nivå

**Kund handlar:**
1. Bläddrar i kollektioner ("Nya textilplattor", "Återbrukade textilplattor")
2. Klickar på en produkt → ser produktsida med SparkLayer-priser baserat på sin nivå
3. Väljer antal (m²), klickar "Köp"
4. Kundkorgen (drawer) öppnas med tillagd produkt
5. Kan fortsätta handla eller gå till checkout

**Montering (Premium/Krets):**
1. På produktsidan syns en checkbox "Lägg till montering +45 kr/m²"
2. Kunden kryssar i → ser beräknad kostnad
3. Vid "Köp" läggs produkten till med montering-attribut
4. En monteringsprodukt (RC-SERVICE-MONTERING) läggs automatiskt till i kundkorgen
5. Monteringsradens kvantitet styrs automatiskt — kunden kan inte ändra den

**Beställ prov (Milliken-produkter):**
1. På Milliken-produkter finns knappen "Beställ prov"
2. Klick → modal öppnas med formulär (namn, e-post, telefon, meddelande)
3. Skickar → kontaktformulär till er inbox

### 1.3 Vad som händer vid restriktioner

Om en kund försöker nå produkter som är begränsade för deras nivå:

- **Storbatch + Member**: Ser meddelande "Stora batcher kräver Plus-medlemskap" med kontaktlänk
- **Tjänsteprodukt + ej Premium**: Ser "Tjänster kräver Premium-medlemskap"
- **Återbrukad + Gäst**: Ser "Återbrukade textilplattor kräver godkänt B2B-konto"
- **Gäst generellt**: Ser "Bli medlem"-knappar och bruttopriser

---

## 2. Så fungerar sidan — Adminperspektiv

### 2.1 Kundhantering

**Godkänna ny kund:**
1. Gå till **Shopify Admin → Customers**
2. Hitta kunden (skickade ansökan via B2B-login-sidan)
3. Öppna kundprofilen → scrolla till **Tags**
4. Lägg till rätt tagg, t.ex. `b2b-member-sek` för en svensk Member-kund
5. Spara — kunden kan nu logga in och handla

**Uppgradera kund:**
- Byt tagg, t.ex. från `b2b-member-sek` till `b2b-plus-sek`
- SparkLayer uppdaterar prislistan automatiskt baserat på taggen

**Valutor:**
- Använd rätt suffix: `-sek` (SEK), `-nok` (NOK), `-dkk` (DKK), `-eur` (EUR)
- T.ex. en norsk Plus-kund: `b2b-plus-nok`

### 2.2 Orderhantering

1. **Shopify Admin → Orders** — alla B2B-ordrar visas här
2. Monteringstjänsten visas som en separat rad (SKU: `RC-SERVICE-MONTERING`)
3. Produkter med monteringsattribut har `montering: true` i customAttributes
4. Handlägg, packa och skicka som vanligt via Shopify

### 2.3 Prislistor

- Prislistor hanteras i **SparkLayer Dashboard → Price lists**
- 16 prislistor finns (4 nivåer × 4 valutor): `member-sek`, `plus-sek`, `premium-sek`, etc.
- Vid prisändringar: uppdatera master-excelfilen → kör `export-pricelists.py` → ladda upp CSV-filerna i SparkLayer

### 2.4 Sidor och innehåll

Alla sidor redigeras via **Online Store → Customize**:

| Sida | Syfte |
|------|-------|
| Startsidan | Hero, produkter, tjänster-timeline, kundkort |
| Om oss | Företagsinfo |
| Vad vi gör | Tjänstebeskrivning |
| Kontakta oss | Kontaktformulär |
| Fastighetsägare / Arkitekter / Hyresgäst / Entreprenör | Segment-specifika landningssidor |
| Integritetspolicy / Köpvillkor | Juridiska texter |
| B2B-login | Inloggning + ansökningsformulär |

---

## 3. All funktionalitet

### Produktsida (PDP)

- SparkLayer köpwidget (kvantitet, pris, köpknapp)
- Nivåbaserad prissättning (olika pris per tier)
- Montering-checkbox (bara Premium/Krets, ej tjänsteprodukter)
- Delsumma för montering (X m² × 45 kr = Y kr)
- Produktspecifikationer (backing, format, tjocklek, brandklass, akustik, LRV)
- Lagerstatus-badge (i lager / lågt lager / ej i lager)
- Lagerdisclaimer för återbruk/överproduktion
- Beställ prov-knapp (Milliken-produkter)
- Storbatch-spärr (Member utan Plus)
- Återbruksspärr (Gäster)
- Tjänstespärr (ej Premium)
- Standardkvantitet 5 m²
- Väntande kund-meddelande ("Ditt konto granskas")

### Kundkorg

- SparkLayer cart drawer (slide-out)
- SparkLayer cart page (/cart)
- Monteringsprodukt auto-tillagd med synkad kvantitet
- Monteringsraden låst (inga kontroller synliga)
- Dold Shopify-kundkorg (B2B-kunder ser bara SparkLayer-korgen)
- Varukorgikon med badge (antal produkter)

### Kollektionssidor

- SparkLayer-produktkort med pris per nivå
- Filtrering (standard Shopify-facetter)
- Sortering (pris, namn)
- Tier-baserad produktspärr per kort

### Konto och inloggning

- B2B-ansökningsformulär (företagsnamn, org.nr, moms-nr, roll, etc.)
- Inloggning (e-post + lösenord)
- Kontosida med orderhistorik och adresser
- SparkLayer-autentisering (token via metafield)
- Väntande-banner för ej godkända kunder

### Navigation

- Header med dropdown-meny (Våra kunder, Vad vi gör, Våra golv, Om oss)
- B2B-loginlänk (gäster) / Kontolänk (inloggade)
- Kontaktlänk
- Varukorgikon (SparkLayer, bara B2B-kunder)
- Footer med kontaktinfo, policylänkar, LinkedIn

### SparkLayer-specifikt

- Shadow DOM-rendering (alla B2B-element)
- Dolt customer reference-fält
- 4 prislistenivåer × 4 valutor = 16 prislistor
- Automatisk prislista baserat på kundtagg

---

## 4. Testchecklista

### Förberedelser

Innan ni börjar testa, skapa testkunder med följande taggar i **Shopify Admin → Customers → Add customer**:

| Testkund | E-post (förslag) | Tagg |
|----------|-------------------|------|
| Gäst | *(ingen kund behövs — logga ut)* | — |
| Väntande | test-pending@recarpet.se | *(ingen b2b-tagg)* |
| Member | test-member@recarpet.se | `b2b-member-sek` |
| Plus | test-plus@recarpet.se | `b2b-plus-sek` |
| Premium | test-premium@recarpet.se | `b2b-premium-sek` |
| Krets | test-krets@recarpet.se | `b2b-premium-sek`, `krets` |

---

### A. Registrering och inloggning

- [ ] **A1.** Gå till `/pages/b2b-login` som utloggad → ansökningsformuläret visas
- [ ] **A2.** Fyll i alla fält och skicka → bekräftelsemeddelande visas
- [ ] **A3.** Kontrollera att ansökan kommer in (Shopify Admin → kontaktformulär eller e-post)
- [ ] **A4.** Logga in som Väntande-kund → gul "ansökan granskas"-banner visas
- [ ] **A5.** Kontrollera att Väntande-kund INTE kan lägga produkter i kundkorgen
- [ ] **A6.** I Shopify Admin: lägg till `b2b-member-sek` på Väntande-kunden
- [ ] **A7.** Logga in som den nu godkända kunden → banner borta, kan handla

### B. Produktsida — per kundnivå

**Som Gäst (utloggad):**
- [ ] **B1.** Öppna en vanlig produkt → ser bruttopris, "Bli medlem"-knapp istället för köpknapp
- [ ] **B2.** Öppna en storbatch-produkt → ser spärr-meddelande
- [ ] **B3.** Öppna en återbrukad produkt → ser spärr-meddelande
- [ ] **B4.** Öppna en tjänsteprodukt → ser spärr-meddelande
- [ ] **B5.** Öppna en Milliken-produkt → "Beställ prov"-knapp synlig och fungerar

**Som Member:**
- [ ] **B6.** Öppna en vanlig produkt → ser Member-pris (bruttopris), köpknapp fungerar
- [ ] **B7.** Öppna en storbatch-produkt → ser spärr "Kräver Plus-medlemskap"
- [ ] **B8.** Öppna en återbrukad produkt → kan köpa
- [ ] **B9.** Öppna en tjänsteprodukt → ser spärr "Kräver Premium-medlemskap"
- [ ] **B10.** Montering-checkbox SYNS INTE

**Som Plus:**
- [ ] **B11.** Öppna en vanlig produkt → ser 10% rabatterat pris
- [ ] **B12.** Öppna en storbatch-produkt → kan köpa
- [ ] **B13.** Öppna en tjänsteprodukt → ser spärr "Kräver Premium"
- [ ] **B14.** Montering-checkbox SYNS INTE

**Som Premium:**
- [ ] **B15.** Öppna en vanlig produkt → ser 10% rabatterat pris
- [ ] **B16.** Öppna en storbatch-produkt → kan köpa
- [ ] **B17.** Öppna en tjänsteprodukt → kan köpa
- [ ] **B18.** Montering-checkbox SYNS på vanliga produkter
- [ ] **B19.** Montering-checkbox SYNS INTE på tjänsteprodukter (RC-SERVICE-*)

### C. Beställ prov

- [ ] **C1.** Öppna en Milliken-produkt → knappen "Beställ prov" syns
- [ ] **C2.** Klicka → modal med formulär öppnas
- [ ] **C3.** Fyll i namn, e-post, telefon, meddelande → skicka
- [ ] **C4.** Kontrollera att formuläret kommer in till er e-post
- [ ] **C5.** Öppna en ICKE-Milliken-produkt → knappen syns INTE

### D. Lagerstatus och disclaimer

- [ ] **D1.** Öppna en produkt med lagersaldo → grön "I lager"-badge visas
- [ ] **D2.** Öppna en återbrukad/överproduktionsprodukt → gul disclaimer visas under lagerstatus
- [ ] **D3.** Kontrollera att disclaimern INTE visas på vanliga nyproducerade produkter

### E. Kundkorg — grundläggande

- [ ] **E1.** Lägg till en produkt → cart drawer öppnas med produkten
- [ ] **E2.** Ändra kvantitet med +/- → kvantiteten uppdateras
- [ ] **E3.** Ta bort produkt → produkten försvinner från korgen
- [ ] **E4.** Lägg till flera olika produkter → alla visas i korgen
- [ ] **E5.** Varukorgikon i headern visar korrekt antal produkter
- [ ] **E6.** Klicka på varukorgsikonen → cart drawer öppnas

### F. Montering (som Premium/Krets)

- [ ] **F1.** Kryssa i "Lägg till montering" → delsumma visas (X m² × 45 kr)
- [ ] **F2.** Ändra kvantitet → delsumman uppdateras
- [ ] **F3.** Klicka "Köp" med montering ikryssad → kundkorg öppnas
- [ ] **F4.** Kundkorgen visar produkten OCH RC-SERVICE-MONTERING som separat rad
- [ ] **F5.** Monteringsraden har INGA +/- knappar, INGEN delete-knapp, INGET quantity-input
- [ ] **F6.** Monteringsradens kvantitet matchar produktens kvantitet
- [ ] **F7.** Lägg till en andra produkt med montering → monteringskvantiteten ökar
- [ ] **F8.** Lägg till samma produkt UTAN montering → monteringsraden påverkas inte negativt
- [ ] **F9.** Ta bort en produkt med montering → monteringskvantiteten minskar
- [ ] **F10.** Ta bort ALLA produkter med montering → monteringsraden försvinner
- [ ] **F11.** Uppdatera sidan → öppna kundkorg → monteringsraden fortfarande låst

### G. Checkout-flöde (fullständig order)

- [ ] **G1.** Fyll kundkorgen med minst 2 produkter (varav en med montering om Premium)
- [ ] **G2.** Gå till checkout
- [ ] **G3.** Kontrollera att alla produkter och priser stämmer i checkout
- [ ] **G4.** Genomför en testbeställning (använd Shopify Bogus Gateway om möjligt)
- [ ] **G5.** Kontrollera ordersidan efter beställning — alla rader korrekta
- [ ] **G6.** I Shopify Admin → Orders: hitta ordern, kontrollera att monteringsraden syns med rätt kvantitet
- [ ] **G7.** Testa att handlägga ordern (markera som betald, packa, skicka)

### H. Kollektionssidor

- [ ] **H1.** Bläddra i "Nya textilplattor" → alla produkter visas med SparkLayer-kort
- [ ] **H2.** Bläddra i "Återbrukade textilplattor" → alla produkter visas
- [ ] **H3.** Testa filtrering (om filter finns) → filtrerar korrekt
- [ ] **H4.** Testa sortering (pris, namn) → sorterar korrekt
- [ ] **H5.** Kontrollera att produktkort visar rätt pris för inloggad nivå

### I. Navigation och sidor

- [ ] **I1.** Header: alla dropdown-länkar fungerar (Våra kunder, Vad vi gör, Våra golv, Om oss)
- [ ] **I2.** "Kontakta oss"-länk → kontaktsidan öppnas
- [ ] **I3.** "Logga in"-länk (utloggad) → B2B-login-sidan
- [ ] **I4.** Kontoikon (inloggad) → kontosidan
- [ ] **I5.** Footer: alla länkar fungerar (policy, villkor, LinkedIn, etc.)
- [ ] **I6.** Kontaktsidan: formuläret fungerar, meddelande kommer in
- [ ] **I7.** Mobilvy: alla sidor fungerar responsivt
- [ ] **I8.** Om oss, Vad vi gör, segment-sidor: innehållet visas korrekt

### J. Adminflöde — fullständig orderhantering

Gör detta som en simulering av hela kedjan:

- [ ] **J1.** Skapa en ny kund i Shopify Admin (simulera ny ansökan)
- [ ] **J2.** Lägg till tagg `b2b-member-sek` → spara
- [ ] **J3.** Logga in som den nya kunden → kan handla
- [ ] **J4.** Uppgradera kunden till `b2b-plus-sek` → logga in igen → ser nya priser, kan köpa storbatcher
- [ ] **J5.** Uppgradera till `b2b-premium-sek` → logga in igen → ser montering-checkbox
- [ ] **J6.** Lägg en beställning som Premium-kund (med montering)
- [ ] **J7.** I Shopify Admin: öppna ordern → alla rader korrekta (matta + montering)
- [ ] **J8.** Markera ordern som betald
- [ ] **J9.** Markera som skickad (lägg till spårningsnummer om tillämpligt)
- [ ] **J10.** Kontrollera att kunden ser uppdaterad orderstatus på sitt konto

### K. Valutor och internationella kunder

- [ ] **K1.** Skapa testkund med tagg `b2b-member-nok` → ser NOK-priser
- [ ] **K2.** Skapa testkund med tagg `b2b-plus-dkk` → ser DKK-priser med 10% rabatt
- [ ] **K3.** Kontrollera att prislistorna matchar förväntade priser i respektive valuta

---

## Anteckningar under testning

*Använd detta utrymme för att notera buggar, frågor eller feedback under testningen:*

| # | Beskrivning | Allvarlighetsgrad | Status |
|---|-------------|-------------------|--------|
|   |             |                   |        |
|   |             |                   |        |
|   |             |                   |        |
