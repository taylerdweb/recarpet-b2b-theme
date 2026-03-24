# reCarpet Shopify Theme — Pixel Perfect Redesign Prompt

Du är en senior Shopify-utvecklare. Din uppgift är att gå igenom reCarpet B2B-temats alla sidor och fixa dem till pixel perfect utifrån referenssidan https://www.recarpet.se/. Arbeta sida för sida i ordningen nedan. Varje sektion ska matchas mot originalsidan — scrapa text, struktur och layout från recarpet.se med Chrome-verktygen (navigate + get_page_text + screenshots) innan du gör ändringar.

Temat är byggt på Shopify Dawn med custom Liquid-sektioner (`sections/rc-*.liquid`) och JSON-templates (`templates/page.*.json`). Alla ändringar ska göras i Liquid/CSS — inga externa JS-bibliotek om det inte krävs för en specifik effekt.

---

## 0. FÖRBEREDELSE — Läs in projektet

Innan du börjar, läs alla relevanta filer:

```
sections/rc-hero.liquid
sections/rc-page-hero.liquid
sections/rc-logo-bar.liquid
sections/rc-customer-cards.liquid
sections/rc-services.liquid
sections/rc-products-cta.liquid
sections/rc-contact-cta.liquid
sections/rc-cta-banner.liquid
sections/rc-kundgrupp.liquid
sections/rc-kontakta-oss.liquid
sections/rc-om-oss.liquid
sections/rc-footer.liquid
sections/rc-vad-vi-gor.liquid
sections/header.liquid
sections/header-group.json
sections/footer-group.json
templates/index.json
templates/page.fastighetsagare.json
templates/page.hyresgast.json
templates/page.arkitekter.json
templates/page.entreprenor.json
templates/page.vad-vi-gor.json
templates/page.om-oss.json
templates/page.kontakta-oss.json
config/settings_schema.json
config/settings_data.json
```

Ta sedan screenshots av referenssidan https://www.recarpet.se/ (och varje undersida) som visuell referens innan du börjar ändra kod.

---

## 1. GLOBALA DESIGNFIXAR (gör dessa först — de påverkar alla sidor)

### 1.1 Typografi
- Font: **DM Sans** (verifiera att `--rc-font: 'DM Sans', sans-serif` används överallt)
- Gå till https://www.recarpet.se/ och inspektera fontsizes i Chrome DevTools eller via screenshot-jämförelse
- Uppdatera alla sektioner med korrekta storlekar för:
  - **H1** (hero-rubriker): jämför med referenssidan
  - **H2** (sektionsrubriker): ett snäpp större än nuvarande — referera till recarpet.se
  - **H3** (kort-rubriker): matcha referens
  - **Body text**: matcha referens (troligen 16-17px)
  - **Small/labels**: matcha referens (troligen 13-14px)
- Se till att `font-weight` stämmer: rubriker 500-700, body 400

### 1.2 Färger
Den gröna brandfärgen är **off** i nuvarande tema. Gå till recarpet.se, inspektera den exakta gröna färgen och uppdatera:
- `--rc-green` (nuvarande: `#174237` — verifiera och korrigera mot referenssidans faktiska gröna)
- `--rc-green-hover` (justera därefter)
- `--rc-cream`: `#F0EFEB` (verifiera)
- `--rc-orange`: `#E05A0C` (verifiera)
- Uppdatera i alla sektioner som hardcodar dessa värden

### 1.3 Knappar — border-radius
- Alla knappar ska ha korrekt `border-radius` — inspektera referenssidan och standardisera:
  - `.rc-btn`, `.rc-btn--primary`, `.rc-btn--outline`, etc.
  - Outline-knappar ska ha `1px border` (inte 2px eller tjockare)
- Se till att border-radius är konsekvent i alla sektioner (troligen 4px eller 6px — matcha referens)

### 1.4 Max-bredd
- Nuvarande max-width: `1200px` — öka till bredare (inspektera referenssidan, troligen `1280px` eller `1400px`)
- Uppdatera `max-width` i alla `.rc-*__inner` containers
- Uppdatera sidpadding så det matchar (48px → justera om max-width ökas)

---

## 2. NAVIGATION (sections/header.liquid + header-group.json)

