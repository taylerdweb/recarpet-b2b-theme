# Montering-tillval — Fullständig spec för ombyggnad

## Översikt

reCarpet säljer mattor (carpet tiles) via en Shopify-butik med SparkLayer B2B. Kunder ska kunna lägga till "montering" (installation service) som tillval vid köp. Monteringen hanteras som en separat produkt i SparkLayer-korgen (SKU: `RC-SERVICE-MONTERING`) men ska vara helt styrd av systemet — kunden ska aldrig kunna ändra kvantitet, radera, eller manipulera monteringsraden i kundkorgen.

---

## Teknisk miljö

### SparkLayer

- B2B-plattform ovanpå Shopify
- Alla cart-relaterade UI-element renderas i **shadow DOM** (closed mode, men vi forcerar open via `Element.prototype.attachShadow` override)
- SolidJS-baserat internt: reactiv rendering som kan **byta ut hela DOM-träd** vid state-ändringar
- Viktiga custom elements: `spark-pdp`, `spark-drawer` (cart drawer), `spark-cart` (cart page), `spark-product-card`

### SparkLayer JS API (`window.spark`)

```js
// Hämta kundkorgen
window.spark.getCart() → Promise<{ items: CartItem[] }>

// CartItem-struktur
{
  sku: string,
  quantity: number,
  customAttributes: [{ key: string, value: string }] | null
}

// Uppdatera kundkorgen (intern metod som vi wrapper)
window.spark._updateCart(payload, t, n) → Promise

// Payload-format för _updateCart
{
  products: [{
    sku: string,
    quantity?: number,        // sätt absolut antal (0 = ta bort)
    adjustQuantity?: number,  // relativ ändring (+5, -3)
    customAttributes?: [{ key: string, value: string }]
  }]
}

// Öppna cart drawer
window.spark.openDrawer()
```

### Shadow DOM-struktur (spark-drawer / spark-cart)

```
spark-drawer (host element)
  └── #shadow-root (open, tack vare vår override)
      ├── <style data-rc-pre="1">  ← vår pre-injicerade CSS
      ├── ... SparkLayer interna styles ...
      └── <div> wrapper
          └── <ul class="divide-y">
              ├── <li class="py-4">  ← cart item row
              │   ├── <a style="background-image: url(...)">  ← produktbild
              │   ├── <div>
              │   │   ├── <p>Produktnamn</p>
              │   │   └── <p class="hidden text-default-body sm:block">SKU-NUMMER</p>
              │   └── <div class="mt-2">  ← qty controls wrapper
              │       ├── <button> - </button>
              │       ├── <input type="number" value="5">
              │       ├── <button> + </button>
              │       └── <button> 🗑 (delete) </button>
              ├── <li class="py-4"> ... nästa produkt ...
              └── ...
```

### Pre-injicerad CSS i shadow roots

Vi har ett `attachShadow`-override som injicerar en `<style>`-tagg i varje `spark-*` shadow root vid skapande-tillfället (innan content renderas). CSS som läggs in här körs **innan första rendering** och kan inte tas bort av SolidJS.

```js
var PRE_INJECT_CSS = '...existing rules...'
  + '/* MONTERING LOCK RULES HÄR */';
```

### Befintlig HTML (main-product.liquid)

Checkboxen finns redan i `sections/main-product.liquid` (rad ~187):

```html
<div class="montering-addon" id="montering-addon" style="display:none;">
  <label class="montering-addon__label">
    <input type="checkbox" id="montering-checkbox" class="montering-addon__checkbox">
    <span class="montering-addon__text">
      Lägg till montering
      <span class="montering-addon__price">+45 kr/m²</span>
    </span>
  </label>
  <p class="montering-addon__note" id="montering-subtotal" style="display:none;"></p>
</div>
```

Visas bara för Premium/Krets-kunder, ej på tjänsteprodukter.

---

## Funktionskrav

