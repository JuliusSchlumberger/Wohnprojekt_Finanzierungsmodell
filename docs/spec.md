# Wohnprojekt-Finanzierungsdashboard – Spezifikation

Ziel: Ein statisches, auf GitHub Pages gehostetes Dashboard (Python → WebAssembly), mit dem eine Wohnprojektgruppe Finanzierungsszenarien für ein gemeinsam gekauftes oder im Erbbaurecht genutztes Haus durchspielen kann. Drei Leitfragen, ein gemeinsamer Rechenkern, drei Komplexitätsschichten.

Sprache der Oberfläche: Deutsch (Referenz), Englisch und Niederländisch, umschaltbar in der Kopfzeile; Texte in `app/locale/`. Code, Variablen, Docstrings: Englisch. Dokumentation und Docstrings knapp halten.

---

## 1. Scope und Grundannahmen

Diese Annahmen sind gesetzt und werden auf der Startseite des Dashboards sichtbar aufgeführt.

| Nr. | Annahme | Festlegung |
|---|---|---|
| A1 | Eigentumsmodell | Ein gemeinsamer Rechtsträger (eG, GmbH, GmbH & Co. KG) kauft das Haus oder nutzt es im Erbbaurecht. Mitglieder zahlen ein Nutzungsentgelt („Miete"). Kein Einzeleigentum, kein WEG-Modell. |
| A2 | Mieteinheit | Miete pro Person und Monat, für alle gleich. Gemeinschaftsflächen sind darin enthalten; Privatflächen werden nicht unterschieden. |
| A3 | Kapitalbeiträge | Einzelpersonen (nicht Haushalte) bringen unterschiedlich viel ein. Modelliert über Mitgliedertypen (siehe §4.4). |
| A4 | Verwendung frei werdenden Geldes | Toggle mit drei Optionen: `rent_reduction` (Mietsenkung), `payout_15y` (Mietrückzahlung an alle Mitglieder alle 15 Jahre), `next_project` (Solidartransfer, Geld verlässt das Modell). Gilt für den nach Tilgung von Bank- und Förderdarlehen frei werdenden Kapitaldienst und für die Liquidität oberhalb von Mindestreserve plus allen offenen Direkt- und Mitgliederdarlehen (inkl. aufgelaufener Zinsen), sobald kein Rückstand offen ist. |
| A5 | Einlagen | Einlage = Genossenschaftsanteil bzw. Einlage in den Rechtsträger. Bei Austritt inflationsindexiert zurückgezahlt; neue Mitglieder kaufen sich zum selben Wert ein, der Bestand im Projekt bleibt konstant (keine Zahlungsströme im Projekt). |
| A6 | Zeithorizont und Inflation | 50 Jahre. Miete, Betriebskosten und Erbbauzins steigen mit der Inflation (wählbar); Zins und Tilgung sind nominal fest. Zinssätze werden in der App als Abstand zur Inflation (Prozentpunkte) eingegeben: Nominalzins = max(Inflation + Abstand, 0). Grafiken wahlweise inflationsbereinigt (Kaufkraft Jahr 1) oder nominal. |
| A7 | Mindestliquidität | Konto darf nie unter 6 Monatsmieten (Summe aller Mitglieder) fallen. |
| A8 | Steuern | Nicht modelliert in Version 1. Sichtbar deklariert. |
| A9 | Direkt- und Mitgliederdarlehen | Nachrangig und endfällig. Direktkredite: Laufzeit 5 oder 10 Jahre, je eigener Betrag und Zins, Zinsen jährlich ausgezahlt. Mitgliederdarlehen: Laufzeit einstellbar (Standard 15 Jahre), Zinsen thesauriert, Rückzahlung samt Zinseszins. Was am Fälligkeitstag nicht ohne Unterschreiten der Mindestreserve zurückgezahlt werden kann, bleibt als Rückstand stehen, verzinst sich zum Satz des Darlehens und wird so schnell wie möglich nachgezahlt; Rückstände müssen nach spätestens 3 Jahren beglichen sein (Bedingung für die erforderliche Miete). Ablösung der Mitgliederdarlehen wählbar (`member_loan_payoff`): `liquidity` (aus dem Konto, Rückstandsregel), `bank` (neues Bankdarlehen über den vollen fälligen Betrag samt Zinsen zum Anschlusszins, Tilgungsart der Bank, Laufzeit Rest der Banklaufzeit, mindestens 10 Jahre) oder `direct_loans` (neue endfällige 10-Jahres-Direktkredite zum DK10-Zins). Zufluss am Ende des Fälligkeitsjahres, Bedienung ab dem Folgejahr. Sonst keine neuen Darlehen. Die reale Restschuld nach 50 Jahren wird angezeigt. |

---

## 2. Die drei Leitfragen (Modi)

Alle drei laufen auf demselben Rechenkern (§3). Sie unterscheiden sich nur darin, welche Größe gesucht wird.

### Modus 1 – Erforderliche Miete
Eingabe: Kosten + Kapitalstapel. Gesucht: die niedrigste Miete pro Person und Monat (im Startjahr, danach inflationsindexiert), bei der die Liquidität in jedem Jahr ≥ Mindestreserve bleibt.
Ausgabe: Miete €/Person/Monat, €/Jahr gesamt, engstes Jahr; Zeitverlauf von Liquidität, Restschuld je Tranche, Kapitaldienst; Jahr der Banktilgung; Entwicklung der Miete nach Tilgung je nach A4.

Lösung: Bisektion über die Miete, Zielfunktion = min über Jahre von (Liquidität − Reserve). Monoton, daher robust.

### Modus 2 – Altersvorsorge-Perspektive
Eingabe: alle Annahmen aus Modus 1 plus für ein Mitglied: Mitgliedertyp (Voreinstellung),
Einlage, eigenes Mitgliederdarlehen, Einzugs- und Auszugsjahr, Marktmiete pro Person,
Alternativrendite. Projektmiete = erforderliche Miete aus Modus 1.
Gesucht: reale Vermögensentwicklung des Mitglieds im Vergleich zur Alternative „Marktmiete
zahlen, Geld anlegen".
Ausgabe (alles in Kaufkraft von Jahr 1):
- Im Projekt: alle Zahlungen an das Mitglied (Ersparnis gegenüber Marktmiete,
  Mietrückzahlungen, zurückgezahltes Darlehen und Einlage) werden zur Alternativrendite
  angelegt; Einlage (real, A5) und Darlehen (mit Zinseszins) zählen, solange sie im Projekt
  stecken.
- Vergleichspfad: Einlage und Darlehensbetrag zur Alternativrendite angelegt, Marktmiete
  gezahlt.
- Vorsorgevorteil = Differenz, als Zeitreihe und Endwert.
- Ausfallszenario (Einlage und Darlehen = 0) als gestrichelte Linie.
- Das einzelne Mitglied wirkt nicht auf die Projektfinanzierung zurück.

### Modus 3 – Zulässige Investition bei Zielmiete
Leitfrage: „Wie viel Haus kann sich unsere Gruppe leisten?"
Eingabe: Zielmiete €/Person/Monat sowie alle übrigen Eingaben (Kosten als Schätzung, Eigenmittel als Beträge: Einlagen, Mitgliederdarlehen, Direktkredite, Förderdarlehen; das Bankdarlehen wächst mit der Investition), Mindestanteil Eigenkapital + Nachrang der Bank.
Gesucht: maximale Gesamtinvestition als Minimum zweier Grenzen: (a) größte Investition, deren erforderliche Miete (Modus 1) die Zielmiete nicht übersteigt, wobei Grundstück, Haus und Sanierung im Verhältnis der Kostenschätzung skaliert werden; (b) (Einlagen + Mitgliederdarlehen + Direktkredite) / Mindestanteil. Ausgabe zusätzlich: Anteil der Kostenschätzung, der zulässig ist.
Lösung: (a) Bisektion über die Gesamtinvestition mit der Bedingung Liquidität ≥ Reserve bei Zielmiete; (b) geschlossen.

---

## 3. Rechenkern (`model/`)

Reines Python, keine UI-Abhängigkeiten. Jahresauflösung, Horizont `T = 50`. Alle Beträge in Euro nominal; Realwerte werden am Ende über den Inflationsindex abgeleitet.

### 3.1 Datenstrukturen (Dataclasses, alle mit Defaults)

```
Property        purchase_price, renovation_cost, ancillary_cost_rate (Default 0.10),
                tenure: "purchase" | "leasehold", ground_share (Anteil Grundstück am Kaufpreis,
                Default 0.3), leasehold_rate (Erbbauzins p.a. auf Grundstückswert, Default 0.04),
                total_area_m2 (nur Plausibilitätskennzahl), replacement_value
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

MemberType      name, count, equity_contribution, member_loan_amount,
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
1. Einnahmen: Miete = rent_per_person × persons × 12 × Index(t) (Index = (1+inflation)^t bei `indexed`, sonst 1) × (1 − Mietausfall); Mietausfall in den ersten 3 Jahren `initial_vacancy_rate` (App: 20 %), danach `vacancy_rate` (App: 4 %).
2. Betriebskosten: maintenance_rate × replacement_value × Index(t) + admin + insurance + community (alle inflationsindexiert) + Erbbauzins (falls leasehold).
3. Kapitaldienst je Tranche: Zins auf Restschuld Jahresanfang; Tilgung je nach `repayment`; Zinsbindung: ab fixed_rate_years gilt follow_up_rate. Bei `accrued` wird der Zins der Restschuld zugeschlagen statt gezahlt. Direkt- und Mitgliederdarlehen endfällig; Rückstände nach A9, Jahr für Jahr (älteste zuerst, nur bis zur Mindestreserve).
4. Rücklage: Instandhaltungsrücklage als eigener Topf außerhalb der Liquidität. Zuführung = 2 % des Wiederherstellungswerts × Index(t) (wählbar), Entnahme = laufende Instandhaltung (1,5 %); die Zuführung ist der Kostenposten für die Miete.
5. Überschussverwendung (A4): frei gewordener Kapitaldienst nach Tilgung aller Bank- und Fördertranchen sowie, wenn kein Rückstand offen ist, die Liquidität oberhalb von Reserve plus aller offenen Direkt- und Mitgliederdarlehen → `rent_reduction`: Miete sinkt um diesen Betrag; `payout_15y`: wird angesammelt und alle 15 Jahre an alle Mitglieder zurückgezahlt (Mietrückzahlung); `next_project`: Abfluss aus dem Modell.
6. Liquidität(t) = Liquidität(t−1) + Einnahmen − Betrieb − Kapitaldienst ± Direktkreditsaldo − Ausschüttungen.
7. Austritte (nur Modus 2, für das betrachtete Mitglied): Rückzahlung Einlage nach A5 plus Darlehen inkl. aufgelaufener Zinsen im Folgejahr.

Result enthält Zeitreihen (Jahr × Größe) als numpy-Arrays bzw. DataFrame: Miete, Einnahmen, Betrieb, Zins und Tilgung je Tranche, Restschuld je Tranche, Liquidität, Rücklage, Ausschüttungen, Inflationsindex, sowie Kennzahlen: min. Liquidität, Jahr der Banktilgung, Gesamtzinsen, Miete €/Person.

### 3.3 Löser (`solve.py`)
- `required_rent(scenario) -> float` (Modus 1): Bisektion über rent_per_m2 in [0, 50], Abbruch bei 0,01 €.
- `max_investment(scenario_for, target_rent, lower) -> float` (Modus 3, Grenze a): Bisektion über Gesamtinvestition; `scenario_for` baut das Szenario für eine Investition, Eigenmittel fest, Bank als Rest.
- `member.member_view(scenario, result, MemberInputs) -> DataFrame` (Modus 2).

### 3.4 Unsicherheit (`uncertainty.py`)
Acht Eingaben bekommen eine Spanne `(low, high)`; der aktuelle Wert ist der wahrscheinlichste (Dreiecksverteilung): Inflation, Bankzins nach Ende der Zinsbindung (± Prozentpunkte), Mietausfall, Sanierungskosten und Verwaltung + Versicherung (als Faktor auf die Schätzung), Laufzeit der Mitgliederdarlehen (ganze Jahre) sowie Umfang der Mitgliederdarlehen und der 10-Jahres-Direktkredite (als Faktor auf die Planung; fehlender Betrag geht ans Bankdarlehen). `rent_uncertainty(inputs, ranges, n, seed)` zieht n Latin-Hypercube-Stichproben (fester Startwert), sucht je Variante die erforderliche Miete (Klammer um die Basismiete, auf 0,50 € genau) und liefert Perzentile 10/50/90, die sichere Miete (90. Perzentil), das Band des Puffers über der Mindestreserve bei sicherer Miete und die Rangkorrelation jeder Eingabe mit der Miete. Zinssätze (Bank, Förderung, DK5, DK10, Mitgliederdarlehen) verschieben sich mit der gezogenen Inflation, der Abstand bleibt. Das Pufferband gibt es real und nominal. Standard 150 Varianten (≈ 3,8 s im Browser).

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
1. **Start** – Zweck, alle Eingaben (gruppiert), die neun Annahmen aus §1, Haftungshinweis. Eingaben sind über alle Seiten geteilt: eine Änderung auf einer Seite gilt sofort überall.
2. **Modus 1: Miete** – Hauptstellschrauben links (Grundstück, Haus, Sanierung, Kauf/Erbbaurecht, Einlagen, Mitgliederdarlehen, Direktkredite, Förderdarlehen, Bankzins, Inflation) mit automatisch berechnetem Bankdarlehen und Eigenkapitalprüfung; rechts Kennzahlen (Miete €/Person, Jahr der Banktilgung, engstes Jahr) und Diagramme: gestapelte Jahreskosten mit Mietlinie; Restschuld je Darlehen; Liquidität mit Reserve-Linie.
3. **Modus 2: Vorsorge** – Mitgliedertyp, Einlage, eigenes Mitgliederdarlehen, Ein-/Auszugsjahr, Marktmiete, Alternativrendite; Diagramm reales Vermögen Projekt vs. Alternative, Ausfallszenario gestrichelt; Kennzahlen mit Endwerten.
4. **Modus 3: Zielmiete** – Zielmiete pro Person, Eigenmittel, Bankzins, Inflation, Mindestanteil; Ausgabe: zulässige Investition mit bindender Grenze und Anteil der Kostenschätzung; Diagramm: zulässige Investition als Funktion der Zielmiete (Kurve) mit Eigenkapitalgrenze.
5. **Szenarien** – Dropdown mit Presets (JSON in `scenarios/`), Vergleich von bis zu drei Szenarien nebeneinander, Export/Import des aktuellen Parametersatzes als JSON.
6. **Methodik** – Rechenlogik in Kurzform, Parameterliste mit Defaults und Quellen, Grenzen des Modells.

### 4.3 Komplexitätsschichten
- **Schicht 1 (Startseite, geteilt)**: Grundstück, Haus, Sanierung (Kaufnebenkosten 10 % automatisch), Kauf/Erbbaurecht, Personenzahl, Inflation, A4-Toggle; Einlagen; Mitgliederdarlehen (Betrag, Zins); Direktkredite 5 und 10 Jahre (je Betrag, Zins); Förderdarlehen (höchstens Sanierungskosten); Bank (Zins, Annuität/Ratenkredit, Laufzeit, Zins nach 10 Jahren −1/±0/+1 Prozentpunkt), Mindestanteil Eigenkapital + Nachrang, Zielmiete. Rechtsform-Preset folgt mit Schritt 6.
- **Schicht 2 (Startseite, ausklappbar „Erweitert“)**: Verwaltung und Versicherung pro Jahr, tatsächliche Instandhaltung (% Wiederherstellungswert), Mindestreserve (Monatsmieten), maximale Dauer von Rückständen, Kaufnebenkostensatz, Erbbauzinssatz, Zins und Laufzeit der Förderdarlehen, Laufzeit der Mitgliederdarlehen. Keine frei editierbare Darlehensliste und keine Mitgliedertypen-Tabelle: Darlehensarten sind fest, Einlagen und Mitgliederdarlehen gelten pro Person.
- **Schicht 3 (eigene Seite „Unsicherheit“)**: Spannen für die acht Eingaben aus §3.4, Anzahl Varianten (50–300), Rechnung nur auf Knopfdruck; Ergebnisse werden als veraltet markiert, sobald sich eine Annahme ändert. Ausgabe: Kennzahlen (Median, Spanne, sichere Miete), Verteilung der Miete, Pufferband, Treiber der Unsicherheit.

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
    solve.py              required_rent, max_investment
    member.py             member_view (Modus 2)
    uncertainty.py        Bandbreiten, LHS, Perzentile
    presets.py            Laden der JSON-Szenarien, Rechtsform-Presets
  app/
    main.py               Panel-App, Seitenstruktur §4.2
    widgets.py            Schichten, Tranchentabelle, Mitgliedertabelle
    charts.py             Plotly-Figuren
  scenarios/              JSON-Presets
  reference/              trias-Excel + Auslese-Skript für den Referenztest
  tests/
  app/methodik.md         Inhalt der Methodikseite (Paketdaten, auch im Browser-Build)
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
