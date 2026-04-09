# reCarpet B2B – Action Points (from meeting 2026-04-09)

**Participants:** Erik Friis (Taylerd), Jonas Hallman & Hampus (reCarpet)
**Target launch:** End of April 2026

---

## 1. Product Filtering & Categories

- [ ] Add filtering for product types: **Återbruk** (reused), **Nytt material** (new), **Överblivet/Stuvbit/Räddat** (salvaged/end-of-series)
- [ ] Map these categories to Orak's existing tags (återbruk, utgående sortiment)
- [ ] Add a column in the product data sheets for category if not already present from Orak/Composil
- [ ] Ensure salvaged material is NOT labelled as "återbruk" (greenwash risk — Jonas was very clear on this)

## 2. Customer Groups — Simplified Structure

- [ ] **Remove Krets as a separate customer group** — Krets customers get Gold access instead
- [ ] Final customer groups: **Brons** (signup, pending approval), **Silver** (standard B2B), **Guld** (entrepreneurs + Krets partners)
- [ ] Krets gets access to all products (same as Gold) — no Krets-specific products on ReCarpet
- [ ] Keep Krets as a separate tag internally so their discount % can be adjusted independently later
- [ ] Confirm exact discount percentages per group with Jonas/Hampus (not finalized in meeting)

## 3. Signup & Account Approval Flow

- [ ] When a customer signs up → account created but **pending approval** (not auto-activated)
- [ ] Customer sees "pending" status when logged in — can browse but not order
- [ ] ReCarpet gets email notification with customer details
- [ ] Admin goes to Shopify → Customers → adds the right tag (b2b-silver, b2b-entrepreneur, etc.)
- [ ] Tagging triggers a welcome email to customer confirming their group and access
- [ ] **Write email copy** (currently placeholder) — Jonas/Hampus want Erik to provide a first draft they can adjust
- [ ] Add mandatory fields to signup: **company name, contact person, email, phone, business type/role**
- [ ] Remove "kundgrupp" from signup form — customers should not see tier names ("Alla kunder ska tro att de har bästa pris")
- [ ] Define the role/business type dropdown options (send to Jonas/Hampus for input)

## 4. Admin-Created Orders → Customer Editable (Sales Agent flow)

- [ ] **Core flow:** Admin builds order → saves as shopping list or draft → sends link to customer → customer edits and confirms
- [ ] Explore SparkLayer Sales Agent + Shopping Lists (partially validated today)
- [ ] The Shopify "Send Invoice" feature could double as an order confirmation/quote — customize the email copy
- [ ] Investigate: Can customer edit a draft order before paying? (Current Shopify drafts are view+pay only)
- [ ] This should work as an **offert (quote)** — customer can sit on it, come back later, adjust quantities
- [ ] Ensure the checkout goes through SparkLayer (invoice/faktura), NOT Shopify's payment checkout

## 5. Accounts — Customer Level (NOT project level)

- [ ] Decided: accounts are per **customer/company**, not per project
- [ ] Customers can invite sub-users to order under the same account
- [ ] Previous orders visible in account history across all projects

## 6. Services (Tjänster)

- [ ] Services available for order: **Rengöring**, **Montering**, **Demontering**
- [ ] Montering checkbox on product pages — already built and working ✓
- [ ] Services should ALSO be orderable standalone (not only as product add-on) — for internal reuse projects where customer buys montering without buying product
- [ ] Skip **underhållsavtal** (maintenance contracts) for now — handled by Composil, not ReCarpet
- [ ] Skip **förlängd garanti** — not relevant for launch

## 7. Product Data & Import Script

- [ ] Import script standardizes data from Orak, Composil, and Milliken into Shopify format ✓ (built)
- [ ] Script converts prices from EUR using daily exchange rate ✓
- [ ] Script generates price lists per currency (SEK, NOK, DKK, EUR) and per customer group ✓
- [ ] **Price markup:** ReCarpet adds 40% on top of supplier cost — configure in script
- [ ] **Rounding:** Always round prices UP (confirmed by Hampus)
- [ ] **SKU format:** `RCT-O-{id}` (Orak), `RCT-C-{id}` (Composil), `Milliken-{id}` (Milliken)
- [ ] Prislistor generated as CSV → manual upload to SparkLayer (for now)
- [ ] Products auto-uploaded to Shopify by script

## 8. Missing Product Data — Composil

- [ ] Composil data sheet is incomplete: missing dimensions, product images, technical data sheets
- [ ] Ask Composil for a more complete export (their website has the data — it should be extractable)
- [ ] Prioritize: at minimum get **images** and **dimensions** from Composil
- [ ] Not all fields need to match Orak — "what exists, exists"

## 9. Product Page Enhancements

- [ ] Show **stock/lager** on product cards in collection grid (Hampus: "väldigt gärna")
- [ ] Show **price per m²** on products in cart (noted during meeting)
- [ ] Add **EPD link** to all Orak products (same PDF for all — one link added via import script)
- [ ] Add reservation/disclaimer text for stock accuracy ("Reservation för lager" — stock updates weekly, actual availability may differ)
- [ ] **Beställ prov (order samples):** Only for Milliken products, as a CTA ("Kontakta oss för mer information") — NOT a direct order function
- [ ] Skip samples for Orak/Composil (too slow, product may be gone before sample arrives)

## 10. Invoicing & Fortnox

- [ ] Fortnox ↔ Shopify integration is limited (B2C-focused, doesn't create proper B2B invoices)
- [ ] **For now:** All invoice info lives in the Shopify order → ReCarpet manually creates invoice in Fortnox
- [ ] Checkout fields needed: **Organisationsnummer, faktura-epost, referensnummer/märkning**
- [ ] Future possibility: Build custom Fortnox integration (separate project, not for launch)

## 11. International Customers

- [ ] Customer tagging determines language + currency (Swedish, Norwegian, Danish, Euro)
- [ ] Admin selects VAT treatment per customer: normal moms or omvänd skattskyldighet (reverse charge)
- [ ] Price lists in all four currencies generated by import script ✓

## 12. Design & Site Structure

- [ ] Continue implementing old site design → new Shopify theme (in progress)
- [ ] Discuss simplifying "Våra kunder" from 4 separate pages to 1 (mentioned but deferred to written discussion)
- [ ] Add **onboarding experience** for first-time B2B login explaining what the customer has access to
- [ ] Add a **help button** (sticky, bottom-right) that adapts to the logged-in customer's group

## 13. Email Copy (all currently placeholders)

- [ ] Signup confirmation email ("ditt konto inväntar godkännande")
- [ ] Account approved email (per customer group — explains their access)
- [ ] Order confirmation email
- [ ] Invoice/draft order email
- [ ] Erik provides first draft → Jonas/Hampus review and adjust

## 14. Deliverables & Timeline

- [ ] Erik: Send summary email with all action points + questions (this document) — after meeting ✓
- [ ] Erik: Research the admin-creates-order → customer-edits flow in depth
- [ ] Erik: Give Jonas/Hampus access to staging site + admin panel (target: end of next week)
- [ ] Jonas/Hampus: Respond to all questions in the summary document
- [ ] Jonas/Hampus: Get updated/complete product data from Composil
- [ ] Jonas/Hampus: Get EPD link from Orak
- [ ] Jonas/Hampus: Confirm discount percentages per customer group
- [ ] Jonas/Hampus: Decide on Krets handling (Gold vs separate group) — leaning toward Gold
- [ ] **Target go-live: End of April 2026**