### F1: PDP Montering-checkbox

1. Vid sidladdning: visa `#montering-addon` (sätts till `display: none` i HTML, JS togglar synlighet)
2. När checkbox är ikryssad, visa beräknad delsumma: `Montering: X m² × 45 kr = Y kr`
3. Kvantiteten hämtas från `spark-pdp`'s shadow DOM (`input[type="number"]`)
4. Delsumman uppdateras löpande (poll eller observer)

### F2: Lägg till produkt med montering

**Flöde:**
1. Kund klickar "Köp" med montering-checkboxen ikryssad
2. Vi interceptar `spark._updateCart`
3. Vi injicerar `customAttributes: [{ key: "montering", value: "true" }]` på produkten i payload
4. SparkLayer lägger till produkten (med attribut) → skapar en **separat rad** från samma SKU utan attribut
5. **Efter** att SparkLayer bekräftat tillägg → vi anropar `_updateCart` igen för att lägga till `RC-SERVICE-MONTERING` med `adjustQuantity: X`
6. Kundkorgen öppnas

**Viktigt:** Steg 5 MÅSTE vänta på att steg 4 resolvar innan det körs. Annars finns monteringsprodukten inte i korgen när drawern öppnas.

### F3: Kvantitetssynkning

Monteringsprodukten (`RC-SERVICE-MONTERING`) ska alltid ha `quantity` = summan av alla produkters quantity som har `customAttributes` med `montering=true`.

**Trigger:** Efter varje cart-ändring (utom våra egna interna anrop):
1. Hämta cart via `spark.getCart()`
2. Summera `quantity` för alla items som har `montering=true` attribut → `attrQty`
3. Hitta montering-radens `quantity` → `monteringQty`
4. Om `monteringQty !== attrQty` → uppdatera montering till `attrQty`
5. Om `attrQty === 0` och montering finns i korgen → ta bort montering (sätt quantity: 0)

### F4: Cart row lock (VIKTIGASTE KRAVET)

Monteringsraden (`RC-SERVICE-MONTERING`) i kundkorgen ska vara **helt låst**:
- ❌ Ingen +/- knapp
- ❌ Ingen delete-knapp
- ❌ Inget quantity-input
- ✅ Produktnamn och SKU ska synas
- ✅ Kvantitet ska visas (som text, inte input)

**Krav:**
- Låsningen måste fungera **omedelbart** när korgen öppnas efter att man lagt till produkt
- Låsningen måste **överleva SolidJS re-renders** (som byter ut DOM-element)
- Inga synliga "flicker" — kontroller ska aldrig vara synliga ens för en frame

---

## Edge cases

### E1: Lägg till produkt A med montering → OK
Förväntat: Korg visar produkt A + RC-SERVICE-MONTERING (låst)

### E2: Lägg till produkt B med montering (korg har redan A + montering)
Förväntat: Korg visar A + B + RC-SERVICE-MONTERING (qty = A.qty + B.qty). Produkt A ska INTE försvinna.

### E3: Lägg till samma produkt A utan montering (korg har redan A med montering)
Förväntat: Korg visar:
- Product A (utan montering attr, ny rad eller uppdaterad qty)
- Product A (med montering attr, separat rad om SparkLayer separerar)
- RC-SERVICE-MONTERING (qty = bara den A-raden som har montering attr)

Om SparkLayer SLÅR IHOP samma SKU (strippas customAttributes): monteringssynken kommer se `attrQty=0` och ta bort montering. **Detta måste hanteras** — antingen:
a) Förhindra merge genom att alltid ha unik customAttribute
b) Eller acceptera att montering försvinner om SparkLayer mergar (men logga tydligt)

### E4: Kund ökar qty på en produkt med montering i korgen
Förväntat: syncMontering uppdaterar montering-qty att matcha

### E5: Kund tar bort en produkt med montering i korgen
Förväntat: syncMontering minskar montering-qty. Om inga montering-produkter kvar → montering tas bort.

