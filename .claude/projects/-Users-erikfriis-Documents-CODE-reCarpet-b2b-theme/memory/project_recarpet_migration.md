---
name: reCarpet Webflow to Shopify Migration
description: Full project context for migrating recarpet.se from Webflow to Shopify Dawn theme with pixel-perfect parity
type: project
---

Migrating reCarpet B2B carpet service website from Webflow to Shopify (Dawn theme base). Goal is pixel-perfect parity with recarpet.se.

**Why:** Business moving to Shopify for B2B e-commerce capabilities (SparkLayer integration).

**How to apply:**
- Source of truth for visuals/CSS: Webflow export at `recarpet-d673fe83bfacb.webflow/`
- Figma design file: `https://www.figma.com/design/tfNwN1kk9YZ2QAaoCjhmER/ReCarpet?node-id=6498-4527&m=dev`
- All custom sections prefixed `rc-*`, all tokens in `snippets/rc-global-styles.liquid`
- Key patterns: transparent navbar with scroll-toggle JS, sections use `margin-top: -72px; padding-top: 72px`, hero uses `::after` overlay, full-bleed kundgrupp uses `calc(max(48px, (100vw - var(--rc-max-width)) / 2))`
- Breakpoints: 991px tablet, 767px mobile landscape, 479px mobile portrait
- Known bug: `--rc-orange: #E05A0C` missing from global styles but referenced in `rc-products-cta.liquid` line ~98

**Remaining work (as of 2026-03-24):**
- Fix --rc-orange bug
- Pixel-perfect QA against Webflow export and Figma
- Upload images to Shopify
- Navigation menu setup in Shopify Admin
- Store name change from "recarpet-build"
- SparkLayer cleanup
- Montering auto-add to cart feature
- Responsive QA across all breakpoints
