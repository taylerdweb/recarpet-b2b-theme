# ReCarpet B2B E-handel — Fullständig genomgång inför kundmöte fredag

> Gå igenom varje sektion i ordning. Bocka av med `[x]` allt eftersom.
> Gör anteckningar direkt i detta dokument under varje punkt.

---

## 1. GRUNDINSTÄLLNINGAR & KONFIGURATION

### 1.1 Butiksinställningar
- [ ] Butiksnamn ändrat från "recarpet-build" till "ReCarpet" (Settings → General)
- [ ] Kontaktmejl korrekt (mottagare för ordermejl etc.)
- [ ] Adress/företagsinfo korrekt (syns på fakturor)
- [ ] Tidzon inställd på Stockholm/CET
- [ ] Valuta: SEK som primär
- [ ] Viktenheter: kg

### 1.2 Domän & DNS
- [ ] Primär domän kopplad (recarpet.se eller shop.recarpet.se)
- [ ] SSL-certifikat aktivt
- [ ] Redirect från www till icke-www (eller tvärtom)
- [ ] Lösenordsskydd borttaget inför launch

### 1.3 Juridiskt
- [ ] Köpvillkor (Terms of Service) upplagda
- [ ] Integritetspolicy (Privacy Policy) upplagd
- [ ] Returer & reklamationspolicy definierad
- [ ] Cookie-banner/GDPR-samtycke på plats

---

## 2. B2B KUNDHANTERING

### 2.1 Kundkonton & behörigheter
- [ ] B2B-konton konfigurerade i Settings → Customers → B2B
- [ ] Företag (Companies) skapade med korrekt info
- [ ] Kontaktpersoner kopplade till respektive företag
- [ ] Testa: kan kund logga in med B2B-inloggning?
- [ ] Testa: ser kund rätt priser efter inloggning?
- [ ] Testa: kan kund INTE se priser utan inloggning? (om det är önskat)
- [ ] Testa: flera användare på samma företag — fungerar det?

### 2.2 Kundgrupper & prislistor
- [ ] Prislistor (Catalogs) skapade per kundgrupp om relevant
- [ ] Procentuell rabatt eller fasta priser per katalog?
- [ ] Testa: logga in som Kundgrupp A → ser rätt priser
- [ ] Testa: logga in som Kundgrupp B → ser rätt priser
- [ ] Kunder utan B2B-konto — vad händer? (redirect till kontaktformulär?)

### 2.3 Betalningsvillkor
- [ ] Betalningsvillkor definierade per företag (Net 30, Net 60 etc.)
- [ ] Testa: syns betalningsvillkor korrekt i checkout?
- [ ] Testa: order skapas med status "Payment pending" (faktura)

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 3. PRODUKTER & KATALOG

### 3.1 Produktstruktur
- [ ] Produkttyper definierade (Återbrukade textilplattor, Nya textilplattor, Tjänster?)
- [ ] Collections skapade och korrekta
- [ ] Produkttaggar konsekventa och användbara för filtrering
- [ ] Produktbilder uppladdade och av bra kvalitet
- [ ] Produktbeskrivningar kompletta
- [ ] Varianter korrekt uppsatta (storlek, färg, kvalitet?)
- [ ] SKU-nummer på alla produkter
- [ ] Lagerstatus/lagerantal korrekt
- [ ] Vikter angivna (behövs för frakt)

### 3.2 CSV-import från Orak
- [ ] Exportformat från Orak dokumenterat
- [ ] Mappning: Orak-fält → Shopify-fält definierad
- [ ] CSV-kolumner: Handle, Title, Body (HTML), Vendor, Type, Tags, Published, Variant SKU, Variant Price, Variant Compare At Price, Variant Inventory Qty, Variant Weight, Image Src
- [ ] Testa: importera en testfil från Orak → verifieras i Shopify
- [ ] Specialtecken (å, ä, ö) hanteras korrekt i CSV (UTF-8)
- [ ] Dubbletthantering: vad händer vid re-import? (uppdatering vs duplicering)

**Orak CSV-format:**
```csv
[Dokumentera exakt kolumnmappning här]
Orak-fält → Shopify-fält
--------------------------
[artikelnummer] → Variant SKU
[benämning] → Title
[pris] → Variant Price
[antal] → Variant Inventory Qty
[vikt] → Variant Weight
[kategori] → Product Type / Tags
[bild-url] → Image Src
```