### 2.1 Hover-öppning
- Dropdown-menyer ska öppnas på **hover**, inte på klick
- Implementera CSS `:hover` på `.header__menu-item` för att visa dropdown
- Behåll klick-stöd för touch/mobil

### 2.2 Logotyp istället för "Recarpet build"
- Byt ut text-logotypen "Recarpet build" mot den faktiska reCarpet SVG/PNG-logotypen
- Logotypen finns redan i projektet (kontrollera `assets/` eller Shopify-inställningarna i `config/settings_data.json` under logo)
- Om den inte finns: se till att Shopify Theme Settings logo-inställningen (`settings_schema.json` → logo image_picker) används istället för hårdkodad text
- Undersök om store name kan ändras i Shopify Admin → Settings → Store details, och notera det som instruktion till användaren

### 2.3 Navigationsstruktur
Verifiera att menyn matchar denna struktur (från recarpet.se):
- **Våra kunder** (dropdown): Fastighetsägare, Arkitekter, Hyresgäster, Entreprenörer
- **Vad vi gör** (dropdown): Inventering, Demontering, Förmedling, Montering, Service & underhåll, Internt återbruk
- **Våra textilplattor** (dropdown): Återbrukade textilplattor, Nya textilplattor (Milliken)
- **Om oss** (direktlänk)
- **Kontakta oss** (direktlänk)

Om navigationsstrukturen styrs av Shopify-menyer (Menus i admin), notera det som en manual setup-instruktion. Om det styrs av header-group.json, uppdatera filen.

---

## 3. STARTSIDA (templates/index.json + relevanta sektioner)

Referens: https://www.recarpet.se/
Ta en fullskalig screenshot av startsidan som referens.

### 3.1 Hero (sections/rc-hero.liquid)
- **Hero-bild syns inte** — felsök: kontrollera att bildinställningen i `index.json` pekar på en giltig bild. Om bilden saknas i Shopify, lägg till en placeholder-kommentar och notera att bilden behöver laddas upp manuellt
- **Rubriker syns inte** — felsök: kontrollera att heading/subtext settings har värden i `index.json`. Verifiera att CSS:en inte döljer texten (kolla `color`, `z-index`, `position`, `display`)
- **Ta bort "Kontakta oss"-knappen** — ta bort den andra CTA-knappen från hero-sektionen (behåll bara primärknappen)
- Matcha rubriktext mot referens: "Professionell hantering av återbrukade och nya textilplattor"
- Matcha underrubrik: "ReCarpet är specialister på demontering, kvalitetssäkring och leverans av textilplattor. För cirkulära lösningar i både ombyggnad och nyproduktion"

### 3.2 Sektion 2 — CTA-banner + Logotyper (rc-cta-banner.liquid + rc-logo-bar.liquid)
- **Bakgrund: vit** — ändra bakgrundsfärgen på rc-cta-banner från `var(--rc-cream)` till `#fff` / `var(--rc-white)`
- **Kundloggor saknas** — notera i prompten att logotypbilder behöver laddas upp manuellt till Shopify. Skapa image_picker settings i rc-logo-bar.liquid schemat om de inte redan finns
- Matcha layout mot referens: "Önskar du boka en demontering eller vill du föreskriva textilplattor?" + kundloggor under

### 3.3 Sektion 3 — Kundkort "Vi har lösningar för era behov" (rc-customer-cards.liquid)
- **Bakgrund: beige** (`var(--rc-cream, #F0EFEB)`) — verifiera att detta redan stämmer
- **Korten ska INTE ha vit bakgrund** — ta bort `background: #fff` från korten. Korten ska vara "platta" mot den beiga bakgrunden (transparent eller samma beige)
- **Centrerad rubrik och text** — lägg till `text-align: center` på sektionens rubrik och beskrivning
- **Rubrik ett snäpp upp i storlek** — öka sektionsrubrikens font-size (t.ex. från `clamp(28px, 3vw, 40px)` till `clamp(32px, 3.5vw, 48px)`)
- **Centrera knappen i kortet** — lägg till `text-align: center` eller `justify-content: center` på kortets CTA-area

