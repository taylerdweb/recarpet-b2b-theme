# ReCarpet B2B — Komplett mejlcopy för alla automatiserade flöden

Alla mail använder samma Klaviyo-template (logga + mörkgrön footer med kontaktinfo).
Subject lines och preview text anges per mail. HTML-body klistras in i textblocket.
Alla knappar länkar till: https://recarpet-b2b.myshopify.com/

---

## 1. ANSÖKAN MOTTAGEN

Skickas automatiskt när en ny kund registrerar sig och får taggen "pending". Samma mejl för alla kunder (svenska).

**Subject:** Vi har mottagit din ansökan — ReCarpet
**Preview:** Vi granskar din ansökan och återkommer inom 1–2 arbetsdagar

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Tack för att du registrerat dig hos ReCarpet! Vi har mottagit din ansökan om ett B2B-konto.</p>
  <p>Vi granskar din ansökan och återkommer inom 1–2 arbetsdagar med besked. När ditt konto är godkänt får du tillgång till våra B2B-priser exklusive moms och kan börja beställa direkt på recarpet.se.</p>
  <p>Har du frågor under tiden? Kontakta oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">070-073 36 82</a>.</p>
  <p>Vänliga hälsningar,<br>ReCarpet-teamet</p>
</div>
```

---

## 2. KONTO GODKÄNT

Skickas automatiskt när en kund tilldelas en B2B-tagg (t.ex. b2b-member-sek, b2b-plus-nok). Anpassas per kundgrupp (Member/Plus/Premium) och språk (SEK=svenska, NOK=norska, DKK=danska, EUR=engelska).

### 2.1 MEMBER

#### Member SEK (Svenska)

**Subject:** Välkommen som B2B Member hos ReCarpet!
**Preview:** Du har nu tillgång till Member-priser exkl. moms

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har granskat din ansökan och är glada att välkomna dig som <strong>B2B Member</strong> hos ReCarpet!</p>
  <p>Som Member får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Tillgång till Member-priser exklusive moms</li>
    <li>Beställning direkt via recarpet.se</li>
    <li>Support via e-post och telefon</li>
  </ul>
  <p>Logga in på ditt konto för att börja handla:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logga in och handla →</a>
  </p>
  <p>Har du frågor? Kontakta oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">070-073 36 82</a>.</p>
  <p>Med vänliga hälsningar,<br>ReCarpet-teamet</p>
</div>
```

---

#### Member NOK (Norsk)

**Subject:** Velkommen som B2B Member hos ReCarpet!
**Preview:** Du har nå tilgang til Member-priser ekskl. mva

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hei {{ first_name|default:"" }},</p>
  <p>Vi har gjennomgått søknaden din og er glade for å ønske deg velkommen som <strong>B2B Member</strong> hos ReCarpet!</p>
  <p>Som Member får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Tilgang til Member-priser eksklusive mva</li>
    <li>Bestilling direkte via recarpet.se</li>
    <li>Support via e-post og telefon</li>
  </ul>
  <p>Logg inn på kontoen din for å begynne å handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logg inn og handle →</a>
  </p>
  <p>Har du spørsmål? Kontakt oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med vennlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Member DKK (Dansk)

**Subject:** Velkommen som B2B Member hos ReCarpet!
**Preview:** Du har nu adgang til Member-priser ekskl. moms

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har gennemgået din ansøgning og er glade for at byde dig velkommen som <strong>B2B Member</strong> hos ReCarpet!</p>
  <p>Som Member får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Adgang til Member-priser eksklusive moms</li>
    <li>Bestilling direkte via recarpet.se</li>
    <li>Support via e-mail og telefon</li>
  </ul>
  <p>Log ind på din konto for at begynde at handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log ind og handle →</a>
  </p>
  <p>Har du spørgsmål? Kontakt os på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med venlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Member EUR (English)

**Subject:** Welcome as a B2B Member at ReCarpet!
**Preview:** You now have access to Member pricing excl. VAT

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hi {{ first_name|default:"" }},</p>
  <p>We've reviewed your application and are happy to welcome you as a <strong>B2B Member</strong> at ReCarpet!</p>
  <p>As a Member, you get:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Access to Member pricing excluding VAT</li>
    <li>Order directly via recarpet.se</li>
    <li>Support via email and phone</li>
  </ul>
  <p>Log in to your account to start shopping:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log in and shop →</a>
  </p>
  <p>Have questions? Contact us at <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> or <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Best regards,<br>The ReCarpet Team</p>