### 3.3 CSV-import från Composil
- [ ] Exportformat från Composil dokumenterat
- [ ] Mappning: Composil-fält → Shopify-fält definierad
- [ ] Testa: importera en testfil från Composil → verifieras i Shopify
- [ ] Skillnader mot Orak-formatet dokumenterade

**Composil CSV-format:**
```csv
[Dokumentera exakt kolumnmappning här]
Composil-fält → Shopify-fält
-----------------------------
```

### 3.4 CSV-import för egna mattor
- [ ] Format för ReCarpets egna mattor dokumenterat
- [ ] Testa import
- [ ] Bildhantering: laddas bilder via URL i CSV eller separat?

### 3.5 Löpande produktuppdatering
- [ ] Process definierad: hur ofta uppdateras produkter?
- [ ] Vem ansvarar för CSV-export → import?
- [ ] Behövs automatisering? (app, script, Shopify Flow?)
- [ ] Hur hanteras utgångna/slutsålda produkter? (arkiveras, döljs, tas bort?)

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 4. KÖPRESA — KUNDPERSPEKTIV (testa hela flödet!)

### 4.1 Före köp
- [ ] Startsida laddar korrekt, alla sektioner synliga
- [ ] Navigation fungerar (mega-menu, alla länkar)
- [ ] Produktkatalog/collection-sidor visar rätt produkter
- [ ] Filtrering & sortering fungerar
- [ ] Produktsida: all info synlig (pris, beskrivning, bilder, lager)
- [ ] Sökfunktion hittar produkter
- [ ] Kund kan logga in smidigt

### 4.2 Varukorg & checkout
- [ ] Lägg till produkt i varukorgen → fungerar
- [ ] Ändra antal i varukorgen → fungerar
- [ ] Ta bort produkt ur varukorgen → fungerar
- [ ] Gå till checkout → rätt priser visas
- [ ] B2B-priser (från katalog/prislista) visas korrekt i checkout
- [ ] Leveransadress: förfylld med företagsadress?
- [ ] Faktureringsadress: korrekt
- [ ] Betalningsvillkor syns (t.ex. "Net 30 — Faktura")
- [ ] Fraktval visas (om tillämpligt)
- [ ] Moms visas korrekt (ex moms / inkl moms — se sektion 6)
- [ ] Slutför order → orderbekräftelse visas

### 4.3 Efter köp
- [ ] Orderbekräftelse-sida visas med korrekt info
- [ ] Orderbekräftelse-mejl skickas till kund (se sektion 5)
- [ ] Kund kan se order i sitt konto under "Ordrar"
- [ ] Kund kan se orderstatus (bekräftad, skickad, levererad)

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 5. MEJLFLÖDEN — alla notifikationer

### 5.1 Kundmejl (Settings → Notifications)
Testa att varje mejl skickas, ser bra ut, och innehåller rätt info:

- [ ] **Orderbekräftelse** — skickas vid lagd order
- [ ] **Order redigerad** — skickas om admin ändrar ordern
- [ ] **Order annullerad** — skickas vid avbokning
- [ ] **Fraktbekräftelse** — skickas när order markeras som skickad (med tracking-nummer om tillämpligt)
- [ ] **Leveransuppdatering** — skickas vid statusändring (utlevererad)
- [ ] **Återbetalning** — skickas vid refund
- [ ] **Utkastorder (Draft order invoice)** — skickas vid B2B draft orders
- [ ] **Kundkonto — inbjudan** — skickas till nya B2B-kunder
- [ ] **Kundkonto — välkomstmejl** — skickas när konto aktiveras
- [ ] **Kundkonto — återställ lösenord** — fungerar
- [ ] **Kontaktformulär — bekräftelse** — skickas (om aktiverat)

### 5.2 Adminmejl
- [ ] Ny order → notifikation till rätt mejladress
- [ ] Ordrar med hög risk → flaggas (om Shopify Payments)
- [ ] Lågt lager → notifikation (om konfigurerat)