### 3.4 Sektion 4 — Tjänster (rc-services.liquid)
- **Knappar: 1px border** — alla outline-knappar i denna sektion ska ha exakt `border: 1px solid`
- **Vertikal tidslinje med scroll-indikator:**
  - Behåll den nuvarande vertikala linjen i mitten med punkter vid varje tjänst
  - **Lägg till en scroll-driven progress-linje**: en tjockare linje i brandfärgen (`--rc-green`) som fyller sig nedåt i takt med att användaren scrollar genom sektionen
  - Implementera med JavaScript `IntersectionObserver` eller `scroll` event:
    1. Beräkna sektionens scroll-progress (0% till 100%)
    2. Applicera progress på en `::before` pseudo-element eller ett separat `<div>` ovanpå den grå linjen
    3. Linjen ska vara tjockare än baslinjen (t.ex. 3-4px vs 1px)
    4. Punkten vid varje tjänst ska "aktiveras" (t.ex. byta färg eller skala) när den passeras
  - Dölj tidslinjen på mobil (redan implementerat)

### 3.5 Sektion 5 — Sortiment (rc-products-cta.liquid)
- Markerad som **"bra"** — inga ändringar krävs. Verifiera bara att fontsizes matchar referenssidan.

### 3.6 Sektion 6 — Kontakt-CTA (rc-contact-cta.liquid)
- **Bakgrund: vit** — ändra från `var(--rc-cream)` till `#fff` / `var(--rc-white)`

---

## 4. FOOTER (sections/rc-footer.liquid + footer-group.json)

- **Ta bort tagline** — ta bort texten "Specialister på demontering, kvalitetssäkring och leverans av textilplattor." från footerns brand-kolumn
- Verifiera att footer-strukturen matchar referens:
  - Kolumn 1: Logo + adress + kontaktinfo
  - Kolumner 2-5: Navigeringslänkar (Våra kunder, Vad vi gör, Våra golv, Kontakta ReCarpet)
  - Botten: © 2025 ReCarpet + Integritetspolicy + Köpvillkor

---

## 5. FASTIGHETSÄGARE (templates/page.fastighetsagare.json + sections/)

Referens: https://www.recarpet.se/fastighetsagare
Scrapa all text från denna sida först.

### 5.1 Hero (rc-page-hero.liquid)
- **Bild och text syns inte** — samma felsökning som startsidans hero. Kontrollera JSON-settings, bild-URL, och CSS visibility
- Matcha rubrik: "För fastighetsägare"
- Matcha underrubrik: "Vi tar ansvar för hela processen – maximerat utfall, minimerat avfall"

### 5.2 Sektion 2 — "Fastighetsägare" intro
- **Kan tas bort** — samma innehåll som hero. Ta bort denna sektion från `page.fastighetsagare.json`

### 5.3 Sektion 3 — "Våra tjänster för fastighetsägare" (rc-kundgrupp.liquid feature cards)
- **Korten ska INTE ha vit bakgrund** — ta bort vit bakgrund från feature cards. Matcha mot referenssidans utseende
- **Rätt fontsizes** — inspektera referens och uppdatera
- **Rubrik ett snäpp upp** — öka sektionsrubrikens storlek

### 5.4 Sektion 4 — CO₂-statistik
- **Se över hur denna sektion byggs på nuvarande site** — scrapa exakt layout från recarpet.se/fastighetsagare
- Uppdatera rc-kundgrupp.liquid stats-sektionen eller skapa en ny sektion om det krävs
- **Fontsizes** — matcha referens
- **Bilder saknas** — notera vilka bilder som behövs. Sätt placeholder och dokumentera
- Innehåll från referens:
  - Rubrik: "Minska CO₂-utsläppen och kostnaderna med ReCarpet"
  - Stats: 70% (textilplattor av CO2), 6 kg CO₂/m² (ReCarpet), 7,1 kg CO₂/m² (Deponi)

### 5.5 Sektion 5 — "Kunskap om produkternas potential" — SAKNAS HELT
- **Skapa ny sektion eller utöka rc-kundgrupp.liquid** med stöd för denna typ av content-block
- Innehåll att scrapa från recarpet.se/fastighetsagare:
  - Rubrik: "Kunskap om produkternas potential ger nöjda kunder och hållbara lokaler"
  - Brödtext om nätverk och kundbehov
  - CTA: "Boka inventering eller kontakta oss för återbruk"
