# ReCarpet B2B — Todo utifrån kundens kommentarer

## Produktdata
- [ ] Lägg till **en** kategori-kolumn per produkt (produkt tillhör endast EN kategori: Återbruk / Nytt / Överblivet).
- [ ] Skapa kolumner för Composil likt ORAKs struktur (dimensioner, bildlänkar, tekniska datablad, varumärke, produktetikett) — ReCarpet fyller i själva.
- [ ] Milliken: hämta in all saknad data (lagersaldo, tekniska datablad, priser). Stäm av med Milliken om de tar fram det eller om ReCarpet gör det själva.
- [ ] Följ upp med Composil och ORAK om det finns mer produktdata att hämta från deras system/hemsida (kunden kollar).

## SKU-system
- [ ] Rätta Composil-prefix: `RCT-C-066` (ta bort extra C — ej `RCT-C-C-066`).
- [ ] Lägg till nytt SKU-prefix för ReCarpets eget lager: `RCT-XXXX` (ex: `RCT-9988`).

## Kundgrupper & behörigheter — IMPLEMENTERAT 2026-04-13
- [x] **Utloggad** (ingen tagg): bruttopris, kan köpa Milliken, ser återbruk men kan ej köpa.
- [x] **Pending** (konto utan `member`-tagg): ser notis om att ansökan inväntar godkännande.
- [x] **Member** (tagg `member`): 0 % rabatt, får köpa sortiment, ej storbatch.
- [x] **Member Plus** (taggar `member` + `plus`): 10 % rabatt, full access.
- [x] **Member Premium** (taggar `member` + `premium`): 10 % + tjänster.
- [x] **Krets** (taggar `member` + `premium` + `krets`): samma som Premium, egen sub-tagg.
- [x] Centralt snippet `snippets/rc-customer-tier.liquid` klassar besökare.
- [x] Signup-CTA `snippets/rc-signup-cta.liquid` renderas på PDP/PLP.
- [x] Återbrukade textilplattor kräver inloggat konto (hanteras i PDP + card-product).
- [ ] Bygg funktion för **individuella nettopriser / manuell rabatt** per projekt/kund (SparkLayer customer-specific pricing + Draft Orders — nästa steg).

## Prismodell — DELVIS IMPLEMENTERAT
- [x] `export-pricelists.py` genererar 16 CSV (utloggad, member, plus, premium × 4 valutor) från `Members`-flik i master-Excel. Rabatt bakas in i scriptet.
- [ ] Implementera ReCarpet-påslag för återförsäljare (nästa steg — tas i separat pass).
- [ ] Stöd för egna nettopriser per avtalskund på specifika produkter (ex. Lundbergs 360 kr/m² vs ordinarie 395 kr/m²).

## Sign-up-formulär
- [ ] Befintliga fält räcker (företagsnamn, kontaktperson, e-post, telefon, roll/verksamhet).
- [ ] Roll/verksamhet-alternativen som redan föreslagits räcker (Arkitekt, Byggare, Golvläggare, Fastighetsbolag, Entreprenör, Hyresgäst).

## Fakturauppgifter vid checkout
- [ ] Lägg till fält **"Er referens"** utöver företagsnamn, org.nr, faktura-epost, referensnummer, VAT.

## Mejltexter
- [ ] **Alla mejlutskick ska ske via Klaviyo istället** (ej Shopifys inbyggda mejl) — sätt upp flows för ansökan, godkännande, orderbekräftelse, leverantörsnotis m.m.
- [ ] Placeholder-copy för "Ansökan mottagen", "Konto godkänt" och "Orderbekräftelse" är ok att använda som utgångspunkt — anpassa per kundgrupp.
- [ ] Leverantörsnotis (ORAK/Composil) ska innehålla:
  - Artikelnummer
  - Mängd
  - Leveransadress
  - Leveransdatum
  - Avi-namn
  - Avi-telefonnummer
- [ ] Säkerställ att kunden fyller i dessa uppgifter vid checkout så ReCarpet också får dem.

## Montering
- [ ] Montering som tillval ska vara **kopplat till Member Premium endast** (ej fristående för övriga grupper).

## Underhållsavtal
- [ ] Inte som tillval på produktsidan, men ska omnämnas någonstans på sidan. Diskutera placering/format utifrån siduppbyggnad.

## Produktkategorier / navigation
- [ ] Kategorier i navigation:
  - Överproduktion/stuvar
  - Återbrukade
  - NYA textilplattor (Milliken + nya plattor från ORAK/Composil — OBS: leverantörerna har inte "Milliken" som vi, allt nytt samlas under denna rubrik)
  - Tjänster (endast synlig för Member Premium)

## Öppna avstämningspunkter
- [ ] Stäm av svar från Composil/ORAK om ytterligare produktdata.
- [ ] Stäm av prismodell/rabattlösning när avtalskundsexemplen är sammanställda.
- [ ] Stäm av placering/innehåll för underhållsavtal.

---

# Kompletterande punkter (från tidigare mötes-todo)

## Produktfiltrering & kategorier
- [ ] Bygg filtrering per produkttyp: **Återbruk** (reused), **Nytt material**, **Överblivet/Stuvbit/Räddat**.
- [ ] Mappa kategorierna mot ORAKs befintliga taggar (`återbruk`, `utgående sortiment`).
- [ ] Lägg till kategori-kolumn i produktdatasheets där den inte redan finns från ORAK/Composil.
- [ ] Säkerställ att **räddat/stuvbit INTE** märks som "återbruk" (greenwash-risk — Jonas tydlig på detta).