### E6: Kund försöker ta bort monteringsraden direkt
Förväntat: **Ska inte vara möjligt** — delete-knappen är gömd av CSS/JS lock.

### E7: Siduppdatering → öppna korg
Förväntat: Montering-raden ska vara låst direkt (fungerar redan efter refresh, var problemet)

### E8: Första cart-öppning (aldrig öppnad denna session)
Förväntat: `spark-drawer` element skapas av SparkLayer vid behov. Vår kod måste hantera att elementet inte existerar förrän korgen öppnas.

---

## Tekniska begränsningar och lärdomar

### SolidJS re-render beteende
- SolidJS **byter ut hela DOM-element** vid state-ändringar (t.ex. ny produkt tillagd)
- Alla custom attributes (`data-rc-locked`) som vi satt på gamla element **försvinner**
- MutationObserver triggar för dessa ersättningar (childList mutations)

### Att undvika
1. **requestAnimationFrame för lock** — ger synlig flicker (en frame utan lock)
2. **Text-ändringar / element-insertions i shadow DOM** — triggar SolidJS feedback loops
3. **Debounce/timeout utan promise-kedja** — missar timing om API-svar tar olika lång tid
4. **Bred CSS i shadow DOM** (t.ex. `[attr] [class*="mt-"]`) — matchar för mycket
5. **dataset på ShadowRoot** — ShadowRoot har inte `dataset` property (använd WeakSet istället)
6. **JSON.parse(JSON.stringify(payload))** — kan stripa non-serializable properties SparkLayer behöver

### Rekommenderad approach för row lock

**Strategi: PRE_INJECT_CSS + synkron MutationObserver**

1. **CSS-first:** Injicera lock-CSS i `PRE_INJECT_CSS` (körs innan rendering). CSS-reglerna ska gömma kontroller på rader med `[data-rc-locked]` attribut.

2. **Synkron MutationObserver:** Observera shadow root med `{ childList: true, subtree: true }`. Vid mutation → kör lock *synkront* (INTE rAF eller setTimeout). Använd `_isLocking` guard mot rekursion.

3. **Promise-kedjad timing:** Kör lock efter varje `silentUpdateCart().then()` — inte efter den yttre `_updateCart`. Montering-produkten existerar inte i DOM:en förrän silentUpdateCart resolvar.

4. **Fallback poll:** 500ms interval som backup, rensas efter 2 min.

---

## Kodens placering

All monteringskod ska ligga i `layout/theme.liquid` inuti den befintliga `spark.onReady(function() { ... })` blocket, efter den nuvarande kommentaren:
```
// MONTERING CODE REMOVED — will be rebuilt from spec
```

CSS ska ligga:
- Lock-regler i `PRE_INJECT_CSS` (shadow DOM)
- Checkbox-styling i `<style>`-blocket för SparkLayer (vanliga DOM)

HTML finns redan i `sections/main-product.liquid` (behöver ej ändras).

---

## Sammanfattning av komponenter att bygga

| # | Komponent | Beskrivning |
|---|-----------|-------------|
| 1 | Checkbox UI | Visa checkbox, beräkna delsumma, poll qty |
| 2 | updateCart wrapper | Intercepta `spark._updateCart`, injicera customAttributes |
| 3 | silentUpdateCart | Intern helper för att anropa `_origSparkUpdateCart` utan att trigga wrapper |
| 4 | syncMonteringWithCart | Läs cart, synka montering-qty med attrQty |
| 5 | Row lock CSS | PRE_INJECT_CSS regler för `[data-rc-locked]` |
| 6 | Row lock JS | Hitta montering-rad i shadow DOM, sätt `data-rc-locked` |
| 7 | MutationObserver setup | Watcha spark-drawer/spark-cart shadow roots |
| 8 | Promise-kedjning | Säkerställ att lock körs EFTER montering finns i korgen |
