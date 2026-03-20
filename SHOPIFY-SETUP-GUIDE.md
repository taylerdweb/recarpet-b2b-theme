# reCarpet Shopify Admin Setup Guide

Everything that needs to be done manually in Shopify Admin after the theme code is deployed. Work through this top to bottom.

---

## 1. Create Pages (Online Store → Pages)

Create each page with the exact handle shown. After creating, assign the template from the "Theme template" dropdown.

| Page title | Handle (URL) | Template to assign |
|---|---|---|
| Om oss | `om-oss` | `page.om-oss` |
| Vad vi gör | `vad-vi-gor` | `page.vad-vi-gor` |
| Fastighetsägare | `fastighetsagare` | `page.fastighetsagare` |
| Arkitekter | `arkitekter` | `page.arkitekter` |
| Hyresgäst | `hyresgast` | `page.hyresgast` |
| Entreprenör | `entreprenor` | `page.entreprenor` |
| Kontakta oss | `kontakta-oss` | `page.kontakta-oss` |
| Integritetspolicy | `integritetspolicy` | `page` (default) |
| Köpvillkor | `kopvillkor` | `page` (default) |

**How to set the handle:** When editing a page, scroll down — the handle field appears below the title. Edit it to match exactly.

**How to assign the template:** While editing a page, look for "Theme template" in the right sidebar. Select the correct template from the dropdown.

---

## 2. Set Up Navigation (Online Store → Navigation)

### Main Menu

Edit the "Main menu" (or create one named `main-menu`). Build this structure:

```
Våra kunder  (dropdown, no link itself)
  ├── Fastighetsägare  → /pages/fastighetsagare
  ├── Arkitekter       → /pages/arkitekter
  ├── Hyresgäst        → /pages/hyresgast
  └── Entreprenör      → /pages/entreprenor

Vad vi gör  → /pages/vad-vi-gor

Våra golv  (dropdown, or link to /collections/all)
  ├── Återbrukade textilplattor  → /collections/aterbrukade-textilplattor
  └── Nya textilplattor          → /collections/nya-textilplattor

Om oss  → /pages/om-oss
```

The "Logga in" and "Kontakta oss" buttons are injected by the theme header code — you don't need to add them to the menu.

### Footer Menu (optional)

If you want the footer links to work, create a menu called `footer` with:
- Integritetspolicy → /pages/integritetspolicy
- Köpvillkor → /pages/kopvillkor
- Om oss → /pages/om-oss

---

## 3. Theme Customizer — Fill In Content

Go to **Online Store → Themes → Customize**. Work through each page/section below.

### Homepage (/)

Select "Home page" in the page selector dropdown.

**Section: reCarpet Hero**
- Background image: Upload a carpet/flooring hero image (or grab from recarpet.se)
- Heading: `Vi återbrukare textilplattor i stor skala`
- Subtext: `Från inventering och demontering till förmedling och montering — vi tar hand om hela processen.`
- Button 1: Label `Kom igång` → Link `/pages/kontakta-oss`
- Button 2: Label `Vad vi gör` → Link `/pages/vad-vi-gor`

**Section: reCarpet CTA Banner**
- Heading: `Ska du demontera eller föreskriva textilplattor?`
- Body: `Vi hjälper fastighetsägare, arkitekter och entreprenörer med hållbara golvlösningar.`
- Button 1: `Kontakta oss` → `/pages/kontakta-oss`
- Button 2: `Läs mer` → `/pages/vad-vi-gor`

**Section: reCarpet Logotyper**
- Heading: `Några av våra nöjda kunder`
- Add customer logo blocks — upload grayscale versions of customer logos

**Section: reCarpet Kundkort**
- Add 4 cards (blocks):
  1. Fastighetsägare — image, text about property management, link `/pages/fastighetsagare`
  2. Arkitekter — image, text about specification/design, link `/pages/arkitekter`
  3. Hyresgäst — image, text about tenant solutions, link `/pages/hyresgast`
  4. Entreprenör — image, text about installation, link `/pages/entreprenor`

**Section: reCarpet Tjänster**
- Fill in each service block with title, short description, and image
- Services: Inventering, Demontering, Förmedling, Montering, Service & underhåll, Internt återbruk
- All link to `/pages/vad-vi-gor`

**Section: reCarpet Produkter CTA**
- Image: Upload a product/carpet image
- Add 2 category blocks:
  1. Title: `Återbrukade textilplattor`, Tag: `ÅTERBRUK`, Link: `/collections/aterbrukade-textilplattor`
  2. Title: `Nya textilplattor`, Tag: `NY`, Link: `/collections/nya-textilplattor`

**Section: reCarpet Kontakt CTA**
- Heading: `Vill du cirkulera golv?`
- Body: `Beställ prover, boka en inventering eller ställ en fråga till oss!`
- Button 1: `Kontakta oss` → `/pages/kontakta-oss`

---

### Footer

In the theme customizer, scroll down to the footer group.

**Section: reCarpet Footer**
- Tagline: `Vi återbrukar textilplattor i stor skala för ett mer hållbart samhälle.`
- Phone: (your phone number)
- Email: `hej@recarpet.se`
- Address: (your address)
- LinkedIn URL: (your LinkedIn page URL)
- Fill in the 4 nav column blocks with titles and links (matching the nav structure above)

