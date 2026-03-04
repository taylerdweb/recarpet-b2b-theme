# reCarpet — Produktdata översikt

## 🏷️ Produktidentitet
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Varumärke | Interface | Orak Excel (MARQUE) | Vendor |
| Modell | Composure | Orak Excel (MODELE) | Title (del av) |
| Färg / Colorway | 4169020 Secure | Orak Excel (COLORIS) | Metafält: recarpet.colorway |
| Format | 50×50 cm | Orak Excel (DESCRIPTION) | Metafält: recarpet.format |
| GIZ-nummer | GIZ2202010 | Orak Excel (N° DE GIZ) | SKU + Metafält: recarpet.giz_id |
| Produkttyp | Moquette de réemploi | Manuellt | Product Type |

---

## 💰 Pris
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Pris per m² | 299 kr/m² | Oraks prislista | Price (native) |

---

## 📦 Lager & beställning
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Lager (m²) | 125 m² | Orak Excel (STOCK M² EBS) | Metafält: recarpet.stock_sqm |
| Minimibeställning | 5 m² | Orak specfil | Metafält: recarpet.min_order_sqm |
| Leveranstid | 15 dagar | Orak specfil | Metafält: recarpet.delivery_days |

---

## 🔧 Tekniska specifikationer
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Tjocklek | 6 mm | Orak specfil | Metafält: recarpet.thickness |
| Brandklass | Bfl S1 | Orak specfil | Metafält: recarpet.fire_rating |
| Ljudisolering | ΔLw: 23 dB | Orak specfil | Metafält: recarpet.acoustic_rating |
| Stötdämpning | α: 0.2 | Orak specfil | Metafält: recarpet.impact_absorption |
| LRV | L: 37.3 – Y: 9.7 | Orak specfil | Metafält: recarpet.lrv |
| Underlag (sous-couche) | Ja / Nej / Typ | Orak specfil | Metafält: recarpet.backing |
| Ecodesigned | Ja | Orak specfil | Metafält: recarpet.ecodesigned |

---

## 🌱 Hållbarhet & ursprung
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Ursprung / Byggnad | Village Olympique Saint Denis | Orak Excel (ORIGINE) | Metafält: recarpet.origin |

---

## 📄 Dokument
| Fält | Exempel | Källa | Shopify-fält |
|---|---|---|---|
| Tekniskt datablad | länk till PDF | Orak specfil | Metafält: recarpet.technical_sheet |

---

## ❓ Öppna frågor att bestämma

- **Visa GIZ-nummer för kunden?** Det är Oraks interna lager-ID — kan vara relevant för B2B-kunder som beställer och behöver referera till en specifik lot.
- **Produktbeskrivning (brödtext)?** Ska det vara en fri text per produkt, autogenererad från data, eller ingen brödtext alls?
- **Bilder** — hur namnges de i Oraks delade mapp? Behöver matcha mot GIZ-nummer eller modellnamn för att importskriptet ska kunna länka rätt bild automatiskt.
- **Minimibeställning och leveranstid** — är dessa alltid fasta (5 m², 15 dagar) eller varierar de per produkt?