- Layout: text-sektion med vit/beige bakgrund, rubrik + brödtext + CTA-knapp

### 5.6 Sektion 6 — "Hållbarhet" — SAKNAS HELT
- **Skapa ny sektion eller block** för denna content
- Innehåll att scrapa:
  - Rubrik: "Hållbarhet"
  - Underrubrik: "Nå era hållbarhetsmål med ReCarpet"
  - Brödtext om koldioxidbesparing per återanvänd kvadratmeter
  - CTA: "Boka demontering"
- Layout: matcha referenssidans design

### 5.7 Sektion 7 — "Ett hållbart golvalternativ" — SAKNAS HELT
- **Skapa ny sektion eller block** för Milliken-information
- Innehåll att scrapa:
  - Rubrik: "Ett hållbart golvalternativ"
  - Underrubrik: "Milliken – Marknadens mest hållbara textilplatta"
  - Brödtext om TractionBack-teknik och cirkulära fördelar
  - CTA: "Kontakta oss" + "Se Millikens plattor här"
- Layout: 2-kolumn med bild + text, matcha referens

---

## 6. HYRESGÄSTER (templates/page.hyresgast.json + sections/)

Referens: https://www.recarpet.se/hyresgast
Scrapa all text.

### 6.1 Hero
- **Content syns inte** — felsök (samma som ovan)
- Rubrik: "För hyresgäster"
- Underrubrik: "Uppgradera kontorsgolvet – enkelt och prisvärt!"

### 6.2 Ta bort "Vad vi behöver"-sektion
- Om det finns en sektion som upprepar hero-content eller listar krav, **ta bort den** från template JSON

### 6.3 Citat-sektion — SAKNAS
- **Skapa en ny sektion `sections/rc-quote.liquid`** (eller lägg till som block i befintlig sektion)
- Innehåll från referens:
  - Citat: "Vi har fått återbrukade textilplattor installerade av ReCarpet och vi är mycket nöjda. Snabb service och kvaliteten och stilen överträffade våra förväntningar."
  - Attribution: "Rasmus Andersson, VD och grundare"
- Design: stor kursiv text, ev. vänster border-accent i brandfärg, centrerad layout
- Gör sektionen generisk så den kan återanvändas på andra sidor
- Lägg till i `page.hyresgast.json` på rätt position

---

## 7. ARKITEKTER (templates/page.arkitekter.json + sections/)

Referens: https://www.recarpet.se/arkitekter
Scrapa all text.

### 7.1 Hero
- **Content syns inte** — felsök
- Rubrik: "För arkitekter"
- Underrubrik: "Utforska vårt sortiment och beställ prover"

### 7.2 Sektion 2 — "För arkitekter"
- **Upprepar hero-content — kan tas bort helt**
- Ta bort från `page.arkitekter.json`

### 7.3 Resterande innehåll
- Verifiera att kvarvarande sektioner matchar referenssidans innehåll:
  - Produktguide ("Våra mattor" / "Ta steget – Vi hjälper dig!")
  - Två produktkategorier (Återbrukade + Nya textilplattor)
  - "ReCarpet — helhetsansvar för storskaligt återbruk"
- Uppdatera text i JSON om den avviker

---

## 8. ENTREPRENÖRER (templates/page.entreprenor.json + sections/)

Referens: https://www.recarpet.se/entreprenorer
Scrapa ALL text — denna sida har flest saknade sektioner.

### 8.1 Hero
- **Content syns inte** — felsök
- Rubrik: "För entreprenörer"
- Underrubrik: "Vi säkerställer rätt produkt, i rätt tid, med minimerat avfall"

### 8.2 Gå igenom hela sidan och implementera saknade sektioner
Referenssidan har dessa sektioner — skapa det som saknas:

