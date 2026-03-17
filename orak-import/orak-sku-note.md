# Notering till ORAK — produktidentifierare i CSV-exporten

Vi har börjat automatisera uppladdningen av ORAKs produktkatalog till vår B2B-webshop och har noterat några inkonsekvenser i fältet `identificationID` som vi vill lyfta.

---

## 1. Interna anteckningar inbakade i produkt-ID:t

Ett antal rader har text som verkar vara interna ORAK-arbetsnoteringar inbakad direkt i ID-fältet, snarare än ett rent produktidentifierare:

**Exempel:**
```
2312005-01_attente nettoyage
250501-01_attente nettoyage-+ -198 11/09-composil+ 900 jonas
240207-01-bloqué Nicolas 03/12
250110-01-bloqué 09/09 welltek+re-you
241001-02-DV1794
```

Vi hanterar detta i vår import idag, men det vore bättre om `identificationID` alltid innehåller enbart det rena lot-numret (t.ex. `2312005-01`) och att eventuella anteckningar ligger i ett separat fält.

---

## 2. Rader som inte är produkter

Följande rader i CSV:n verkar vara interna poster som av misstag tagits med i exporten:

```
Mr_Rouni
LAB SERVICES
Yannick_16/12_sur chantier
```

Dessa saknar meningsfulla produktdata och orsakar fel i vår import. Kan ni säkerställa att enbart faktiska produkter ingår i exporten?

---

## 3. Blandade ID-format

En del produkter har GIZ-nummer (`GIZ2202010`) och andra har datum-baserade lot-nummer (`240604-01`). Det är inget problem i sig — vi förstår att de representerar olika stadier i er process — men det vore bra att bekräfta:

- **GIZ-nummer** = fullt katalogiserade produkter
- **Datum-format (YYMMDD-NN)** = lot-nummer för produkter under bearbetning

Stämmer detta? Och kan vi räkna med att ett GIZ-nummer aldrig ändras efter tilldelning?

---

Tack för att ni tittar på detta. Det underlättar vår automatisering avsevärt om exporten är konsekvent formaterad.
