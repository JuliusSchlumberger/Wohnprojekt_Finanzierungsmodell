# Review: Wohnprojekt_Finanzierungsmodell (Stand c9abfd8, 2026-10-26)

Geprüft: `model/` vollständig, `app/main.py`, `app/widgets.py` (Eingabe-Umrechnung), Methodikseite, Tests (83 bestanden), trias-Referenz. Dazu numerische Experimente mit den App-Defaults (`ProjectInputs()`), siehe Abschnitt 6.

## 1. Gesamturteil

Der Rechenkern ist handwerklich sauber: Annuität, Ratentilgung, Zinsbindung mit Anschlusszins, Tilgungszuschuss, Zinsgutschrift, Erbbaurecht, Rückstandslogik und die trias-Referenz stimmen (Jahr-1-Werte per Hand nachgerechnet: Bankannuität 135.897 €, Zins 112.236 €, Tilgung 23.661 €). Die Liquiditätsidentität hält, die Bisektion ist monoton und robust.

Die Probleme liegen nicht in den Formeln, sondern in dem, was die Kennzahl „erforderliche Miete“ misst, und in einigen Modellannahmen, die ökonomisch nicht zusammenpassen. Mit den Defaults ist **Jahr 1 die bindende Nebenbedingung** (`binding_year` = (1, "reserve")). Die ausgewiesenen 903,55 € sind damit die Miete, die nötig ist, um das erste Jahr mit 20 % Leerstand, 6 % Bankzins auf den vollen Kredit und 6 Monaten Reserve zu überstehen – nicht die Miete, die das Projekt dauerhaft kostendeckend macht. Alles, was danach passiert (Mitgliederdarlehen zu 5 %, Direktkredite, Rückstände), beeinflusst die Kennzahl **gar nicht** und wird nur über die späteren Mietrabatte sichtbar. Das ist die wichtigste Erkenntnis dieses Reviews, weil die Nutzer daraus falsche Schlüsse ziehen werden („der Mitgliederdarlehenszins spielt keine Rolle“).

## 2. Befunde nach Gewicht

### Hoch

**H1 – Die Kennzahl „erforderliche Miete“ misst den Engpass, nicht die Kosten.**
Experiment (Defaults): Mitgliederdarlehenszins 5 % → 2 % → 0 %: Startmiete 903,55 / 903,55 / 903,55; mittlere reale Miete über 30 Jahre (nach Rabatten): 781 / 748 / 734 €. Ablösung der Mitgliederdarlehen durch Direktkredite: Startmiete unverändert, Lebenszeitkosten +17 €/Monat. Reserve 6 → 12 Monate: +50 € Startmiete, obwohl das Geld dem Projekt gehört. Empfehlung: zweite Hauptkennzahl „mittlere reale Miete nach Rabatten über 30 Jahre“ (oder Barwert aller Mitgliederzahlungen pro Person) neben der Startmiete; `binding_year` prominent anzeigen („Die Miete wird von Jahr 1 bestimmt: Anfangsleerstand“). Die Unsicherheitsseite sollte dieselbe zweite Kennzahl auswerten.

**H2 – Geld liegt zu 0 % herum, während die Bank 6 % kostet.**
Weil Jahr 1 bindet, sammelt das Projekt bis Jahr 14 rund 497.000 € Liquidität an (Defaults), die erst in Jahr 15 die Mitgliederdarlehen bedienen. Zinsen auf Liquidität und Rücklage gibt es im Modell nicht; eine Sondertilgung der Bank aus Überschüssen ebenfalls nicht. Opportunitätskosten in der Größenordnung von 20–30 T€/Jahr in den Jahren 8–14. Empfehlung: (a) Parameter `cash_interest_rate` (Default z. B. Inflation − 1 pp) auf Liquidität und Instandhaltungsrücklage; (b) Option in `Rules.surplus_use`: `bank_prepayment` – Liquidität oberhalb Reserve + fälliger Nachrangdarlehen tilgt die Bank vorzeitig. Beides ist mit der bestehenden Tranchenlogik umsetzbar (Sondertilgung = zusätzliches `repayment`, Annuität wird ohnehin jährlich neu gerechnet).