1. **Hero** (finns, men content syns inte — fixa)
2. **CTA-block** — "Har du ett projekt med föreskrivna återbrukade textilplattor? Kontakta oss!"
3. **Tre fördelskort** — Hållbar helhetslösning, Prisvärda kvalitetsgolv, Smidigt samarbete
4. **Certifiering** — "ReCarpet Certifierad ÅterbruksPartner" + info om 5 kr/m² donation
5. **Produktfördelar** — "Fördelarna med ReCarpets textilplattor" + "Skapa en bättre miljö med återbrukade textilplattor"
6. **FAQ-sektion** — "Vanliga frågor" med 4 frågor och svar (implementera som collapsible/accordion):
   - Hur monterar man återbrukade textilplattor?
   - Har ni garanti på materialet?
   - Hur kommer slutresultatet bli?
   - Kan man få en provbit för att visa kund?
7. **Galleri** — "Se bilder från våra tidigare återbruksprojekt" (bildplats)
8. **Partner-CTA** — "Bli en del av en hållbar byggbransch" med avslutande text

Skapa nya Liquid-sektioner om rc-kundgrupp.liquid inte kan stödja alla dessa block-typer. Uppdatera `page.entreprenor.json` med alla sektioner i rätt ordning.

---

## 9. VAD VI GÖR / TJÄNSTER (templates/page.vad-vi-gor.json + sections/rc-vad-vi-gor.liquid)

Referens: https://www.recarpet.se/tjanster
Ta en screenshot av hela sidan, speciellt den övre navigationen.

### 9.1 Tidslinjenavigation (ersätter den nuvarande under-navigationen)
- Den horisontella navigeringen längst upp (som nu fungerar som snabblänkar till tjänster) ska **byggas om till en tidslinje-stil**
- Inspektera exakt hur recarpet.se visar detta: troligen en horisontell linje med steg/noder
- Implementera som:
  - Horisontell linje med numrerade steg eller noder
  - Varje nod = en tjänst (Inventering → Demontering → Förmedling → Montering → Service → Internt återbruk)
  - Klickbar — scrollar ner till rätt sektion
  - Sticky (fastnar under headern vid scroll)
- Behåll den gröna bakgrundsfärgen men ändra layouten till tidslinje

### 9.2 Tjänstekortens copy
- **Fixa till texten** — scrapa exakt copy från recarpet.se/tjanster för varje tjänst:
  1. **Inventering**: korrekt rubrik, underrubrik, punktlista med fördelar, CTA
  2. **Demontering**: korrekt rubrik, underrubrik, punktlista, CTA
  3. **Förmedling**: korrekt innehåll
  4. **Montering**: korrekt innehåll + "Våra samarbetspartners finns i hela landet"
  5. **Service & underhåll**: korrekt innehåll
  6. **Internt återbruk**: korrekt innehåll + dubbla CTA-knappar
- Uppdatera alla textblock i `page.vad-vi-gor.json` med exakt text från referenssidan

---

## 10. OM OSS (templates/page.om-oss.json + sections/rc-om-oss.liquid)

Referens: https://www.recarpet.se/om-oss
**Gå igenom sidan ordentligt och implementera allt.** Scrapa all text.

Referenssidans fulla struktur:

1. **Hero** — "Om oss" / "Välkommen till ReCarpet" + multi-paragraph intro om grundandet 2022
2. **Grundarcitat** — "Vi demonterar inte bara golven – vi cirkulerar dem!" / Jonas Hallman
3. **Team** — Två medlemmar:
   - Jonas Hallman (Ägare) — bio + kontaktinfo
   - Tim Aronsson (Försäljningschef) — bio + kontaktinfo
4. **Statistik/uppnått** — "Sedan start har vi demonterat och förmedlat 40.000m² textilplattor..."
5. **Projektportfölj** — "Några av våra lyckade projekt:" med tre kategorier:
   - Demontering: Kv Yrket (NCC), Upplands Väsby Kommunhus (ByggDialog), Kåkenhusen (Huvudstaden)
   - Återbrukade: Veidekke HK, Skanska HK, Vossloh
   - Milliken: Deloitte HK, Meta HK, Disney HK