</div>
```

---

### 2.2 PLUS

#### Plus SEK (Svenska)

**Subject:** Välkommen som B2B Plus-kund hos ReCarpet!
**Preview:** Du har nu tillgång till Plus-priser exkl. moms

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har granskat din ansökan och är glada att välkomna dig som <strong>B2B Plus</strong>-kund hos ReCarpet!</p>
  <p>Som Plus-kund får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Tillgång till förmånliga Plus-priser exklusive moms</li>
    <li>Prioriterad orderhantering</li>
    <li>Beställning direkt via recarpet.se</li>
    <li>Dedikerad support via e-post och telefon</li>
  </ul>
  <p>Logga in på ditt konto för att börja handla:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logga in och handla →</a>
  </p>
  <p>Har du frågor? Kontakta oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">070-073 36 82</a>.</p>
  <p>Med vänliga hälsningar,<br>ReCarpet-teamet</p>
</div>
```

---

#### Plus NOK (Norsk)

**Subject:** Velkommen som B2B Plus-kunde hos ReCarpet!
**Preview:** Du har nå tilgang til Plus-priser ekskl. mva

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hei {{ first_name|default:"" }},</p>
  <p>Vi har gjennomgått søknaden din og er glade for å ønske deg velkommen som <strong>B2B Plus</strong>-kunde hos ReCarpet!</p>
  <p>Som Plus-kunde får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Tilgang til gunstige Plus-priser eksklusive mva</li>
    <li>Prioritert ordrehåndtering</li>
    <li>Bestilling direkte via recarpet.se</li>
    <li>Dedikert support via e-post og telefon</li>
  </ul>
  <p>Logg inn på kontoen din for å begynne å handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logg inn og handle →</a>
  </p>
  <p>Har du spørsmål? Kontakt oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med vennlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Plus DKK (Dansk)

**Subject:** Velkommen som B2B Plus-kunde hos ReCarpet!
**Preview:** Du har nu adgang til Plus-priser ekskl. moms

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har gennemgået din ansøgning og er glade for at byde dig velkommen som <strong>B2B Plus</strong>-kunde hos ReCarpet!</p>
  <p>Som Plus-kunde får du:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Adgang til fordelagtige Plus-priser eksklusive moms</li>
    <li>Prioriteret ordrehåndtering</li>
    <li>Bestilling direkte via recarpet.se</li>
    <li>Dedikeret support via e-mail og telefon</li>
  </ul>
  <p>Log ind på din konto for at begynde at handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log ind og handle →</a>
  </p>
  <p>Har du spørgsmål? Kontakt os på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med venlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Plus EUR (English)

**Subject:** Welcome as a B2B Plus customer at ReCarpet!
**Preview:** You now have access to Plus pricing excl. VAT

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hi {{ first_name|default:"" }},</p>
  <p>We've reviewed your application and are happy to welcome you as a <strong>B2B Plus</strong> customer at ReCarpet!</p>
  <p>As a Plus customer, you get:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Access to discounted Plus pricing excluding VAT</li>
    <li>Priority order handling</li>
    <li>Order directly via recarpet.se</li>
    <li>Dedicated support via email and phone</li>
  </ul>
  <p>Log in to your account to start shopping:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log in and shop →</a>
  </p>
  <p>Have questions? Contact us at <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> or <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Best regards,<br>The ReCarpet Team</p>
</div>
```

---

### 2.3 PREMIUM

#### Premium SEK (Svenska)

**Subject:** Välkommen som B2B Premium-kund hos ReCarpet!
**Preview:** Du har nu tillgång till våra bästa priser och premiumtjänster

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har granskat din ansökan och är glada att välkomna dig som <strong>B2B Premium</strong>-kund hos ReCarpet!</p>
  <p>Som Premium-kund får du tillgång till vårt mest omfattande erbjudande:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Våra bästa Premium-priser exklusive moms</li>
    <li>Prioriterad orderhantering och leverans</li>
    <li>Tillgång till premiumtjänster och exklusivt sortiment</li>
    <li>Personlig kontaktperson hos ReCarpet</li>
    <li>Beställning direkt via recarpet.se</li>
  </ul>
  <p>Logga in på ditt konto för att börja handla:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logga in och handla →</a>
  </p>
  <p>Har du frågor? Kontakta oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">070-073 36 82</a>.</p>
  <p>Med vänliga hälsningar,<br>ReCarpet-teamet</p>
</div>
```

---

#### Premium NOK (Norsk)

**Subject:** Velkommen som B2B Premium-kunde hos ReCarpet!
**Preview:** Du har nå tilgang til våre beste priser og premiumtjenester

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hei {{ first_name|default:"" }},</p>
  <p>Vi har gjennomgått søknaden din og er glade for å ønske deg velkommen som <strong>B2B Premium</strong>-kunde hos ReCarpet!</p>
  <p>Som Premium-kunde får du tilgang til vårt mest omfattende tilbud:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Våre beste Premium-priser eksklusive mva</li>
    <li>Prioritert ordrehåndtering og levering</li>
    <li>Tilgang til premiumtjenester og eksklusivt sortiment</li>
    <li>Personlig kontaktperson hos ReCarpet</li>
    <li>Bestilling direkte via recarpet.se</li>
  </ul>
  <p>Logg inn på kontoen din for å begynne å handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Logg inn og handle →</a>
  </p>
  <p>Har du spørsmål? Kontakt oss på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med vennlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Premium DKK (Dansk)