**H3 – Direktkredite werden getilgt statt ersetzt.**
`build_scenario` legt Direktkredite als endfällig 5/10 Jahre an und zahlt sie aus der Miete zurück; `churn_rate`/`replacement_rate` existieren in `Tranche`, werden aber nicht genutzt. Das widerspricht der Praxis (Kündigungsquote 5–10 % p. a., Ersatz durch neue Kredite) und macht Direktkredite im Modell zu einem teuren, kurzen Bankersatz. Die Methodikseite erklärt das ehrlich, aber der Default sollte der realistische Fall sein. Empfehlung: Toggle „Direktkredite: ersetzen (Kündigungsquote x %, Ersatzquote y %) / tilgen“, Default ersetzen; Ersatz als `inflow` ist schon implementiert.

**H4 – Jahr-1-Index 1,02: Eingabe und Ausweis passen nicht zusammen.**
`cost_index` mit `indexation_start_year=1` liefert in Jahr 1 bereits (1 + Inflation). Die KPI zeigt 903,55 €, die Tabelle (`rent_per_person`, Jahr 1) 921,62 €. Die Methodik sagt „Miete in Jahr 1“. Gleiches gilt für Marktmiete und Einlage in Modus 2 und für alle „real = Kaufkraft Jahr 1“-Grafiken, die damit 2 % neben den Eingaben liegen. Empfehlung: Index so definieren, dass Jahr `indexation_start_year` den Wert 1 hat (für die trias-Referenz `indexation_start_year=6` → Jahr 5 Basis, Jahr 6 = 1,02 bleibt dann über einen Offset abbildbar), oder die KPI mit dem tatsächlich gezahlten Jahr-1-Betrag ausweisen. Steht bereits in TODO.md – sollte vor Veröffentlichung gelöst sein.

### Mittel

**M1 – Wiederherstellungswert enthält das Grundstück.**
`Property.replacement_value = 0,6 × (purchase_price + renovation_cost)`, `purchase_price` enthält den Bodenwert (Default 540 T€). Boden wird nicht wiederhergestellt. Mit den Defaults 1,332 M€ statt ≈ 1,0 M€ → Instandhaltungszuführung um ein Drittel überhöht (≈ 9 T€/Jahr, ≈ 37 €/Person/Monat). Empfehlung: `replacement_value_ratio × (building_price + renovation_cost)`; unter Erbbaurecht ändert sich dann nichts, was auch richtig ist.

**M2 – Instandhaltungsrücklage wird nie verwendet.**
Zuführung 2 %, Verbrauch 1,5 % des Wiederherstellungswerts → der Topf wächst auf 574 T€ (nominal) in Jahr 50 und ist weder Liquidität noch Verwendung. Effektiv verschwinden 0,5 % × Wiederherstellungswert p. a. (≈ 28 €/Person/Monat) aus dem Modell. Entweder große Sanierungszyklen einbauen (z. B. Entnahme alle 25 Jahre) oder Default `maintenance_reserve_rate = maintenance_rate` und die Differenz als expliziten Sicherheitsaufschlag benennen. Außerdem fehlt eine Prüfung, dass die Rücklage nicht negativ wird (bei `reserve_rate < maintenance_rate`).

**M3 – Einjähriger Ausreißer in der Miete nach Banktilgung.**
Nach `payoff` sinkt `charged_rent` um den Kapitaldienst, damit sinkt `reserve_required` (6 Monate der niedrigeren Miete), und die freigewordene Reserve wird im selben Jahr als `rent_rebate` ausgeschüttet: Jahr 31 zeigt 7 €/Person (Defaults), Jahr 32 dann 321 €. Das ist kein Rechenfehler, aber eine Darstellungsfalle in jeder Mietgrafik. Empfehlung: Reservefreigaben über mehrere Jahre glätten oder die Reserve an die Miete vor Rabatt koppeln.