## Kundgrupper — rabatter
- [ ] Bekräfta exakta rabattprocent per kundgrupp med Jonas/Hampus (ej klart i möte).
- [ ] Beslut om Krets: separat grupp eller = Gold (lutar åt Gold, men behåll Krets som intern tagg så rabatt kan justeras separat senare).

## Signup & account approval flow
- [ ] ReCarpet får mejlnotis med kunduppgifter vid ansökan.
- [ ] Tagging i Shopify triggar välkomstmejl till kunden med bekräftelse av grupp + access.
- [ ] Lägg till obligatoriska fält i signup: företagsnamn, kontaktperson, e-post, telefon, roll/verksamhet.
- [ ] Definiera dropdown-alternativ för roll/verksamhet (skicka till Jonas/Hampus för input).

## Admin-skapade ordrar (Sales Agent-flöde)
- [ ] Shopifys "Send Invoice" kan fungera som orderbekräftelse/offert — anpassa mejltexten.

## Tjänster (services)
- [ ] Tjänster som kan beställas: **Rengöring, Montering, Demontering**.
- [ ] Tjänster ska gå att beställa **fristående** (inte bara som produkt-addon) — för interna återbruksprojekt där kund köper montering utan produkt.
- [ ] Skippa underhållsavtal tills vidare (hanteras av Composil, inte ReCarpet).
- [ ] Skippa förlängd garanti — ej relevant till launch.

## Import-script & prislogik
- [ ] Import-script standardiserar data från ORAK, Composil och Milliken till Shopify-format.
- [ ] **Prispåslag**: ReCarpet lägger på 40% ovanpå leverantörspris — konfigurera i scriptet. (Obs: avstäm mot "50% / 1,5×" från tidigare anteckningar — bekräfta vilken siffra som gäller.)
- [ ] **Avrundning**: priser avrundas alltid UPPÅT (bekräftat av Hampus).
- [ ] SKU-format i scriptet: `RCT-O-{id}` (ORAK), `RCT-C-{id}` (Composil), `Milliken-{id}` (Milliken).

## Composil — saknad data
- [ ] Composils datasheet är ofullständigt: saknade dimensioner, produktbilder, tekniska datablad.
- [ ] Be Composil om mer komplett export (datan finns på deras hemsida — borde gå att extrahera).
- [ ] Prioritera minst **bilder + dimensioner** från Composil.
- [ ] Alla fält måste inte matcha ORAK — "det som finns, finns".

## Produktsida — förbättringar
- [ ] Visa **pris per m²** på produkter i varukorgen.
- [ ] Lägg till **EPD-länk** på alla ORAK-produkter (samma PDF för alla — läggs in via import-script).
- [ ] Lägg till reservation/disclaimer för lagersaldo ("Reservation för lager" — uppdateras veckovis, faktisk tillgänglighet kan skilja).
- [ ] **Beställ prov**: endast för Milliken-produkter, som CTA ("Kontakta oss för mer information") — inte direkt beställningsfunktion.
- [ ] Skippa prov för ORAK/Composil (för långsamt, produkten kan vara borta innan provet anländer).

## Checkout & Fortnox
- [ ] Checkout-fält som krävs för Fortnox-faktura: **organisationsnummer, faktura-epost, referensnummer/märkning** (utöver tidigare nämnda + "Er referens").

## Internationella kunder
- [ ] Admin ska kunna välja momsbehandling per kund: **normal moms** eller **omvänd skattskyldighet** (reverse charge).

## Design & sajtstruktur
- [ ] Fortsätt implementera befintlig designen → nytt Shopify-tema (pågår).
- [ ] Diskutera att slå ihop "Våra kunder" från 4 separata sidor till 1 (flyttades till skriftlig diskussion).
- [ ] Onboarding-upplevelse vid första B2B-inloggning som förklarar vad kunden har tillgång till.
- [ ] Sticky help-knapp (nere till höger) som anpassas efter inloggad kundgrupp.

## Mejl-copy (alla placeholder idag)
- [ ] Samtliga mejl nedan byggs och skickas via **Klaviyo** (inte Shopify-mejl).
- [ ] Signup-bekräftelse ("ditt konto inväntar godkännande").
- [ ] Konto-godkänt-mejl (per kundgrupp — förklarar deras access).
- [ ] Orderbekräftelse.
- [ ] Faktura / draft-order-mejl.
- [ ] Erik tar fram första utkast → Jonas/Hampus granskar och justerar.

## Deliverables & tidsplan
- [ ] **Erik**: ge Jonas/Hampus access till staging + admin-panel (mål: slutet av nästa vecka).
- [ ] **Jonas/Hampus**: svara på alla frågor i sammanfattningsdokumentet.
- [ ] **Jonas/Hampus**: hämta uppdaterad/komplett produktdata från Composil.
- [ ] **Jonas/Hampus**: hämta EPD-länk från ORAK.
- [ ] **Jonas/Hampus**: bekräfta rabattprocent per kundgrupp.
- [ ] **Jonas/Hampus**: beslut om Krets-hantering (Gold vs egen grupp — lutar åt Gold).
- [ ] **Mål för go-live**: slutet av april 2026.
