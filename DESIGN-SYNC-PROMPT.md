# reCarpet Shopify Theme — Design Token Sync Prompt

Use this prompt to align the Shopify Dawn theme (reCarpet B2B) with the production Webflow site at recarpet.se. The Webflow export lives in `recarpet-d673fe83bfacb.webflow/` within this repo and is the source of truth for all visual design decisions.

---

## Context

We are rebuilding recarpet.se as a Shopify store using the Dawn theme. All custom sections use the `rc-` prefix and share a single design-token file: `snippets/rc-global-styles.liquid`. The goal is pixel-perfect visual parity with the Webflow site.

---

## Task

Update `snippets/rc-global-styles.liquid` and every `sections/rc-*.liquid` file so that colors, typography, spacing, border-radius, and max-widths match the Webflow source CSS exactly. Set up a proper variable/token system so future tweaks can be made in one place.

---

## 1. Design Tokens — update `snippets/rc-global-styles.liquid`

Replace the current `:root` block with the full token set below. These values come directly from the Webflow export CSS (`recarpet-d673fe83bfacb.webflow.css`).

### Colors

```css
:root {
  /* Brand */
  --rc-green: #1e4433;           /* rc-re-green — primary brand */
  --rc-green-hover: #264f3f;     /* slightly lighter for hover states */
  --rc-sage: #6c9985;            /* rc-sage-green — secondary green */
  --rc-yellow: #edb81e;          /* rc-yellow — accent */
  --rc-beige: #e6e3de;           /* rc-beige — warm neutral bg */
  --rc-off-white: #f6f6f6;       /* rc-white — light bg */
  --rc-off-black: #121212;       /* rc-off-black — primary text */
  --rc-white: #ffffff;
  --rc-black: #000000;

  /* Neutrals */
  --rc-neutral-lightest: #eeeeee;
  --rc-neutral-lighter: #cccccc;
  --rc-neutral-light: #aaaaaa;
  --rc-neutral: #666666;
  --rc-neutral-dark: #444444;
  --rc-neutral-darker: #222222;

  /* Semantic */
  --rc-text: var(--rc-off-black);
  --rc-text-muted: var(--rc-neutral);  /* was #555 — Webflow uses #666 */
  --rc-bg-primary: var(--rc-white);
  --rc-bg-secondary: var(--rc-off-white);
  --rc-bg-alt: var(--rc-beige);
  --rc-border: var(--rc-neutral-light);
}
```

### Typography

```css
:root {
  /* Font family */
  --rc-font: 'DM Sans', sans-serif;

  /* Heading sizes (from .heading-style-h* classes) */
  --rc-h1: 56px;     /* 3.5rem */
  --rc-h2: 48px;     /* 3rem */
  --rc-h3: 40px;     /* 2.5rem */
  --rc-h4: 32px;     /* 2rem */
  --rc-h5: 24px;     /* 1.5rem */
  --rc-h6: 20px;     /* 1.25rem */

  /* Heading weight: h1–h4 = 500, h5–h6 = 700 */
  --rc-heading-weight: 500;
  --rc-heading-weight-bold: 700;
  --rc-heading-lh: 1.2;

  /* Body text sizes */
  --rc-text-base: 1rem;        /* 16px */
  --rc-text-sm: 0.875rem;      /* 14px */
  --rc-text-xs: 0.75rem;       /* 12px */
  --rc-text-md: 1.125rem;      /* 18px */
  --rc-text-lg: 1.25rem;       /* 20px */
  --rc-body-lh: 1.5;
  --rc-body-weight: 400;
}
```

### Layout & Spacing

```css
:root {
  /* Container */
  --rc-max-width: 80rem;       /* 1280px — matches .container-large */
  --rc-page-padding: 5%;       /* horizontal — matches .padding-global */

  /* Section vertical padding */
  --rc-section-lg: 7rem;       /* 112px — .padding-section-large */
  --rc-section-md: 5rem;       /* 80px  — .padding-section-medium */
  --rc-section-sm: 3rem;       /* 48px  — .padding-section-small */

  /* Border radius */
  --rc-radius: 8px;            /* buttons, cards, images */
  --rc-radius-sm: 4px;
  --rc-radius-lg: 12px;
}
```

### Buttons

```css
.rc-btn {
  font-family: var(--rc-font);
  font-size: var(--rc-text-base);
  font-weight: 500;
  line-height: 1.4;
  padding: 0.75rem 1.5rem;       /* 12px 24px */
  border-radius: var(--rc-radius); /* 8px */
  border: 1px solid transparent;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Primary — green bg */
.rc-btn--primary {
  background: var(--rc-green);
  color: var(--rc-white);
  border-color: var(--rc-green);
}
.rc-btn--primary:hover {
  background: var(--rc-green-hover);
  border-color: var(--rc-green-hover);
}

/* Secondary / outline — transparent bg, green border */
.rc-btn--outline {
  background: transparent;
  color: var(--rc-green);
  border-color: var(--rc-green);
}
.rc-btn--outline:hover {
  background: var(--rc-green);
  color: var(--rc-white);
}

/* Outline white — for use on dark/image backgrounds */
.rc-btn--outline-white {
  background: transparent;
  color: var(--rc-white);
  border-color: rgba(255,255,255,0.85);
}
.rc-btn--outline-white:hover {
  background: rgba(255,255,255,0.15);
}

/* Small button variant */
.rc-btn--sm {
  padding: 0.5rem 1.25rem;
  font-size: var(--rc-text-sm);
}

/* Link-style button */
.rc-btn--link {
  padding: 0.25rem 0;
  background: transparent;
  border: none;
  color: var(--rc-green);
  line-height: 1;
}
```

---