**M4 – Spec-Toggles A5 und A6 sind nicht verdrahtet.**
`Rules.exit_repayment` wird nirgends gelesen (`member_view` indexiert die Einlage immer real); `Operations.rent_mode` ist nicht in `ProjectInputs`, die App kann „fixed“ nicht einstellen. Entweder verdrahten oder aus Spec/Methodik streichen.

**M5 – Modus 2 ist vom Projekt entkoppelt.**
`member_view` rechnet das Mitgliederdarlehen mit `(1 + r)^(t − entry)` und zahlt es in `loan_due` voll aus – unabhängig davon, ob das Projekt laut `Result` in Rückstand ist (Defaults: 632 T€ von 832 T€ pünktlich, Rest über zwei Jahre mit Verzugszins). Ebenso wird bei Austritt vor Fälligkeit ausgezahlt, ohne Gegenbuchung im Projekt. Für eine Vorsorge-Aussage sollte der Mitgliederpfad aus den Tranchen-Zahlungsströmen (`result.tranches["member_loans"]`, anteilig) abgeleitet werden; `MemberInputs.member_loan` sollte an `ProjectInputs.member_loans / persons` gebunden sein (ist in der App über Widgets gekoppelt, im Modell nicht).

**M6 – Eigenkapitalprüfung zählt befristete Nachrangdarlehen voll.**
`equity_like_share` = Einlagen + Mitglieder- + Direktkredite / Investition (Default 26,7 %). Banken rechnen qualifiziert nachrangige Darlehen an, aber nicht solche, die in 5 Jahren fällig werden und aus dem Cashflow getilgt werden müssen. Mit H3 (Ersatz statt Tilgung) wird die Anrechnung plausibel; bis dahin sollte die Prüfung nur Tranchen mit Laufzeit ≥ Bankzinsbindung zählen oder den Nutzer darauf hinweisen.

### Niedrig

- **N1** `_run`: `kinds` wird nur aus `scenario.tranches` gebildet; Tranchen aus `member_tranches()` (`member_loan_<Typ>`) fallen aus `sub`/`outstanding`/Stundung heraus. Die App nutzt den Pfad nicht, aber `MemberType.member_loan_amount` ist öffentliche API – entweder einbeziehen oder entfernen.
- **N2** `_distribute` bei `payout_15y`: Auszahlungen nur in Jahren 15/30/45; der Rest nach 45 verfällt am Horizont; der Topf liegt zinslos (siehe H2).
- **N3** `uncertainty._rent_near`: `step = 0.08 × guess`; bei `guess = 0` Endlosschleife. Praktisch nicht erreichbar, aber `max(step, 1.0)` kostet nichts.
- **N4** Unsicherheit: der stärkste Treiber der Startmiete (Anfangsleerstand) und der Bankaufschlag selbst sind nicht in `Ranges`; der Bankzins variiert nur über die Inflationsverschiebung und die Anschlussänderung. Mit H1 (zweite Kennzahl) wird die Sensitivitätsanalyse ohnehin aussagekräftiger.
- **N5** Mitgliederdarlehen mit `interest_mode="accrued"`: Zinsgutschriften sind steuerlich im Jahr der Gutschrift zugeflossen (A8 Steuern ausgeklammert, aber auf der Methodikseite erwähnenswert, weil es Mitglieder direkt betrifft).
- **N6** Default-Werte, die das Ergebnis stark prägen und aktuell pessimistisch sind: Bank 6 % nominal (Aufschlag 4 pp; Wohnprojekt-Konditionen 2025/26 eher 3,5–4,5 %), Mitgliederdarlehen 5 % (Praxis 0–2 %), Anfangsleerstand 20 % über drei Jahre (eine Gruppe, die selbst einzieht, hat eher 5–10 % über ein Jahr). Gegenläufig zu niedrig: Verwaltung 4 T€ + Versicherung 2,5 T€ p. a. für ein 2,4-M€-Haus mit 20 Personen (Hausverwaltung/Buchhaltung, Gebäudeversicherung, Grundsteuer, bei eG Prüfungsverband: eher 12–18 T€). Jede dieser Größen verschiebt die Miete um 25–110 €/Person.

