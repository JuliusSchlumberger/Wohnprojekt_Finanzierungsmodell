# Wohnprojekt-Finanzierungsdashboard – Spezifikation

Ziel: Ein statisches, auf GitHub Pages gehostetes Dashboard (Python → WebAssembly), mit dem eine Wohnprojektgruppe Finanzierungsszenarien für ein gemeinsam gekauftes oder im Erbbaurecht genutztes Haus durchspielen kann. Drei Leitfragen, ein gemeinsamer Rechenkern, drei Komplexitätsschichten.

Sprache der Oberfläche: Deutsch. Code, Variablen, Docstrings: Englisch. Dokumentation und Docstrings knapp halten.

---

## 1. Scope und Grundannahmen

Diese Annahmen sind gesetzt und werden auf der Startseite des Dashboards sichtbar aufgeführt.

| Nr. | Annahme | Festlegung |
|---|---|---|
| A1 | Eigentumsmodell | Ein gemeinsamer Rechtsträger (eG, GmbH, GmbH & Co. KG) kauft das Haus oder nutzt es im Erbbaurecht. Mitglieder zahlen ein Nutzungsentgelt („Miete"). Kein Einzeleigentum, kein WEG-Modell. |
| A2 | Mieteinheit | Miete wird pro m² Privatraum berechnet. Standard: alle Mitglieder haben denselben Privatraum (Default 20 m²). Option: Privatraum pro Mitglied einzeln eingeben. Gemeinschaftsflächen werden nicht bepreist, ihre Kosten gehen in die Miete pro m² Privatraum ein. |
| A3 | Kapitalbeiträge | Einzelpersonen (nicht Haushalte) bringen unterschiedlich viel ein. Modelliert über Mitgliedertypen (siehe §4.4). |
| A4 | Verwendung des nach Tilgung frei werdenden Kapitaldienstes | Toggle mit drei Optionen: `rent_reduction` (Mietsenkung), `payout_15y` (Ausschüttung an alle Mitglieder alle 15 Jahre), `next_project` (Solidartransfer, Geld verlässt das Modell). |
| A5 | Rückzahlung der Einlage bei Austritt | Einlage = Genossenschaftsanteil bzw. Einlage in den Rechtsträger. Toggle: `nominal` (Rückzahlung des eingezahlten Betrags) oder `real` (inflationsindexiert). Auszahlung innerhalb eines Jahres nach Austritt. |
| A6 | Zeithorizont | 50 Jahre. Beide Varianten der Mietentwicklung wählbar: `indexed` (Miete folgt Inflation) oder `fixed` (nominal festgeschrieben). |
| A7 | Mindestliquidität | Konto darf nie unter 6 Monatsmieten (Summe aller Mitglieder) fallen. |
| A8 | Steuern | Nicht modelliert in Version 1. Sichtbar deklariert. |
| A9 | Direktkredite | Nachrangig, werden nicht getilgt, sondern bei Kündigung ersetzt (Kündigungsquote p.a. als Parameter) oder aus Rücklage/Bankaufstockung bedient. |

---

## 2. Die drei Leitfragen (Modi)

Alle drei laufen auf demselben Rechenkern (§3). Sie unterscheiden sich nur darin, welche Größe gesucht wird.

### Modus 1 – Erforderliche Miete
Eingabe: Kosten + Kapitalstapel. Gesucht: die niedrigste konstante Miete pro m² Privatraum (im Startjahr, danach je nach A6 indexiert oder fest), bei der die Liquidität in jedem Jahr ≥ Mindestreserve bleibt.
Ausgabe: Miete €/m²/Monat, €/Person/Monat (je Mitgliedertyp), €/Jahr gesamt; Zeitverlauf von Liquidität, Restschuld je Tranche, Kapitaldienst; Jahr der Banktilgung; Entwicklung der Miete nach Tilgung je nach A4.

Lösung: Bisektion über die Miete, Zielfunktion = min über Jahre von (Liquidität − Reserve). Monoton, daher robust.

### Modus 2 – Altersvorsorge-Perspektive
Eingabe: wie Modus 1 plus Mitgliedertyp, Eintrittsjahr, Austrittsjahr (Default: bleibt bis Horizontende), Marktmiete als Vergleich, Alternativrendite für angelegtes Geld.
Gesucht: reale Vermögensentwicklung eines Mitglieds des gewählten Typs im Vergleich zur Alternative „Marktmiete zahlen, Einlage am Kapitalmarkt anlegen".
Ausgabe (alles in Kaufkraft des Startjahrs):
- Nettovermögen im Projekt: Einlage (nominal/real gemäß A5) + Mitgliederdarlehen inkl. gutgeschriebener Zinsen + kumulierte Ausschüttungen (A4).
- Kumulierte Mietersparnis gegenüber Marktmiete (negativ, wenn Projektmiete höher).
- Summe beider = „Vorsorgewert" des Projekts, als Zeitreihe und als Endwert.
- Vergleichspfad: Einlage angelegt zur Alternativrendite, Marktmiete gezahlt.
- Risikohinweis: Nachrangigkeit; optional ein Ausfallszenario (Einlage und Darlehen = 0) als zweite Linie.

Drei Kapitalvarianten je Mitglied als Toggle: `share_only` (nur Genossenschaftsanteil/Einlage, kein Zins), `member_loan` (Einlage plus Mitgliederdarlehen mit Zins, wahlweise Auszahlung oder Gutschrift), `mixed` (beides, Anteile frei einstellbar).

### Modus 3 – Zulässige Investition bei Zielmiete
Eingabe: Zielmiete €/m², Kapitalstapel als Quoten (Eigenkapitalquote, Direktkreditquote, Förderquote, Rest Bank), Betriebskostenparameter, Gesamtkosten je m² (Kauf + Sanierung + Nebenkosten).
Gesucht: maximale Gesamtinvestition, bei der Modus 1 die Zielmiete liefert. Daraus bei gegebenen €/m²: zulässige Gesamtfläche, bei gegebenem Privatraum pro Person: Personenzahl.
Lösung: Bisektion über die Gesamtinvestition, innen Modus 1.

---

## 3. Rechenkern (`model/`)

Reines Python, keine UI-Abhängigkeiten. Jahresauflösung, Horizont `T = 50`. Alle Beträge in Euro nominal; Realwerte werden am Ende über den Inflationsindex abgeleitet.

### 3.1 Datenstrukturen (Dataclasses, alle mit Defaults)

```
Property        purchase_price, renovation_cost, ancillary_cost_rate (Default 0.10),
                tenure: "purchase" | "leasehold", ground_share (Anteil Grundstück am Kaufpreis,
                Default 0.3), leasehold_rate (Erbbauzins p.a. auf Grundstückswert, Default 0.04),
                total_area_m2, private_area_m2_total (Summe Privaträume), replacement_value
                (Default 0.6 × (purchase_price + renovation_cost)), start_year

Tranche         kind: "equity" | "member_loan" | "direct_loan" | "subsidy_loan" | "bank_loan"
                amount, interest_rate, repayment: "annuity" | "linear" | "bullet" | "none",
                term_years, grace_years, fixed_rate_years (Zinsbindung), follow_up_rate,
                drawdown_year, interest_mode: "paid" | "accrued" (nur member_loan/direct_loan),
                churn_rate (nur direct_loan: Anteil p.a. gekündigt), replacement_rate
                (Anteil der Kündigungen, der durch neue Direktkredite ersetzt wird), subsidy_grant
                (Tilgungszuschuss, nur subsidy_loan)

Operations      maintenance_rate (% Wiederherstellungswert p.a., Default 0.015),
                admin_cost_per_year, insurance_per_year, vacancy_rate (Mietausfallwagnis, Default
                0.02), community_cost_per_year, inflation (Default 0.02), rent_mode: "indexed"
                | "fixed", min_liquidity_months (Default 6), start_liquidity

MemberType      name, count, private_area_m2, equity_contribution, member_loan_amount,
                member_loan_rate, member_loan_interest_mode
                (Default: ein Typ, count = Personenzahl, 20 m², gleiche Einlage)

Rules           surplus_use: "rent_reduction" | "payout_15y" | "next_project",
                exit_repayment: "nominal" | "real", payout_interval_years (Default 15)

Scenario        property, tranches: list[Tranche], operations, member_types: list[MemberType],
                rules, horizon_years = 50
```

Konsistenzregel: Summe der Tranchen + Summe der Mitgliedereinlagen und -darlehen = Gesamtinvestition (Kaufpreis + Sanierung + Nebenkosten). Bei Erbbaurecht entfällt der Grundstücksanteil aus der Investition und wird zu einer jährlichen Pacht (inflationsindexiert) in den Betriebskosten. Mitgliedereinlagen und -darlehen werden intern als Tranchen vom Typ `equity` bzw. `member_loan` geführt.

### 3.2 Jahresschleife (`simulate(scenario, rent_per_m2) -> Result`)

Für jedes Jahr t = 1..T:
1. Einnahmen: Miete = rent_per_m2 × private_area_m2_total × 12 × Index(t) (Index = (1+inflation)^t bei `indexed`, sonst 1) × (1 − vacancy_rate).
2. Betriebskosten: maintenance_rate × replacement_value × Index(t) + admin + insurance + community (alle inflationsindexiert) + Erbbauzins (falls leasehold).
3. Kapitaldienst je Tranche: Zins auf Restschuld Jahresanfang; Tilgung je nach `repayment`; Zinsbindung: ab fixed_rate_years gilt follow_up_rate. Bei `accrued` wird der Zins der Restschuld zugeschlagen statt gezahlt. Direktkredite: Kündigungen = churn_rate × Bestand; Ersatz = replacement_rate × Kündigungen (Zufluss); Differenz aus Liquidität.
4. Rücklage: Instandhaltungsrücklage wird als eigener Topf geführt (Zuführung = Posten aus 2, Entnahmen in Version 1 nur als pauschale Jahresausgabe = Zuführung; Topf bleibt als Anzeige).
5. Überschussverwendung (A4), sobald alle Bank- und Fördertranchen getilgt sind: frei gewordener Kapitaldienst → `rent_reduction`: Miete sinkt um diesen Betrag; `payout_15y`: wird angesammelt und alle 15 Jahre gleichmäßig an alle Mitglieder ausgezahlt; `next_project`: Abfluss aus dem Modell.
6. Liquidität(t) = Liquidität(t−1) + Einnahmen − Betrieb − Kapitaldienst ± Direktkreditsaldo − Ausschüttungen.
7. Austritte (nur Modus 2, für das betrachtete Mitglied): Rückzahlung Einlage nach A5 plus Darlehen inkl. aufgelaufener Zinsen im Folgejahr.

Result enthält Zeitreihen (Jahr × Größe) als numpy-Arrays bzw. DataFrame: Miete, Einnahmen, Betrieb, Zins und Tilgung je Tranche, Restschuld je Tranche, Liquidität, Rücklage, Ausschüttungen, Inflationsindex, sowie Kennzahlen: min. Liquidität, Jahr der Banktilgung, Gesamtzinsen, Miete €/m² und €/Person je Typ.

### 3.3 Löser (`solve.py`)
- `required_rent(scenario) -> float` (Modus 1): Bisektion über rent_per_m2 in [0, 50], Abbruch bei 0,01 €.
- `max_investment(scenario_template, target_rent) -> float` (Modus 3): Bisektion über Gesamtinvestition; Tranchen werden aus Quoten abgeleitet.
- `member_view(scenario, member_type, entry_year, exit_year, market_rent, alt_return) -> MemberResult` (Modus 2).

### 3.4 Unsicherheit (`uncertainty.py`)
Jeder numerische Parameter kann statt eines Werts eine Bandbreite `(low, high)` oder `(low, mode, high)` (Dreiecksverteilung) erhalten. `sample(scenario, n=300, method="lhs")` zieht Latin-Hypercube-Stichproben, führt den gewählten Modus aus und liefert Perzentile (10/50/90) der Zeitreihen und Kennzahlen. Rechenzeit im Browser muss unter 5 s bleiben; n ist einstellbar.

### 3.5 Tests (`tests/`)
- Annuität, Ratentilgung, Anlaufjahre, Endfällig gegen geschlossene Formeln (PMT).
- Konsistenz: Summe Tilgungen = Darlehensbetrag; Liquiditätsidentität.
- Monotonie: required_rent steigt mit Bankzins, sinkt mit Eigenkapitalquote.
- Referenzfall gegen die Excel „Finanzplan_Wohnprojekte_Stiftung_trias.xlsx" (Bankdarlehen + Nachrangdarlehen + Mieteinnahmen, Toleranz 1 %). Die Excel liegt in `reference/`; ein Hilfsskript liest die relevanten Zeilen mit openpyxl.

---

## 4. Oberfläche (`app/`)

### 4.1 Technik
Panel (bevorzugt) oder marimo; Export nach WebAssembly über `panel convert` bzw. `marimo export html-wasm`. Diagramme: Plotly. Kein Server, keine Datenbank. Build über GitHub Action nach `gh-pages`. Lokale Entwicklung mit `panel serve`.

### 4.2 Seitenstruktur
1. **Start** – Zweck, die neun Annahmen aus §1, Haftungshinweis (keine Finanz- oder Rechtsberatung), Link zur Methodik.
2. **Modus 1: Miete** – Schicht-1-Regler links, rechts Kennzahlen (Miete €/m², €/Person je Typ, Jahr der Banktilgung) und Diagramme: gestapelte Jahreskosten (Betrieb, Zins, Tilgung) mit Mietlinie; Restschuld je Tranche; Liquidität mit Reserve-Linie.
3. **Modus 2: Vorsorge** – Mitgliedertyp, Eintritts-/Austrittsjahr, Kapitalvariante, Marktmiete, Alternativrendite; Diagramm reales Vermögen Projekt vs. Alternative; Tabelle Endwerte; Ausfallszenario als gestrichelte Linie.
4. **Modus 3: Zielmiete** – Zielmiete, Quoten, €/m²; Ausgabe: zulässige Investition, Fläche, Personenzahl; Diagramm: zulässige Investition als Funktion der Zielmiete (Kurve).
5. **Szenarien** – Dropdown mit Presets (JSON in `scenarios/`), Vergleich von bis zu drei Szenarien nebeneinander, Export/Import des aktuellen Parametersatzes als JSON.
6. **Methodik** – Rechenlogik in Kurzform, Parameterliste mit Defaults und Quellen, Grenzen des Modells.

### 4.3 Komplexitätsschichten
- **Schicht 1 (Standard sichtbar)**: Gesamtinvestition, Privatraum pro Person, Personenzahl, Eigenkapitalquote, Direktkreditquote, Förderquote, Bankzins, Kauf/Erbbaurecht, Rechtsform-Preset, A4-Toggle, A5-Toggle, Mietmodus (A6).
- **Schicht 2 (ausklappbar „Erweitert")**: vollständige Tranchenliste (Tabelle, Zeilen hinzufügen/entfernen), Betriebsparameter, Inflation, Zinsbindung und Anschlusszins, Kündigungs- und Ersatzquote Direktkredite, Mindestreserve, Mitgliedertypen-Tabelle, Privatraum je Mitglied.
- **Schicht 3 (Schalter „Unsicherheit")**: zu jedem Schicht-2-Parameter ein Bandbreitenfeld; Diagramme zeigen Median und 10–90 %-Band; n einstellbar.

### 4.4 Mitgliedertypen
Tabelle mit Spalten: Name, Anzahl, Privatraum m², Einlage, Mitgliederdarlehen, Darlehenszins, Zinsmodus. Default: ein Typ „Standard". Presets: „Wenig Kapital" (Einlage 2.000 €), „Mittel" (10.000 €), „Viel" (50.000 € Einlage + 25.000 € Darlehen). Die Miete ist für alle gleich pro m²; unterschiedliche Einlagen wirken über Modus 2 und über die Gesamtsumme des Eigenkapitals.

### 4.5 Rechtsform-Presets
Nur als Voreinstellung von Parametern, keine Rechtslogik: `eG` (Einlage = Anteile, Mitgliederdarlehen möglich, Verwaltungskosten höher wegen Prüfungsverband), `GmbH` (Einlage klein, Rest Direktkredite), `KG` (Einlage = Kommanditeinlage, kein Direktkreditzwang). Werte im JSON, in der Methodikseite begründet.

### 4.6 Szenario-Presets (`scenarios/*.json`)
Mindestens: `syndikat.json` (6 % EK, 25 % Direktkredite, 69 % Bank), `genossenschaft_gefoerdert.json` (15 % Anteile, 10 % Mitgliederdarlehen, 30 % Förderdarlehen, 45 % Bank, Mietobergrenze), `erbbaurecht_stiftung.json`, `konservativ.json` (hohe Zinsen, hohe Instandhaltung), `optimistisch.json`.

---

## 5. Repository

```
wohnprojekt-dashboard/
  README.md               Kurzbeschreibung, lokaler Start, Deployment
  pyproject.toml          Abhängigkeiten: numpy, pandas, panel, plotly, pytest, openpyxl (nur dev)
  model/
    __init__.py
    types.py              Dataclasses aus §3.1
    cashflow.py           Jahresschleife, Tranchenlogik
    solve.py              required_rent, max_investment, member_view
    uncertainty.py        Bandbreiten, LHS, Perzentile
    presets.py            Laden der JSON-Szenarien, Rechtsform-Presets
  app/
    main.py               Panel-App, Seitenstruktur §4.2
    widgets.py            Schichten, Tranchentabelle, Mitgliedertabelle
    charts.py             Plotly-Figuren
  scenarios/              JSON-Presets
  reference/              trias-Excel + Auslese-Skript für den Referenztest
  tests/
  docs/methodik.md        Inhalt der Methodikseite
  .github/workflows/pages.yml
```

---

## 6. Reihenfolge der Umsetzung

1. `model/types.py`, `model/cashflow.py` mit den vier Tilgungsformen; Tests gegen PMT-Formeln.
2. Direktkredit-Logik (Kündigung/Ersatz), Zinsgutschrift, Erbbaurecht, Überschussverwendung (A4), Austritt (A5).
3. `solve.required_rent`, Referenztest gegen trias-Excel.
4. Panel-App mit Startseite, Modus 1, Schicht 1. Lokaler Lauf.
5. Modus 3, dann Modus 2 inklusive Mitgliedertypen.
6. Schicht 2 und Szenario-Presets, JSON-Export/Import.
7. Schicht 3 (Unsicherheit).
8. WASM-Build, GitHub Action, Deployment auf Pages, Methodikseite.

Jeder Schritt endet mit laufenden Tests. Keine UI-Arbeit, bevor Schritt 3 steht.

---

## 7. Akzeptanzkriterien

- Modus 1 liefert für das Beispiel „2,4 Mio. € Investition, 1.000 m², 20 Personen, 6 % EK, 19 % Direktkredite zu 1 %, 15 % Förderdarlehen zu 1,5 %, 60 % Bank zu 3,8 %/2 % Tilgung, Instandhaltung 20.000 €/Jahr" eine Miete in der Größenordnung von 10–11 €/m² (Plausibilitätsreferenz, kein exakter Zielwert).
- Referenztest gegen trias-Excel innerhalb 1 %.
- Alle Parameter haben Defaults; die App startet ohne Eingaben mit einem sinnvollen Szenario.
- Statische Seite läuft ohne Server im Browser; Rechenzeit Modus 1 < 0,5 s, Unsicherheit mit n = 300 < 5 s.
- Startseite zeigt die Annahmen A1–A9 und den Haftungshinweis.
