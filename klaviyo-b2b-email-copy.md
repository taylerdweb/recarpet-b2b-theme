# ReCarpet — B2B Konto Godkänt: Email-copy per kundgrupp & språk

Alla mail använder samma Klaviyo-template (logga + mörkgrön footer med kontaktinfo).
Subject lines och preview text anges per mail. HTML-body klistras in i textblocket.

---

## MEMBER

### Member SEK (Svenska)

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

### Member NOK (Norsk)

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

### Member DKK (Dansk)

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

### Member EUR (English)

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

## PLUS

### Plus SEK (Svenska)

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

### Plus NOK (Norsk)

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

### Plus DKK (Dansk)

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

### Plus EUR (English)

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

## PREMIUM

### Premium SEK (Svenska)

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

### Premium NOK (Norsk)

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

### Premium DKK (Dansk)

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

### Premium EUR (English)

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