## 2. Global base styles — add to `rc-global-styles.liquid`

Apply the font and heading tokens globally so all `rc-*` sections inherit correct typography without repeating values:

```css
/* Apply DM Sans globally to rc sections */
[class^="rc-"], [class*=" rc-"] {
  font-family: var(--rc-font);
}

/* Heading resets for rc sections */
.rc-h1, [class^="rc-"] h1 { font-size: var(--rc-h1); font-weight: var(--rc-heading-weight); line-height: var(--rc-heading-lh); color: var(--rc-text); }
.rc-h2, [class^="rc-"] h2 { font-size: var(--rc-h2); font-weight: var(--rc-heading-weight); line-height: var(--rc-heading-lh); color: var(--rc-text); }
.rc-h3, [class^="rc-"] h3 { font-size: var(--rc-h3); font-weight: var(--rc-heading-weight); line-height: var(--rc-heading-lh); color: var(--rc-text); }
.rc-h4, [class^="rc-"] h4 { font-size: var(--rc-h4); font-weight: var(--rc-heading-weight); line-height: 1.3; color: var(--rc-text); }
.rc-h5, [class^="rc-"] h5 { font-size: var(--rc-h5); font-weight: var(--rc-heading-weight-bold); line-height: 1.4; color: var(--rc-text); }
.rc-h6, [class^="rc-"] h6 { font-size: var(--rc-h6); font-weight: var(--rc-heading-weight-bold); line-height: 1.4; color: var(--rc-text); }

/* Body text */
[class^="rc-"] p, [class^="rc-"] li {
  font-size: var(--rc-text-base);
  line-height: var(--rc-body-lh);
  font-weight: var(--rc-body-weight);
  color: var(--rc-text-muted);
}
```

---

## 3. Section-by-section updates

Go through every `sections/rc-*.liquid` file and:

1. **Replace hard-coded colors** with CSS variables (e.g. `#1E4433` → `var(--rc-green)`, `#555555` → `var(--rc-text-muted)`, `#F6F6F6` → `var(--rc-bg-secondary)`, `#E6E3DE` → `var(--rc-bg-alt)`)
2. **Replace hard-coded font sizes** with variables (e.g. `font-size: 48px` → `font-size: var(--rc-h2)`, `font-size: 16px` → `font-size: var(--rc-text-base)`)
3. **Replace hard-coded max-widths** — `max-width: 1280px` → `max-width: var(--rc-max-width)`
4. **Replace hard-coded padding** — `padding: 0 48px` → `padding: 0 var(--rc-page-padding)`, section vertical padding → use `var(--rc-section-md)` or appropriate size
5. **Replace hard-coded border-radius** — `border-radius: 8px` → `border-radius: var(--rc-radius)`
6. **Font weights** — ensure h1–h4 headings use weight 500 (not 700), and h5–h6 use weight 700
7. **Font family** — ensure DM Sans is applied via `var(--rc-font)` wherever it was hardcoded

### Files to update (all in `sections/`):

- `rc-hero.liquid` — heading, subtext, overlay, CTA
- `rc-kundgrupp.liquid` — intro heading, body, feature cards, stats
- `rc-content-block.liquid` — heading, body text
- `rc-faq.liquid` — heading, question/answer text
- `rc-quote.liquid` — quote text, attribution
- `rc-om-oss.liquid` — headings, body, team cards
- `rc-page-hero.liquid` — heading, subtext
- Any other `rc-*.liquid` files in the sections folder

---

## 4. Navbar alignment

In `sections/header.liquid`, ensure:

- Nav links use `font-family: var(--rc-font)` (DM Sans)
- Nav link color: `var(--rc-off-black)` (#121212)
- Nav link line-height: 120%
- Nav link padding: `1.5rem 1rem`
- Logo max-width: `120px`
- Header background: `var(--rc-off-white)` (#f6f6f6)
- Header border-bottom: `1px solid var(--rc-off-black)` (Webflow uses black border, not light gray)

---

## 5. Responsive breakpoints

Match the Webflow breakpoints:

- **Tablet**: `max-width: 991px`
  - `--rc-section-md` → 4rem, `--rc-section-lg` → 6rem
  - Headings scale down proportionally
- **Mobile landscape**: `max-width: 767px`
- **Mobile portrait**: `max-width: 479px`
  - `--rc-section-sm` → 2rem, `--rc-section-md` → 3rem, `--rc-section-lg` → 4rem

---

## 6. Verification checklist

After implementation, verify:

- [ ] All `rc-*` sections render in DM Sans
- [ ] Heading sizes match: h1=56px, h2=48px, h3=40px, h4=32px, h5=24px, h6=20px
- [ ] Heading weights: h1-h4 = 500, h5-h6 = 700
- [ ] Body text: 16px, weight 400, line-height 1.5, color #666
- [ ] Primary green is exactly #1e4433
- [ ] Buttons have 8px border-radius, 12px 24px padding
- [ ] Content max-width is 80rem (1280px) with 5% horizontal page padding
- [ ] Section padding uses the three-tier system (sm/md/lg)
- [ ] No hard-coded color values remain in any `rc-*.liquid` file
- [ ] No hard-coded font-size values remain — all use variables
- [ ] Navbar matches Webflow styling (DM Sans, #f6f6f6 bg, black border)
- [ ] Mobile breakpoints trigger at 991px, 767px, 479px

---

## Reference

- Webflow CSS source: `recarpet-d673fe83bfacb.webflow/css/recarpet-d673fe83bfacb.webflow.css`
- Webflow HTML pages: `recarpet-d673fe83bfacb.webflow/*.html`
- Current Shopify tokens: `snippets/rc-global-styles.liquid`
- Shopify base CSS: `assets/base.css`