6. **Filosofi** — citat om produktkunskap och byggnation
7. **Nyckeltal** — 4 kort: 2022 (Grundat), 40.000m² (Återbrukade), 450 ton (Undviket avfall), 100+ (Nöjda kunder)
8. **Tjänstesammanfattning** — lista av tjänster + "Se våra tjänster" + "Gör en offertförfrågan"
9. **Vision** — "Vår vision" — text om cirkulära textilplattor
10. **Hållbarhetslösning** — "En hållbar lösning" / "Hållbara golv är vår passion"
11. **Avslutande CTA** — "Kontakta oss för ditt mattprojekt" + "Kroka arm med oss idag. Tiden är knapp!"

Utöka `rc-om-oss.liquid` eller skapa kompletterande sektioner för att täcka ALLA dessa. Den nuvarande sektionen har bara intro + stats + mission — det saknas team-bios, projektportfölj, filosofi, vision, och mer.

Uppdatera `page.om-oss.json` med alla sektioner och korrekt text.

---

## 11. KONTAKTA OSS (templates/page.kontakta-oss.json + sections/rc-kontakta-oss.liquid)

Referens: https://www.recarpet.se/kontakta-oss
Scrapa alla formulärfält och kontaktinfo.

### 11.1 Ta bort hero
- Ta bort `rc-page-hero` från `page.kontakta-oss.json` (kontaktsidan ska INTE ha en hero-banner)

### 11.2 Formulärfält — se till att ALLA finns
Nuvarande formulär har: Namn, Email, Telefon, Ämne (select), Meddelande.
Referenssidan har dessa fält — uppdatera formuläret i rc-kontakta-oss.liquid:

1. **Namn** (text, required)
2. **Företag** (text, required) — **SAKNAS i nuvarande**
3. **Email** (email, required)
4. **Telefonnummer** (tel, required)
5. **"Välj vad du vill ha hjälp med"** (radio buttons, single select) — **byt från select/dropdown till radio buttons**:
   - Fråga pris
   - Beställa prov
   - Inventering
   - Föreskriftsfrågor
   - Demontering
   - Boka möte
   - Produktfråga
   - Service & Underhåll
   - Samarbeten
   - Annat
6. **Meddelande** (textarea, required)
7. **"Jag accepterar Integritetspolicyn"** (checkbox, required) — **SAKNAS i nuvarande**

### 11.3 Kontaktpersoner
Verifiera att kontaktinfo stämmer:
- Jonas Hallman — Demonteringar, Samarbeten — 070-073 36 82 — jonas@recarpet.se
- Tim Aronsson — Försäljningschef — 070-073 36 81 — tim.aronsson@recarpet.se

### 11.4 Logobanner i botten
- **Lägg till rc-logo-bar sektionen** i `page.kontakta-oss.json` efter formuläret
- Rubrik: "Några av våra nöjda kunder"
- Samma logo-bar som på startsidan — återanvänd sektionen

---

## 12. VERIFIERING

När alla sidor är klara:

1. Gå igenom varje sida på Shopify-preview och ta screenshots
2. Jämför sida vid sida med recarpet.se
3. Kontrollera specifikt:
   - Alla hero-bilder och rubriker syns
   - Korrekt typografi (fontsizes, weights)
   - Korrekt färger (grön, cream, orange)
   - Knappar har rätt border-radius och 1px border där det gäller
   - Max-width känns rätt
   - Nav öppnas på hover
   - Logotyp visas istället för "Recarpet build"
   - Alla formulärfält finns på kontaktsidan
   - Footer saknar tagline-texten
   - Logobanner finns på kontaktsidan
4. Dokumentera eventuella bilder som behöver laddas upp manuellt

---

## VIKTIGA REGLER

- **Scrapa alltid text från recarpet.se** innan du skriver content — gissa inte
- **Ändra INTE sektioner som markeras som "bra"** (t.ex. sortiment-sektionen)
- **Skapa nya sektioner** när befintliga inte kan utökas (t.ex. FAQ, citat, team-bios)
- **Uppdatera JSON-templates** med korrekt content och nya sektioner
- **Bibehåll Shopify-kompatibilitet** — alla nya sektioner ska ha korrekt `{% schema %}` med settings
- **Responsivitet** — alla ändringar ska fungera på mobil, tablet och desktop
- **Bilder** — för saknade bilder, använd placeholder image settings i schema och dokumentera vilka bilder som behöver laddas upp
- **Testa varje sida** efter ändringar genom att ta screenshots och jämföra med referenssidan