**Subject:** Velkommen som B2B Premium-kunde hos ReCarpet!
**Preview:** Du har nu adgang til vores bedste priser og premiumtjenester

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Vi har gennemgået din ansøgning og er glade for at byde dig velkommen som <strong>B2B Premium</strong>-kunde hos ReCarpet!</p>
  <p>Som Premium-kunde får du adgang til vores mest omfattende tilbud:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Vores bedste Premium-priser eksklusive moms</li>
    <li>Prioriteret ordrehåndtering og levering</li>
    <li>Adgang til premiumtjenester og eksklusivt sortiment</li>
    <li>Personlig kontaktperson hos ReCarpet</li>
    <li>Bestilling direkte via recarpet.se</li>
  </ul>
  <p>Log ind på din konto for at begynde at handle:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log ind og handle →</a>
  </p>
  <p>Har du spørgsmål? Kontakt os på <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med venlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

#### Premium EUR (English)

**Subject:** Welcome as a B2B Premium customer at ReCarpet!
**Preview:** You now have access to our best pricing and premium services

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hi {{ first_name|default:"" }},</p>
  <p>We've reviewed your application and are happy to welcome you as a <strong>B2B Premium</strong> customer at ReCarpet!</p>
  <p>As a Premium customer, you get access to our most comprehensive offering:</p>
  <ul style="padding-left: 20px; margin: 8px 0 16px;">
    <li>Our best Premium pricing excluding VAT</li>
    <li>Priority order handling and delivery</li>
    <li>Access to premium services and exclusive product range</li>
    <li>Personal account manager at ReCarpet</li>
    <li>Order directly via recarpet.se</li>
  </ul>
  <p>Log in to your account to start shopping:</p>
  <p style="text-align: center; margin: 24px 0;">
    <a href="https://recarpet-b2b.myshopify.com/" style="background-color: #edb81e; color: #121212; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Log in and shop →</a>
  </p>
  <p>Have questions? Contact us at <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> or <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Best regards,<br>The ReCarpet Team</p>
</div>
```

---

## 3. ORDERBEKRAFTELSE

Skickas automatiskt via Shopify Flow → Klaviyo (b2b_order_confirmation) när en draft order skapas. Anpassas per sprak baserat på kundens valutatagg (SEK/NOK/DKK/EUR). Ordernummer och belopp fylls i dynamiskt via event properties.

### Svenska (SEK)

**Subject:** Orderbekraftelse — {{ event.order_name }}
**Preview:** Tack for din bestallning hos ReCarpet

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Tack for din bestallning! Vi har mottagit din order och den bearbetas nu.</p>
  <p><strong>Ordernummer:</strong> {{ event.order_name }}<br>
  <strong>Totalt belopp:</strong> {{ event.total_amount }} SEK (exkl. moms)</p>
  <p>Vi aterkommer med leveransinformation inom kort.</p>
  <p>Har du fragor? Kontakta oss pa <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">070-073 36 82</a>.</p>
  <p>Med vanliga halsningar,<br>ReCarpet-teamet</p>
</div>
```

---

### Norsk (NOK)

**Subject:** Ordrebekreftelse — {{ event.order_name }}
**Preview:** Takk for din bestilling hos ReCarpet

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hei {{ first_name|default:"" }},</p>
  <p>Takk for din bestilling! Vi har mottatt ordren din og den behandles na.</p>
  <p><strong>Ordrenummer:</strong> {{ event.order_name }}<br>
  <strong>Totalt belop:</strong> {{ event.total_amount }} NOK (ekskl. mva)</p>
  <p>Vi kommer tilbake med leveringsinformasjon snart.</p>
  <p>Har du sporsmal? Kontakt oss pa <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med vennlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

### Dansk (DKK)

**Subject:** Ordrebekraeftelse — {{ event.order_name }}
**Preview:** Tak for din bestilling hos ReCarpet

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hej {{ first_name|default:"" }},</p>
  <p>Tak for din bestilling! Vi har modtaget din ordre, og den behandles nu.</p>
  <p><strong>Ordrenummer:</strong> {{ event.order_name }}<br>
  <strong>Samlet belob:</strong> {{ event.total_amount }} DKK (ekskl. moms)</p>
  <p>Vi vender tilbage med leveringsinformation snart.</p>
  <p>Har du sporgsmaal? Kontakt os pa <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> eller <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Med venlig hilsen,<br>ReCarpet-teamet</p>