### 5.3 Mejl-design
- [ ] ReCarpet logotyp i mejlmallarna
- [ ] Rätt färger och typsnitt (matchar varumärket)
- [ ] Kontaktinfo i footer på alla mejl
- [ ] Mejl fungerar i olika klienter (Gmail, Outlook)

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 6. MOMS (VAT)

### 6.1 Momsinställningar
- [ ] Momsregistreringsnummer angivet i Settings → Taxes
- [ ] Sverige: 25% moms konfigurerad
- [ ] B2B-priser: visas exklusive moms? (standard för B2B)
- [ ] Checkout visar moms separat på orderraden
- [ ] Faktura visar moms korrekt

### 6.2 EU-handel (om tillämpligt)
- [ ] Omvänd skattskyldighet (reverse charge) för EU B2B-kunder med VAT-nummer
- [ ] VAT-validering vid checkout (manuellt eller via app)
- [ ] Momsfri försäljning till B2B-kunder utanför Sverige med giltigt VAT-nummer
- [ ] Korrekt momsbehandling per market (se sektion 7)

### 6.3 Testa momscenarier
- [ ] Testorder: svensk kund → 25% moms tillkommer
- [ ] Testorder: EU-kund med VAT-nummer → 0% moms (reverse charge)
- [ ] Testorder: kund utanför EU → 0% moms
- [ ] Verifiera att moms visas korrekt på orderbekräftelse
- [ ] Verifiera att moms visas korrekt i Shopify admin

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 7. MARKETS & INTERNATIONELLT

### 7.1 Markets-konfiguration (Settings → Markets)
- [ ] Primär market: Sverige (SEK, svenska)
- [ ] Sekundära markets definierade? (EU, Norden, övriga?)
- [ ] Valuta per market korrekt
- [ ] Språk per market korrekt
- [ ] Domänstrategi per market (subdomän, subfolder, separat domän?)

### 7.2 Priser per market
- [ ] Prisavrundning konfigurerad per market
- [ ] Prislistor kopplade till rätt markets
- [ ] Fraktzoner matchar markets

### 7.3 Testa
- [ ] Byt till annan market → rätt språk och valuta
- [ ] Lägg order från annan market → korrekt moms och frakt
- [ ] B2B-kund i annan market → rätt katalogpriser

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 8. FAKTURA-FLÖDE

### 8.1 Faktureringsprocess
- [ ] Definiera flödet: Kund beställer → order skapas → faktura skickas → betalning inkommer
- [ ] Vem skickar faktura? (Shopify, extern integration, manuellt?)
- [ ] Faktura-app installerad och konfigurerad? (t.ex. Sufio, Order Printer, Billie)
- [ ] Fakturanummersekvens korrekt
- [ ] Fakturainnehåll: företagsnamn, org.nr, momsreg.nr, betalningsvillkor, bankgiro/IBAN

### 8.2 Fakturadesign
- [ ] ReCarpet logotyp på faktura
- [ ] Korrekt avsändarinfo
- [ ] Alla juridiskt nödvändiga fält med (org.nr, moms etc.)
- [ ] Betalningsinstruktioner tydliga

### 8.3 Betalningsuppföljning
- [ ] Process för att matcha inbetalningar mot ordrar
- [ ] Markera order som betald i Shopify vid mottagen betalning
- [ ] Påminnelserutin vid utebliven betalning
- [ ] Kreditkontroll innan nya B2B-kunder godkänns?

### 8.4 Draft Orders (utkastordrar)
- [ ] Testa: skapa draft order i admin → skicka faktura till kund
- [ ] Kund kan betala via faktura-länk?
- [ ] Draft order konverteras till riktig order vid betalning

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 9. FRAKT & LEVERANS

### 9.1 Fraktzoner
- [ ] Sverige definierad som fraktzon
- [ ] Övriga zoner definierade (Norden, EU, Internationellt?)
- [ ] Fraktpriser per zon konfigurerade

### 9.2 Fraktalternativ
- [ ] Fraktmetoder definierade (t.ex. pall, paket, hämta själv)
- [ ] Prisberäkning: fast pris, viktbaserat, eller fraktintegration?
- [ ] Fraktkostnader rimliga och verifierade
- [ ] Gratis frakt-tröskel? (t.ex. fri frakt över X kr)
- [ ] Hanteras fraktbokning utanför Shopify? (egen logistik, speditör)