---

### Om oss page (/pages/om-oss)

Switch to the Om oss page in the customizer.

**Section: Page Hero**
- Eyebrow: `Om oss`
- Heading: `Vi är reCarpet`
- Subtext: `Sveriges ledande aktör för cirkulering av textilplattor.`
- Background image: Upload an office/team image

**Section: Om oss**
- Intro heading: `Vi tror på cirkulär ekonomi för golv`
- Fill in intro text, stat blocks (e.g. `500+ projekt`, `50 000+ m² återbrukade`)
- Mission heading and text

**Section: Logotyper** — reuse with customer logos

**Section: Kontakt CTA** — same as homepage

---

### Vad vi gör page (/pages/vad-vi-gor)

**Section: Page Hero**
- Eyebrow: `Tjänster`
- Heading: `Vad vi gör`
- Subtext: `En helhetslösning för återbruk av textilplattor — från inventering till montering.`

**Section: Vad vi gör**
- Fill in each of the 6 service blocks with full descriptions and images
- Service IDs (for #hash links in nav): inventering, demontering, formedling, montering, service, internt-aterbruk

---

### Kontakta oss page (/pages/kontakta-oss)

**Section: Page Hero**
- Heading: `Hur kan vi hjälpa dig?`

**Section: Kontakta oss**
- Phone: your phone number
- Email: `hej@recarpet.se`
- Address: your office address

---

### Customer group pages

Each page (Fastighetsägare, Arkitekter, Hyresgäst, Entreprenör) uses the same structure:

**Page Hero** — set eyebrow, heading, subtext, background image specific to that audience

**Kundgrupp section** — fill in:
- Intro heading + body text tailored to that customer group
- Intro image
- Add feature card blocks (2–4 per page) with images and descriptions
- Add stat blocks with relevant numbers
- CTA button linking to kontakta oss or relevant collection

---

## 4. Collections — Create if Missing

Make sure these collection handles exist:

| Collection | Handle |
|---|---|
| Återbrukade textilplattor | `aterbrukade-textilplattor` |
| Nya textilplattor | `nya-textilplattor` |

If they don't exist, go to **Products → Collections → Create collection** and set the handle manually.

---

## 5. Upload Images Checklist

Images to upload (go to **Content → Files** or use image pickers in the customizer):

- [ ] Homepage hero background (full-bleed, landscape, min 1600px wide)
- [ ] CTA banner background (optional)
- [ ] 4 × customer card images (Fastighetsägare, Arkitekter, Hyresgäst, Entreprenör)
- [ ] 6 × service timeline images (one per service)
- [ ] Products CTA image
- [ ] Customer logos (grayscale PNGs preferred, or color — theme applies grayscale via CSS)
- [ ] Om oss hero image
- [ ] Page hero images for each interior page
- [ ] Kundgrupp intro images (one per customer group page)
- [ ] Feature card images (2–4 per customer group page)

You can use images from the old recarpet.se site by right-clicking → Save image, then uploading them in Shopify.

---

## 6. Contact Form Email

Go to **Settings → Notifications** and verify the "Contact form" notification is set to send to the right email address (hej@recarpet.se or whoever should receive inquiries).

---

## 7. Final Checks

- [ ] Preview the theme on desktop and mobile before publishing
- [ ] Click through all nav links to make sure pages load correctly
- [ ] Submit a test contact form message
- [ ] Check the homepage hero displays correctly
- [ ] Verify the footer shows with dark green background (if the Dawn default footer still shows, check theme.liquid for the `.footer.gradient { display: none }` CSS)
- [ ] Check that the "Logga in" link in the header works (SparkLayer login)
- [ ] Verify collections pages load with products

---

## Summary of Files Created

| File | Purpose |
|---|---|
| `sections/rc-hero.liquid` | Homepage hero |
| `sections/rc-cta-banner.liquid` | Split CTA banner |
| `sections/rc-logo-bar.liquid` | Customer logos row |
| `sections/rc-customer-cards.liquid` | 4-column customer group cards |
| `sections/rc-services.liquid` | Alternating timeline services |
| `sections/rc-products-cta.liquid` | Products split + category cards |
| `sections/rc-contact-cta.liquid` | Full-width bottom CTA |
| `sections/rc-page-hero.liquid` | Interior page hero |
| `sections/rc-om-oss.liquid` | Om oss specific content |
| `sections/rc-vad-vi-gor.liquid` | Services detail page |
| `sections/rc-kundgrupp.liquid` | Reusable customer group landing |
| `sections/rc-kontakta-oss.liquid` | Contact page with form |
| `sections/rc-footer.liquid` | Dark green custom footer |
| `templates/index.json` | Homepage template |
| `templates/page.om-oss.json` | Om oss page |
| `templates/page.vad-vi-gor.json` | Vad vi gör page |
| `templates/page.fastighetsagare.json` | Fastighetsägare page |
| `templates/page.arkitekter.json` | Arkitekter page |
| `templates/page.hyresgast.json` | Hyresgäst page |
| `templates/page.entreprenor.json` | Entreprenör page |
| `templates/page.kontakta-oss.json` | Kontakta oss page |