## 3. Was richtig ist (geprüft)

- Annuität: jährliche Neuberechnung auf Restschuld und Restlaufzeit reproduziert die konstante Annuität exakt; nach Zinsänderung bleibt der Tilgungstermin, die Rate steigt (konservative, korrekte Lesart).
- `amortization_years` aus Zins + anfänglicher Tilgung: n = −ln(1 − rP/A)/ln(1+r), korrekt.
- Zinsgutschrift + endfällig: 400 T€ × 1,05¹⁵ = 831.571 €, stimmt; Rückzahlung inklusive Zins des letzten Jahres.
- Rückstandslogik: älteste zuerst, Verzugszins mit gewichtetem Satz der fälligen Tranchen, Fristprüfung – nachvollziehbar und konservativ.
- Erbbaurecht: Investition −594 T€ (Boden + Nebenkosten), Erbbauzins 4 % indexiert; Miete 830 statt 904 € – Größenordnung plausibel.
- Startliquidität wird mitfinanziert (nicht aus dem Nichts), Vacancy auf Soll-Miete, Reserve auf Soll-Miete: konsistent.
- trias-Referenz: Übersetzung der Eingaben sauber dokumentiert, inklusive der Eigenheit des Tilgungsbeginns beim Förderdarlehen.
- Zinsen als Aufschlag auf Inflation mit Fisher-Kopplung in der Unsicherheitsanalyse: methodisch sauber.

## 4. Empfohlene Reihenfolge

1. H4 (Index) – klein, aber vor jeder Veröffentlichung.
2. H1 (zweite Kennzahl + bindendes Jahr sichtbar) – ändert keine Rechnung, ändert die Interpretation.
3. M1, M2 (Wiederherstellungswert, Rücklage) – zwei Zeilen, ≈ 60 €/Person/Monat Effekt.
4. H3 (Direktkredite ersetzen) und H2 (Cash-Zins / Sondertilgung) – die beiden Modellerweiterungen mit dem größten ökonomischen Hebel.
5. M4, M5 (Toggles, Modus-2-Kopplung).
6. N6 (Defaults mit Quellen belegen).

## 5. Regressionswerte nach Änderungen

Die Baselines in CLAUDE.md (903,55 / 558,76) werden sich durch H4, M1, M2 ändern. Vorher die Zerlegung aus Abschnitt 6 als Test festhalten (Monotonie je Hebel), nicht nur den Endwert.

## 6. Experimente (Defaults, zur Reproduktion)

```
Startmiete 903,55 €; bindend: Jahr 1 (Reserve); Banktilgung Jahr 30
Jahr-1 rent_per_person in Tabelle: 921,62 € (= 903,55 × 1,02)
Liquidität Jahr 14: 640 T€ (Headroom 497 T€); Jahr 15 Rückstand 249 T€
Reale Miete (Kaufkraft Jahr 1), Jahre 1/6/11/16/21/26/31/36/41/46: 922 922 922 922 599 560 4 174 176 177
Variante                          Start   Ø real 30 J.   Ø real 50 J.
Default                           903,55     781            535
Mitgliederdarlehen 2 %            903,55     748            516
Mitgliederdarlehen 0 %            903,55     734            507
Ablösung durch Direktkredite      903,55     798            546
Bank 4 %                          793,26     681            475
Anfangsleerstand 4 %              878,59     766            526
Rücklage = Instandhaltung 1,5 %   870,45     749            504
Anfangsleerstand × Reserve: 4 %/3 M 859 … 30 %/12 M 1.107
```