### 9.3 Leveransprocess
- [ ] Order markeras som fulfillad när den skickas
- [ ] Tracking-nummer läggs till (om tillämpligt)
- [ ] Fraktbekräftelsemejl skickas automatiskt
- [ ] Partiella leveranser möjliga? (del av order skickas separat)

### 9.4 Testa
- [ ] Testorder Sverige → rätt fraktpris i checkout
- [ ] Testorder annan zon → rätt fraktpris i checkout
- [ ] Markera som skickad i admin → mejl skickas

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 10. ADMIN-PERSPEKTIV — daglig drift

### 10.1 Orderhantering
- [ ] Nya ordrar syns tydligt i Orders-vyn
- [ ] Orderflöde: Ny → Bekräftad → Packad → Skickad → Levererad
- [ ] Kan filtrera ordrar på status, kund, datum
- [ ] Kan redigera order (lägga till/ta bort produkter, ändra adress)
- [ ] Kan annullera order
- [ ] Kan göra delvis eller hel återbetalning
- [ ] Ordrar kopplas till rätt B2B-företag

### 10.2 Produkthantering (admin)
- [ ] Kan skapa ny produkt manuellt
- [ ] Kan importera produkter via CSV (se sektion 3)
- [ ] Kan redigera pris, lager, beskrivning
- [ ] Kan arkivera/dölja utgångna produkter
- [ ] Bilduppladdning fungerar smidigt

### 10.3 Kundhantering (admin)
- [ ] Kan lägga till nytt B2B-företag
- [ ] Kan bjuda in ny kontaktperson
- [ ] Kan tilldela prislista/katalog till företag
- [ ] Kan se kundens orderhistorik
- [ ] Kan ändra betalningsvillkor per företag

### 10.4 Rapporter & analytics
- [ ] Försäljningsrapport visar relevanta data
- [ ] Kan exportera orderdata
- [ ] Google Analytics kopplat? (om önskat)
- [ ] Shopify Analytics aktiverat

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 11. DESIGN & UX — slutgiltig genomgång

### 11.1 Desktop
- [ ] Alla sektioner på startsidan ser bra ut
- [ ] Mega-menu fungerar och ser rätt ut
- [ ] Logo swap (vit på hero, grön på scroll) fungerar
- [ ] Collection-sidor formaterade korrekt
- [ ] Produktsidor ser bra ut
- [ ] Checkout ser professionell ut
- [ ] Footer komplett (kontaktinfo, länkar, legal)

### 11.2 Mobil
- [ ] Startsidan responsiv
- [ ] Hamburger-meny fungerar
- [ ] Produktbilder skalas korrekt
- [ ] Checkout fungerar på mobil
- [ ] Touch-targets tillräckligt stora

### 11.3 Hastighet
- [ ] Lighthouse score acceptabel (>70)
- [ ] Bilder optimerade (WebP, rätt storlek)
- [ ] Inga tunga scripts som blockerar

**Anteckningar:**
```
[Skriv anteckningar här]
```

---

## 12. SÄKERHET & BACKUP

- [ ] Tema-backup tagen innan launch
- [ ] Adminrättigheter korrekta (vem har tillgång?)
- [ ] Tvåfaktorsautentisering på admin-konton
- [ ] Testordrar rensade/annullerade innan launch
- [ ] Testdata rensad (testprodukter, testkunder)

---

## 13. LAUNCH-CHECKLISTA (slutsteg)

- [ ] Lösenordsskydd borttaget
- [ ] Domän pekar rätt
- [ ] Alla testordrar rensade
- [ ] Alla mejlmallar granskade
- [ ] Betalningsflöde testat med riktig kund
- [ ] CSV-importprocess dokumenterad och testad
- [ ] Backup av tema sparad
- [ ] Överlämningsdokumentation klar till ReCarpet
- [ ] Supportkontakt definierad (vem fixar om något går fel?)

---

## SAMMANFATTNING INFÖR KUNDMÖTET

**Klart:**
```
[Lista vad som är klart]
```

**Kvarstår:**
```
[Lista vad som behöver fixas]
```

**Beslut som behövs från ReCarpet:**
```
[Lista beslutspunkter som kunden måste ta ställning till]
```

**Tidsuppskattning kvarvarande arbete:**
```
[Uppskatta tid]
```