</div>
```

---

### English (EUR)

**Subject:** Order confirmation — {{ event.order_name }}
**Preview:** Thank you for your order at ReCarpet

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hi {{ first_name|default:"" }},</p>
  <p>Thank you for your order! We have received it and it is now being processed.</p>
  <p><strong>Order number:</strong> {{ event.order_name }}<br>
  <strong>Total amount:</strong> {{ event.total_amount }} EUR (excl. VAT)</p>
  <p>We will get back to you with shipping information shortly.</p>
  <p>Have questions? Contact us at <a href="mailto:info@recarpet.se" style="color:#1e4433;">info@recarpet.se</a> or <a href="tel:+46700733682" style="color:#1e4433;">+46 700 73 36 82</a>.</p>
  <p>Best regards,<br>The ReCarpet Team</p>
</div>
```

---

## 4. INTERN ORDERNOTIFIERING

Skickas internt till ReCarpet (info@recarpet.se) vid varje ny B2B-order via Shopify Flow → Klaviyo (b2b_internal_order_notification). Innehaller orderdetaljer och kundinfo for intern hantering.

**Subject:** Ny B2B-order: {{ event.order_name }} — {{ event.customer_name }}
**Preview:** Order pa {{ event.total_amount }} {{ event.currency }} fran {{ event.customer_name }}

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p><strong>Ny B2B-order inkommen</strong></p>
  <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
    <tr>
      <td style="padding: 8px 12px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600; width: 160px;">Ordernummer</td>
      <td style="padding: 8px 12px; border: 1px solid #ddd;">{{ event.order_name }}</td>
    </tr>
    <tr>
      <td style="padding: 8px 12px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Kund</td>
      <td style="padding: 8px 12px; border: 1px solid #ddd;">{{ event.customer_name }} ({{ event.customer_email }})</td>
    </tr>
    <tr>
      <td style="padding: 8px 12px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Kundgrupp</td>
      <td style="padding: 8px 12px; border: 1px solid #ddd;">{{ event.customer_tags }}</td>
    </tr>
    <tr>
      <td style="padding: 8px 12px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Totalt belopp</td>
      <td style="padding: 8px 12px; border: 1px solid #ddd;">{{ event.total_amount }} {{ event.currency }} (exkl. moms)</td>
    </tr>
  </table>
  <p>Hantera ordern i <a href="https://recarpet-b2b.myshopify.com/admin/draft_orders" style="color:#1e4433;">Shopify Admin</a>.</p>
</div>
```

---

## 5. LEVERANTORSNOTIFIERING (Orak / Composil)

Skickas automatiskt till leverantoren (Orak eller Composil) nar en B2B-kund bestaller deras produkter. Triggas via Shopify Flow baserat pa SKU-prefix: RCT-O- (Orak) eller RCT-C- (Composil). Klaviyo-events: b2b_supplier_order_orak / b2b_supplier_order_composil.

### Orak

**Subject:** New order from ReCarpet — {{ event.order_name }}
**Preview:** Order for {{ event.line_item_sku }} to {{ event.customer_name }}

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hello,</p>
  <p>We would like to confirm a new order placed via ReCarpet.</p>

  <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600; width: 180px;">Article number</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.line_item_sku }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Quantity</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.line_item_quantity }} pcs</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Delivery address</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.shipping_address }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Delivery date</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.delivery_date|default:"To be confirmed" }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Consignee name</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.customer_name }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Consignee phone</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.customer_phone|default:"Not provided" }}</td>
    </tr>
  </table>

  <p>Please confirm receipt of this order.</p>
  <p>Kind regards,<br>ReCarpet</p>
</div>
```

### Composil

**Subject:** New order from ReCarpet — {{ event.order_name }}
**Preview:** Order for {{ event.line_item_sku }} to {{ event.customer_name }}

```html
<div style="font-family: Arial, Helvetica, sans-serif; color: #121212; font-size: 16px; line-height: 1.6;">
  <p>Hello,</p>
  <p>We would like to confirm a new order placed via ReCarpet.</p>

  <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600; width: 180px;">Article number</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.line_item_sku }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Quantity</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.line_item_quantity }} pcs</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Delivery address</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.shipping_address }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Delivery date</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.delivery_date|default:"To be confirmed" }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Consignee name</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.customer_name }}</td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #ddd; background: #f5f5f5; font-weight: 600;">Consignee phone</td>
      <td style="padding: 10px 14px; border: 1px solid #ddd;">{{ event.customer_phone|default:"Not provided" }}</td>
    </tr>
  </table>

  <p>Please confirm receipt of this order.</p>
  <p>Kind regards,<br>ReCarpet</p>
</div>
```
