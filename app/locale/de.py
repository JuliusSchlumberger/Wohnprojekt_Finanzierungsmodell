"""German UI texts; the reference language. Keys are shared by all languages."""

TEXTS = {
    # App frame and navigation
    "app.title": "Wohnprojekt-Rechner",
    "app.language": "Sprache",
    "nav.start": "Start",
    "nav.mode1": "Modus 1: Miete",
    "nav.mode2": "Modus 2: Vorsorge",
    "nav.mode3": "Modus 3: Zielmiete",
    "nav.uncertainty": "Unsicherheit",
    "nav.methodik": "Methodik",
    # Start page
    "start.intro": """
Mit diesem Rechner kann eine Wohnprojektgruppe durchspielen, wie sich ein gemeinsam
gekauftes oder im Erbbaurecht genutztes Haus finanzieren lässt. Hier stellt ihr alle
Annahmen ein; auf den Modus-Seiten lassen sich die wichtigsten davon direkt ändern.
Jede Änderung gilt sofort auf allen Seiten. Das **?** neben einem Feld oder einer
Kennzahl erklärt, was dahintersteckt.
""",
    "start.mode1.question": "Welche Miete pro Person braucht unser Haus mindestens?",
    "start.mode2.question": "Lohnt sich das Projekt für ein Mitglied gegenüber Marktmiete?",
    "start.mode3.question": "Wie viel Haus kann sich unsere Gruppe bei einer Zielmiete leisten?",
    "start.heading": "Annahmen einstellen",
    "start.disclaimer": (
        "**Haftungshinweis:** Dieser Rechner ist ein Planungswerkzeug und keine Finanz-, Steuer- "
        "oder Rechtsberatung. Alle Ergebnisse hängen von den Annahmen ab."
    ),
    "start.advanced": "Erweitert: Betrieb, Reserve, Nebenkosten, Förderkonditionen",
    # Assumptions A1-A9
    "assumptions.title": "Annahmen des Modells (A1–A9)",
    "assumptions.header": "| Nr. | Annahme | Festlegung |",
    "assumption.1.title": "Eigentumsmodell",
    "assumption.1.text": (
        "Ein gemeinsamer Rechtsträger (eG, GmbH, GmbH & Co. KG) kauft das Haus oder nutzt es "
        "im Erbbaurecht. Mitglieder zahlen ein Nutzungsentgelt („Miete“). Kein Einzeleigentum."
    ),
    "assumption.2.title": "Mieteinheit",
    "assumption.2.text": (
        "Miete pro Person und Monat, für alle gleich. Gemeinschaftsflächen sind darin enthalten."
    ),
    "assumption.3.title": "Kapitalbeiträge",
    "assumption.3.text": "Einzelpersonen bringen unterschiedlich viel ein (Mitgliedertypen).",
    "assumption.4.title": "Frei werdendes Geld",
    "assumption.4.text": (
        "Nach Tilgung von Bank- und Förderdarlehen und sobald alle Direkt- und "
        "Mitgliederdarlehen gedeckt sind: Mietsenkung, Mietrückzahlung alle 15 Jahre oder "
        "Solidartransfer an ein nächstes Projekt."
    ),
    "assumption.5.title": "Einlagen",
    "assumption.5.text": (
        "Bei Austritt inflationsindexiert zurückgezahlt; neue Mitglieder kaufen sich zum "
        "selben Wert ein. Der Bestand im Projekt bleibt konstant."
    ),
    "assumption.6.title": "Zeithorizont und Inflation",
    "assumption.6.text": (
        "50 Jahre. Miete, Betriebskosten und Erbbauzins steigen mit der Inflation; Zins und "
        "Tilgung sind nominal fest."
    ),
    "assumption.7.title": "Mindestliquidität",
    "assumption.7.text": "Das Konto fällt nie unter die Mindestreserve (Standard 6 Monatsmieten).",
    "assumption.8.title": "Steuern",
    "assumption.8.text": "Nicht modelliert.",
    "assumption.9.title": "Direkt- und Mitgliederdarlehen",
    "assumption.9.text": (
        "Nachrangig und endfällig. Direktkredite laufen 5 oder 10 Jahre, Zinsen jährlich "
        "ausgezahlt; Mitgliederdarlehen mit einstellbarer Laufzeit (Standard 15 Jahre), Zinsen "
        "thesauriert. Was am Fälligkeitstag "
        "nicht ohne Unterschreiten der Mindestreserve zurückgezahlt werden kann, wird so "
        "schnell wie möglich nachgezahlt, innerhalb einer Frist (Standard 3 Jahre), und verzinst "
        "sich bis dahin."
    ),
    # Input sections
    "section.house": "Haus und Kosten",
    "section.group": "Gruppe und Betrieb",
    "section.own_funds": "Eigenmittel",
    "section.direct_loans": "Direktkredite",
    "section.bank": "Bank und Förderung",
    "section.surplus": "Überschuss und Zielmiete",
    "section.member_capital": "Mitglied: Kapital (Modus 2)",
    "section.member_compare": "Mitglied: Vergleich (Modus 2)",
    "section.adv_operations": "Betrieb",
    "section.adv_liquidity": "Liquidität und Rückstände",
    "section.adv_purchase": "Kauf und Erbbaurecht",
    "section.adv_subsidy": "Förderdarlehen",
    "section.adv_member_loans": "Mitgliederdarlehen",
    # Input labels
    "label.land_price": "Grundstück (€)",
    "label.building_price": "Haus (€)",
    "label.renovation_cost": "Sanierung (€)",
    "label.tenure": "Grundstück",
    "label.persons": "Personenzahl",
    "label.equity_per_person": "Einlage pro Person (€)",
    "label.member_loan_per_person": "Mitgliederdarlehen pro Person (€)",
    "label.direct_loans_5y": "Direktkredite 5 Jahre (€)",
    "label.direct_loans_10y": "Direktkredite 10 Jahre (€)",
    "label.subsidy": "Förderdarlehen (€)",
    "label.bank_repayment": "Tilgungsform Bank",
    "label.bank_term_years": "Laufzeit Bank (Jahre)",
    "label.bank_rate_change": "Bankzins nach 10 Jahren",
    "label.inflation_pct": "Inflation (%)",
    "label.surplus_use": "Nach Tilgung von Bank- und Förderdarlehen",
    "label.min_equity_like_pct": "Mindestanteil EK + Nachrang (%)",
    "label.target_rent": "Zielmiete pro Person (€/Monat)",
    "label.maintenance_reserve_pct": "Instandhaltungsrücklage (%)",
    "label.vacancy_pct": "Mietausfall (%)",
    "label.initial_vacancy_pct": "Mietausfall erste 3 Jahre (%)",
    "label.admin_cost_per_year": "Verwaltung pro Jahr (€)",
    "label.insurance_per_year": "Versicherung pro Jahr (€)",
    "label.min_liquidity_months": "Mindestreserve (Monatsmieten)",
    "label.max_arrears_years": "Rückstand höchstens (Jahre)",
    "label.ancillary_cost_pct": "Kaufnebenkosten (%)",
    "label.leasehold_rate_pct": "Erbbauzins (%)",
    "label.subsidy_term_years": "Laufzeit Förderdarlehen (Jahre)",
    "label.member_loan_term_years": "Laufzeit Mitgliederdarlehen (Jahre)",
    "label.member_type": "Mitgliedertyp",
    "label.member_equity": "Einlage (€)",
    "label.member_loan_personal": "Mitgliederdarlehen (€)",
    "label.entry_year": "Einzug (Jahr)",
    "label.exit_year": "Auszug (Jahr)",
    "label.market_rent": "Marktmiete pro Person (€/Monat)",
    "label.inflation_range": "Inflation (%)",
    "label.bank_change_range": "Bankzins nach 10 J. (± Pp.)",
    "label.vacancy_range": "Mietausfall (%)",
    "label.renovation_range": "Sanierung (% der Schätzung)",
    "label.running_range": "Verwaltung, Versicherung (%)",
    "label.n_samples": "Anzahl Varianten",
    # Options of choice inputs
    "option.tenure.purchase": "Kauf",
    "option.tenure.leasehold": "Erbbaurecht",
    "option.bank_repayment.annuity": "Annuität",
    "option.bank_repayment.linear": "Ratenkredit",
    "option.bank_rate_change.down": "sinkt",
    "option.bank_rate_change.same": "bleibt",
    "option.bank_rate_change.up": "steigt",
    "option.surplus_use.rent_reduction": "Mietsenkung",
    "option.surplus_use.payout_15y": "Mietrückzahlung alle 15 Jahre",
    "option.surplus_use.next_project": "Solidartransfer",
    "option.member_type.custom": "Eigene Angaben",
    "option.member_type.low": "Wenig Kapital",
    "option.member_type.mid": "Mittel",
    "option.member_type.high": "Viel",
    # Input explanations
    "info.land_price": (
        "Kaufpreis des Grundstücks. Bei Erbbaurecht wird es nicht gekauft; der Betrag gilt "
        "dann als Grundstückswert, auf den der Erbbauzins (Satz unter „Erweitert“) berechnet wird."
    ),
    "info.building_price": "Kaufpreis des Hauses ohne Grundstück.",
    "info.renovation_cost": (
        "Kosten für Sanierung und Umbau. Nur dafür können Förderdarlehen eingesetzt werden."
    ),
    "info.tenure": (
        "Kauf: das Grundstück wird mitfinanziert, auch die Kaufnebenkosten darauf. "
        "Erbbaurecht: das Grundstück wird nicht gekauft, stattdessen fällt jährlich ein "
        "Erbbauzins auf den Grundstückswert an (Standard 4 %, unter „Erweitert“), der mit der "
        "Inflation steigt."
    ),
    "info.persons": "Anzahl der Personen, die im Projekt wohnen und Miete zahlen.",
    "info.equity_per_person": (
        "Einlage pro Person (Genossenschaftsanteil bzw. Einlage in den Rechtsträger). "
        "Einlagen kosten keine Zinsen und werden nicht getilgt. Wer auszieht, bekommt die "
        "Einlage inflationsindexiert zurück; neue Mitglieder kaufen sich zum selben Wert ein. "
        "Der Bestand im Projekt bleibt deshalb konstant."
    ),
    "info.member_loan_per_person": (
        "Mitgliederdarlehen pro Person. Die Zinsen werden nicht ausgezahlt, sondern jährlich "
        "dem Darlehen gutgeschrieben (thesauriert). Am Ende der Laufzeit (Standard 15 Jahre, "
        "unter „Erweitert“) wird "
        "alles samt Zinseszins auf einmal zurückgezahlt."
    ),
    "info.direct_loans_5y": (
        "Nachrangige Privatdarlehen von Unterstützer*innen über 5 Jahre. Zinsen werden "
        "jährlich ausgezahlt, der Betrag nach 5 Jahren auf einmal zurück. Banken werten "
        "Direktkredite wegen des Nachrangs meist als eigenkapitalähnlich."
    ),
    "info.direct_loans_10y": (
        "Wie oben, aber über 10 Jahre. Längere Laufzeiten haben meist einen höheren Zins."
    ),
    "info.subsidy": (
        "Förderdarlehen (z. B. KfW oder Landesförderbank) als Annuität; Zins und Laufzeit "
        "unter „Erweitert“ (Standard 1,5 % über 30 Jahre). Nur für Sanierungskosten nutzbar, "
        "deshalb höchstens so hoch wie diese. "
        "Zählt nicht als eigenkapitalähnlich."
    ),
    "info.bank_repayment": (
        "Annuität: gleichbleibende Rate aus Zins und Tilgung, anfangs viel Zins. "
        "Ratenkredit: gleichbleibende Tilgung, die Rate ist anfangs höher und sinkt dann."
    ),
    "info.bank_term_years": "Laufzeit, nach der das Bankdarlehen vollständig getilgt ist.",
    "info.bank_rate_change": (
        "Nach 10 Jahren endet die Zinsbindung. Für die Anschlussfinanzierung wird der Zins "
        "um 1 Prozentpunkt gesenkt, beibehalten oder erhöht."
    ),
    "info.surplus_use": (
        "Gilt ab dem Jahr, in dem Bank- und Förderdarlehen getilgt sind (A4). Mietsenkung: "
        "die Miete sinkt um den frei gewordenen Kapitaldienst. Mietrückzahlung: der Betrag "
        "wird angespart und alle 15 Jahre an alle Mitglieder zurückgezahlt. "
        "Solidartransfer: das Geld geht an ein nächstes Projekt. Die erforderliche "
        "Anfangsmiete ändert sich dadurch in der Regel nicht, nur der Verlauf danach."
    ),
    "info.min_equity_like_pct": (
        "Banken verlangen meist, dass Eigenkapital und nachrangige Mittel (Einlagen, "
        "Mitgliederdarlehen, Direktkredite) einen Mindestanteil der Gesamtinvestition "
        "decken, oft 20 bis 30 %. Tragt hier die Anforderung eurer Bank ein."
    ),
    "info.vacancy_pct": (
        "Anteil der Miete, der im Schnitt ausfällt, z. B. durch Leerstand bei Wechseln oder "
        "Zahlungsausfälle. Gilt ab dem 4. Jahr."
    ),
    "info.initial_vacancy_pct": (
        "Mietausfall in den ersten 3 Jahren, solange das Haus noch bezogen und saniert wird."
    ),
    "info.admin_cost_per_year": (
        "Verwaltung, Buchhaltung, Prüfung (bei eG Prüfungsverband), Bankgebühren. Steigt mit "
        "der Inflation."
    ),
    "info.insurance_per_year": "Gebäude- und Haftpflichtversicherung. Steigt mit der Inflation.",
    "info.min_liquidity_months": (
        "So viele Monatsmieten muss das Konto immer mindestens enthalten. Sie wird zu Beginn "
        "über das Bankdarlehen finanziert. Mehr Reserve heißt mehr Sicherheit, aber auch eine "
        "höhere Miete."
    ),
    "info.max_arrears_years": (
        "Wie lange eine fällige Rückzahlung von Direkt- oder Mitgliederdarlehen höchstens "
        "aufgeschoben werden darf. 0 heißt: alles muss pünktlich gezahlt werden."
    ),
    "info.ancillary_cost_pct": (
        "Grunderwerbsteuer, Notar, Grundbuch und ggf. Makler, in % des Kaufpreises von Haus "
        "und (bei Kauf) Grundstück. Die Grunderwerbsteuer liegt je nach Bundesland bei "
        "3,5 bis 6,5 %."
    ),
    "info.leasehold_rate_pct": (
        "Jährlicher Erbbauzins in % des Grundstückswerts. Steigt mit der Inflation. Gilt nur "
        "bei Erbbaurecht."
    ),
    "info.member_loan_term_years": (
        "Nach so vielen Jahren werden Mitgliederdarlehen samt aufgelaufener Zinsen auf "
        "einmal zurückgezahlt. Längere Laufzeiten schieben die große Rückzahlung nach "
        "hinten, lassen aber mehr Zinseszins auflaufen."
    ),
    "info.subsidy_term_years": "Laufzeit der Förderdarlehen; sie werden als Annuität getilgt.",
    "info.maintenance_reserve_pct": (
        "So viel vom Wiederherstellungswert (60 % von Haus plus Sanierung, ohne Grundstück) "
        "wird jedes Jahr für Instandhaltung zurückgelegt und ausgegeben, mit der Inflation "
        "steigend."
    ),
    "info.member_type": (
        "Voreinstellungen für Einlage und Mitgliederdarlehen dieses Mitglieds. "
        "„Eigene Angaben“ lässt die Werte frei einstellen."
    ),
    "info.member_equity": (
        "Einlage dieses Mitglieds in heutigem Geld. Sie wird beim Einzug "
        "inflationsindexiert eingezahlt und beim Auszug inflationsindexiert zurückgezahlt."
    ),
    "info.member_loan_personal": (
        "Mitgliederdarlehen dieses Mitglieds. Es wird zum Zins der Mitgliederdarlehen "
        "thesauriert und am Ende der Laufzeit oder im Jahr nach dem Auszug samt Zinseszins "
        "zurückgezahlt."
    ),
    "info.entry_year": "Jahr des Einzugs, gezählt ab Projektstart (0 = von Anfang an).",
    "info.exit_year": "Jahr des Auszugs. Einlage und Darlehen kommen im Jahr danach zurück.",
    "info.market_rent": (
        "Was eine vergleichbare Wohnung bzw. ein Zimmer am Markt pro Person und Monat "
        "kostet, in derselben Einheit wie die Projektmiete. Steigt mit der Inflation."
    ),
    "info.target_rent": (
        "Die Miete, die eine Person im ersten Jahr zahlen will oder kann, pro Monat. "
        "Danach steigt sie mit der Inflation."
    ),
    "info.bank_loan": (
        "Das Bankdarlehen schließt die Lücke: Gesamtinvestition + Startliquidität "
        "(Mindestreserve) − Einlagen − Mitgliederdarlehen − Direktkredite − "
        "Förderdarlehen. Weil die Startliquidität von der Miete abhängt, wird es zusammen "
        "mit der Miete berechnet."
    ),
    "info.inflation_range": "Spanne der jährlichen Inflation. Wahrscheinlichster Wert: Startseite.",
    "info.bank_change_range": (
        "Änderung des Bankzinses nach Ende der Zinsbindung (10 Jahre), in Prozentpunkten. "
        "Wahrscheinlichster Wert: die Wahl auf der Startseite (sinkt −1, bleibt 0, steigt +1)."
    ),
    "info.vacancy_range": (
        "Spanne des Mietausfalls ab dem 4. Jahr. Wahrscheinlichster Wert: Startseite."
    ),
    "info.renovation_range": (
        "Sanierungskosten in % eurer Schätzung. 130 % heißt: die Sanierung wird 30 % teurer. "
        "Wahrscheinlichster Wert: 100 %."
    ),
    "info.running_range": (
        "Verwaltung und Versicherung in % eurer Schätzung. Wahrscheinlichster Wert: 100 %."
    ),
    "info.n_samples": (
        "Mehr Varianten machen das Ergebnis stabiler, dauern aber länger (im Browser etwa "
        "2,5 Sekunden pro 100 Varianten)."
    ),
    # Summaries under input boxes
    "summary.costs": "Kaufnebenkosten ({rate}): **{ancillary}**  \nGesamtinvestition: **{total}**",
    "summary.costs_unknown": "Gesamtinvestition: –",
    "summary.capital": (
        "Einlagen gesamt: **{equity}**  \nMitgliederdarlehen gesamt: **{member_loans}**"
    ),
    # Shared page elements
    "ui.levers": "Stellschrauben",
    "ui.more_on_start": "*Alle weiteren Annahmen auf der Startseite.*",
    "ui.how_computed": "So wird gerechnet",
    "ui.no_solution": "Keine Lösung: {error}",
    "ui.how_to_read": "Wie lese ich diese Grafik?",
    "ui.values_table": "Werte als Tabelle",
    "ui.year": "Jahr",
    # Errors
    "error.subsidy_above_renovation": (
        "Förderdarlehen ({subsidy}) sind nur für Sanierung nutzbar und "
        "übersteigen die Sanierungskosten ({renovation})."
    ),
    "error.zero_price": "Grundstück und Haus dürfen nicht beide 0 € kosten.",
    "error.own_funds_above_investment": (
        "Eigenmittel und Förderdarlehen ({own}) übersteigen die "
        "Gesamtinvestition ({total}). Bitte Beträge reduzieren."
    ),
    "error.exit_before_entry": "Der Auszug muss nach dem Einzug liegen.",
    "error.rent_too_low_for_own_funds": (
        "Schon ein Haus in Höhe eurer Eigenmittel ({lower}) braucht mehr als "
        "{target} Miete pro Person. Zielmiete erhöhen oder Eigenmittel ändern."
    ),
    "error.no_upper_bound": "Keine obere Grenze für die Investition gefunden; Eingaben prüfen.",
    "error.bank_rule_no_house": (
        "Die Eigenkapitalanforderung der Bank lässt kein Haus zu, das eure Eigenmittel "
        "aufnimmt: Einlagen, Mitgliederdarlehen und Direktkredite sind im Verhältnis zu "
        "den Förderdarlehen zu klein."
    ),
    # Bank loan and equity check
    "bank.line": "**Bankdarlehen (automatisch): {amount}**",
    "bank.check": (
        "Eigenkapital + Nachrang: {equity_like} = {share} der "
        "Gesamtinvestition (Mindestanteil {min_share}). "
        "Bankdarlehen : Eigenkapital + Nachrang = {ratio}."
    ),
    "bank.missing": (
        "{check} Es fehlen {gap} Einlagen, Mitgliederdarlehen oder "
        "Direktkredite; so finanziert eine Bank vermutlich nicht."
    ),
    # Methods
    "method.mode1": """
Das Modell rechnet 50 Jahre in Jahresschritten. Jedes Jahr gilt:
**Konto neu = Konto alt + Mieteinnahmen − Betriebskosten − Zinsen − Tilgung**
(abzüglich Rückzahlung fälliger Direkt- und Mitgliederdarlehen, Mietsenkung aus dem
Überschuss, Mietrückzahlung oder Solidartransfer).

- **Mieteinnahmen**: Miete × Personen × 12, abzüglich Mietausfall (in den ersten
  3 Jahren höher).
- **Betriebskosten**: Zuführung zur Instandhaltungsrücklage (Anteil des
  Wiederherstellungswerts), Verwaltung und Versicherung.
- **Zins und Tilgung**: je Darlehen nach seinen Konditionen, nominal fest.
- **Mindestreserve**: das Konto darf nie unter die Mindestreserve fallen (Standard
  6 Monatsmieten, unter „Erweitert“).
- **Rückstände**: würde eine fällige Rückzahlung das Konto unter die Reserve drücken,
  wird nur der mögliche Teil gezahlt; der Rest wird so schnell wie möglich nachgezahlt
  und muss innerhalb einer Frist beglichen sein (Standard 3 Jahre, unter „Erweitert“). Bis dahin
  fallen Zinsen an.
- **Überschuss (A4)**: erst wenn kein Rückstand offen ist und das Konto über der Reserve
  alle noch offenen Direkt- und Mitgliederdarlehen decken könnte, fließt der Rest in
  Mietsenkung, Mietrückzahlung oder Solidartransfer.

Die **erforderliche Miete** ist die niedrigste Anfangsmiete, bei der diese Bedingungen in
allen 50 Jahren erfüllt sind, auf 1 Cent genau. Das **bestimmende Jahr** ist das Jahr, in
dem die Rechnung mit etwas weniger Miete scheitern würde: Dort würde das Konto die Reserve
unterschreiten oder ein Rückstand zu lange offen bleiben. Jahre, in denen das Konto genau
auf der Reserve liegt, weil eine Rückzahlung aufgeschoben wird, bestimmen die Miete nicht.
""",
    "method.mode2": """
Grundlage ist die erforderliche Miete aus Modus 1 mit allen Annahmen der Startseite.
Verglichen werden zwei Wege für ein Mitglied, beide inflationsbereinigt:

- **Im Projekt**: Das Mitglied zahlt Einlage und ggf. Mitgliederdarlehen ein und zahlt die
  Projektmiete. Alles, was es gegenüber der Marktmiete spart, sowie Mietrückzahlungen und
  zurückgezahlte Einlage und Darlehen legt es zur Alternativrendite an. Einlage (real) und
  Darlehen (mit Zinseszins) zählen zum Vermögen, solange sie im Projekt stecken.
- **Marktmiete + Geld angelegt**: Einlage und Darlehensbetrag werden stattdessen zur
  Alternativrendite angelegt, und das Mitglied zahlt Marktmiete.
- **Einlage und Darlehen verloren** (gestrichelt): wie „Im Projekt“, aber Einlage und
  Darlehen fallen aus, z. B. bei Insolvenz. Nachrangiges Kapital trägt dieses Risiko.

Mietsenkungen aus dem Überschuss (A4) senken die Projektmiete und erhöhen damit die
Ersparnis. Das einzelne Mitglied wirkt nicht auf die Projektfinanzierung zurück.
""",
    "method.mode3": """
Eure Eigenmittel (Einlagen, Mitgliederdarlehen, Direktkredite, Förderdarlehen) sind fest;
das Bankdarlehen wächst mit dem Haus. Grundstück, Haus und Sanierung werden dabei im
Verhältnis eurer Kostenschätzung hoch- oder heruntergerechnet. Zwei Grenzen bestimmen,
wie teuer das Haus sein darf:

- **Zielmiete**: Je teurer das Haus, desto größer das Bankdarlehen und desto höher die
  erforderliche Miete (Modus 1). Gesucht wird die größte Investition, bei der die
  erforderliche Miete die Zielmiete nicht übersteigt, auf 1.000 € genau.
- **Eigenkapitalanforderung der Bank**: Einlagen, Mitgliederdarlehen und Direktkredite
  müssen mindestens den Mindestanteil der Investition decken, also
  Investition ≤ (Einlagen + Mitgliederdarlehen + Direktkredite) / Mindestanteil.

Die zulässige Investition ist die kleinere der beiden Grenzen.
""",
    "method.uncertainty": """
Viele Annahmen kennt ihr heute nicht genau. Hier gebt ihr für die fünf wichtigsten eine
Spanne an. Der Rechner zieht daraus viele Varianten (Latin-Hypercube-Stichprobe) und sucht
für jede die erforderliche Miete wie in Modus 1, auf 50 Cent genau.

- Innerhalb jeder Spanne ist der Wert von der Startseite am **wahrscheinlichsten**;
  Werte zu den Rändern hin werden seltener (Dreiecksverteilung).
- Die **sichere Miete** ist die Miete, die in 90 % der Varianten reicht.
- Alle übrigen Annahmen kommen unverändert von der Startseite.
- Gleiche Eingaben liefern immer dasselbe Ergebnis (fester Zufallsstartwert).
""",
    # Chart reading guides
    "help.annual_costs": """
Jeder Balken zeigt, wofür das Projekt in einem Jahr Geld ausgibt; die schwarze Linie sind
die Mieteinnahmen nach Mietausfall.

- **Balken über der Linie**: das Projekt zahlt in diesem Jahr aus seinem Konto drauf.
- **Balken unter der Linie**: das Konto wächst.
- Alle Werte sind **inflationsbereinigt** (Kaufkraft von Jahr 1). Eine waagerechte Linie
  heißt also: die Miete steigt genau mit der Inflation. Zins und Tilgung der Bank sind
  nominal fest und werden deshalb real von Jahr zu Jahr kleiner.
- Die hohen Balken in einzelnen Jahren sind **Fälligkeiten** von Direkt- und
  Mitgliederdarlehen. Was dort nicht sofort geht, erscheint in den Folgejahren als
  Nachzahlung.
- Ab dem Jahr, in dem der **Überschuss** fließt, füllt Mietsenkung, Mietrückzahlung oder
  Solidartransfer die Lücke bis zur Linie.

Mit der Maus über einem Jahr seht ihr alle Beträge.
""",
    "help.debt_balances": """
Wie viel das Projekt am Ende jedes Jahres noch schuldet, je Darlehen und als Summe
(gestrichelt), inflationsbereinigt.

- **Bank und Förderung** sinken stetig durch die Tilgung.
- **Direktkredite** bleiben bis zu ihrer Fälligkeit (5 bzw. 10 Jahre) stehen und fallen dann
  auf null. **Mitgliederdarlehen** wachsen bis zur Fälligkeit (Standard 15 Jahre) durch den
  Zinseszins.
- **Rückstände** zeigen, was nach der Fälligkeit noch nachgezahlt werden muss.
""",
    "help.liquidity": """
Kontostand am Jahresende im Vergleich zur Mindestreserve (gestrichelt, Standard 6 Monatsmieten),
inflationsbereinigt.

- Die Miete ist so gewählt, dass das Konto die Reserve **nie unterschreitet**. Berühren
  sich die Linien, wird dort entweder eine Rückzahlung aufgeschoben (Konto genau auf der
  Reserve) oder es ist das bestimmende Jahr.
- Vor Fälligkeiten von Darlehen spart das Konto an, danach fällt es.
- Sobald kein Rückstand offen ist und alle Direkt- und Mitgliederdarlehen gedeckt wären,
  wird der **Überschuss** abgeschöpft; deshalb wächst das Konto dann nicht weiter.
- Gepunktet: die **Instandhaltungsrücklage**, ein eigener Topf, der nicht zur Liquidität
  zählt.
""",
    "help.arrears": """
- **Balken**: wie viel von fälligen Direkt- und Mitgliederdarlehen am Fälligkeitstag nicht
  gezahlt werden konnte, ohne die Mindestreserve zu unterschreiten.
- **Linie**: wie viel davon am Jahresende noch offen ist. Sie muss innerhalb der Frist
  wieder auf null sein; bis dahin zahlt das Projekt Zinsen auf den Rückstand.

Für Darlehensgeber*innen heißt ein Balken: Sie bekommen ihr Geld später als vereinbart.
""",
    "help.investment_curve": """
Wie viel Haus (Gesamtinvestition) bei einer bestimmten Zielmiete pro Person finanzierbar
ist, in heutigen Preisen.

- Die **Linie** steigt, weil eine höhere Miete ein größeres Bankdarlehen trägt.
- **Gestrichelt**: die Obergrenze durch die Eigenkapitalanforderung der Bank; sie hängt
  nicht von der Miete ab.
- Zulässig ist jeweils die **niedrigere** der beiden Linien. Der Punkt markiert eure
  Zielmiete.
""",
    "help.liquidity_mode3": """
Kontostand des Hauses, das bei eurer Zielmiete gerade noch finanzierbar ist, im Vergleich
zur Mindestreserve (gestrichelt), inflationsbereinigt. Berührt die Linie die Reserve, ist
das Haus an der Grenze dessen, was die Zielmiete trägt.
""",
    "help.member_wealth": """
Vermögen des Mitglieds über die Zeit, inflationsbereinigt.

- **Im Projekt** über **Marktmiete + Geld angelegt**: das Projekt lohnt sich finanziell.
  Der Abstand ist der Vorsorgevorteil.
- Am Anfang liegt der Vergleich oft vorn, weil Geld am Markt mehr Rendite bringt als
  Einlage und Darlehen. Die Mietersparnis holt das über die Jahre auf.
- **Gestrichelt**: falls Einlage und Darlehen verloren gingen, z. B. bei einer Insolvenz.
  Liegt auch diese Linie über dem Vergleich, lohnt sich das Projekt selbst dann.
""",
    "help.rent_distribution": """
Jeder Balken zählt, wie viele Varianten eine erforderliche Miete in diesem Bereich haben.

- **Gepunktet**: die Miete aus Modus 1, mit den Werten der Startseite.
- **Durchgezogen**: der Median; die Hälfte der Varianten braucht weniger, die Hälfte mehr.
- **Gestrichelt**: die sichere Miete. Nur 10 % der Varianten brauchen mehr.

Je breiter die Verteilung, desto mehr hängt die Miete von Annahmen ab, die ihr heute nicht
kennt. Ein Abstand zwischen Modus-1-Miete und sicherer Miete ist ein Puffer, den ihr
einplanen könnt.
""",
    "help.headroom_band": """
Wie viel Geld über der Mindestreserve auf dem Konto liegt, wenn ihr die sichere Miete
ansetzt, inflationsbereinigt.

- **Linie**: Median über alle Varianten.
- **Band**: 80 % der Varianten liegen darin (zwischen dem 10. und 90. Perzentil).
- Der Puffer ist in jedem Jahr höchstens so hoch, bis der Überschuss abgeschöpft wird;
  danach liegt er nahe null.

Liegt das untere Bandende unter null, unterschreiten in diesem Jahr einige Varianten die
Reserve. Das sind die 10 %, für die die sichere Miete nicht reicht.
""",
    "help.sensitivity": """
Wie stark jede unsichere Annahme mit der erforderlichen Miete zusammenhängt
(Rangkorrelation, −1 bis +1).

- **Positiv** (blau): ist die Annahme höher, steigt die Miete, z. B. höhere Sanierungskosten.
- **Negativ** (rot): ist die Annahme höher, sinkt die Miete. Bei der Inflation liegt das
  daran, dass die Miete mit der Inflation wächst, Zins und Tilgung aber nicht.
- Je länger der Balken, desto mehr lohnt es sich, diese Annahme genauer zu klären.
""",
    # Mode 1 KPIs
    "kpi.required_rent.label": "Erforderliche Miete",
    "kpi.required_rent.help": (
        "Niedrigste Miete pro Person und Monat, bei der das Konto in allen 50 Jahren "
        "über der Mindestreserve bleibt und jeder Rückstand nach höchstens {years} Jahren "
        "beglichen ist. Danach steigt sie mit der Inflation."
    ),
    "kpi.per_person_month": "pro Person und Monat",
    "kpi.rent_income.label": "Mieteinnahmen Jahr 1",
    "kpi.rent_income.help": "Miete aller Personen im ersten Jahr, vor Mietausfall.",
    "kpi.rent_income.note": "pro Jahr, alle Personen",
    "kpi.investment.label": "Gesamtinvestition",
    "kpi.investment.help": "Grundstück (bei Kauf), Haus, Sanierung und Kaufnebenkosten.",
    "kpi.binding.label": "Bestimmendes Jahr",
    "kpi.binding.help": (
        "Das Jahr, das die erforderliche Miete festlegt: Mit etwas weniger Miete würde "
        "in diesem Jahr die Mindestreserve unterschritten oder ein Rückstand zu lange "
        "offen bleiben. Spätere Belastungen ändern die Miete erst, wenn sie dieses Jahr "
        "ablösen."
    ),
    "kpi.binding.note_reserve": "Jahr {year}, Reserve",
    "kpi.binding.note_arrears": "Jahr {year}, Rückstand zu lange offen",
    "kpi.payoff.label": "Bank und Förderung getilgt",
    "kpi.payoff.help": (
        "Ab dem Folgejahr wird der bisherige Kapitaldienst frei und nach der "
        "gewählten Überschussverwendung genutzt."
    ),
    "kpi.surplus_start.label": "Überschuss fließt ab",
    "kpi.surplus_start.help": (
        "Ab diesem Jahr ist kein Rückstand offen und das Konto deckt Reserve plus "
        "alle offenen Direkt- und Mitgliederdarlehen. Der Rest geht in Mietsenkung, "
        "Mietrückzahlung oder Solidartransfer."
    ),
    "kpi.late.label": "Nicht pünktlich zurückgezahlt",
    "kpi.late.help": (
        "Teil fälliger Direkt- und Mitgliederdarlehen, der am Fälligkeitstag nicht "
        "gezahlt werden konnte (nominal). Er wird innerhalb von {years} Jahren "
        "nachgezahlt; Details in der Grafik unten."
    ),
    "alert.sub_debt_grew": (
        "Direkt- und Mitgliederdarlehen sind nach {years} Jahren real höher als "
        "am Anfang, weil Zinsen auf Mitgliederdarlehen schneller auflaufen, als "
        "zurückgezahlt wird. Diese Schuld geht nicht in die erforderliche Miete ein."
    ),
    # Mode 2 KPIs
    "kpi.project_rent.label": "Projektmiete",
    "kpi.project_rent.help": (
        "Erforderliche Miete aus Modus 1, pro Person und Monat im ersten Jahr."
    ),
    "kpi.from_mode1": "aus Modus 1",
    "kpi.saving.label": "Ersparnis gegenüber Marktmiete",
    "kpi.saving.help": (
        "Marktmiete minus Projektmiete im ersten Jahr nach dem Einzug. Später wächst "
        "die Ersparnis, sobald der Überschuss die Miete senkt."
    ),
    "kpi.saving.note": "pro Monat, erstes Jahr",
    "kpi.advantage.label": "Vorsorgevorteil",
    "kpi.advantage.help": (
        "Vermögen im Projekt minus Vermögen mit Marktmiete und angelegtem Geld, am "
        "Ende, inflationsbereinigt."
    ),
    "kpi.advantage.note": "bis {end}",
    "kpi.wealth_project.label": "Vermögen im Projekt",
    "kpi.wealth_project.help": (
        "Angelegte Ersparnisse und Rückzahlungen plus Einlage und Darlehen, solange "
        "sie im Projekt stecken; inflationsbereinigt."
    ),
    "kpi.wealth_market.label": "Vermögen mit Marktmiete",
    "kpi.wealth_market.help": (
        "Einlage und Darlehensbetrag zur Alternativrendite angelegt, Marktmiete "
        "gezahlt; inflationsbereinigt."
    ),
    "kpi.default.label": "Bei Ausfall von Einlage und Darlehen",
    "kpi.default.help": (
        "Vorsorgevorteil, falls Einlage und Darlehen komplett verloren gingen, z. B. "
        "bei einer Insolvenz des Projekts."
    ),
    "kpi.default.note": "Vorteil gegenüber Marktmiete",
    # Mode 3 KPIs
    "kpi.admissible.label": "Zulässige Investition",
    "kpi.admissible.help": (
        "Die kleinere der beiden Grenzen: was die Zielmiete trägt und was die "
        "Eigenkapitalanforderung der Bank zulässt."
    ),
    "kpi.admissible.by_rent": "begrenzt durch Zielmiete",
    "kpi.admissible.by_equity": "begrenzt durch Eigenkapital",
    "kpi.share.label": "Anteil eurer Kostenschätzung",
    "kpi.share.help": (
        "Zulässige Investition geteilt durch eure Kostenschätzung (Grundstück, Haus, "
        "Sanierung und Nebenkosten von der Startseite). Ab 100 % ist das Haus "
        "finanzierbar."
    ),
    "kpi.share.note": "Schätzung {estimate}",
    "kpi.rent_limit.label": "Grenze durch Zielmiete",
    "kpi.rent_limit.help": (
        "Größte Investition, bei der die erforderliche Miete die Zielmiete nicht übersteigt."
    ),
    "kpi.bank_limit.label": "Grenze durch Eigenkapital",
    "kpi.bank_limit.help": (
        "(Einlagen + Mitgliederdarlehen + Direktkredite) / Mindestanteil, den die Bank verlangt."
    ),
    "kpi.bank_limit.none": "keine",
    # Uncertainty page
    "unc.ranges": "Spannen",
    "unc.compute": "Berechnen",
    "unc.hint": "*Wahrscheinlichster Wert jeweils von der Startseite.*",
    "unc.prompt": "Spannen einstellen und auf „Berechnen“ klicken.",
    "unc.stale": (
        "Annahmen wurden geändert. Die Ergebnisse unten sind veraltet; bitte neu berechnen."
    ),
    "kpi.base.label": "Miete ohne Unsicherheit",
    "kpi.base.help": "Erforderliche Miete aus Modus 1, mit den Werten der Startseite.",
    "kpi.median.label": "Median",
    "kpi.median.help": "Die Hälfte der Varianten braucht weniger, die Hälfte mehr.",
    "kpi.spread.label": "Spanne 10–90 %",
    "kpi.spread.help": "80 % der Varianten brauchen eine Miete in diesem Bereich.",
    "kpi.safe.label": "Sichere Miete",
    "kpi.safe.help": (
        "Reicht in 90 % der Varianten. Der Abstand zur Miete ohne Unsicherheit ist "
        "ein Puffer für ungünstige Entwicklungen."
    ),
    "kpi.safe.note": "{amount} über Modus 1",
    "kpi.failed.label": "Varianten ohne Lösung",
    "kpi.failed.help": (
        "In diesen Varianten reicht keine Miete bis 5.000 € pro Person; sie fehlen "
        "in der Auswertung."
    ),
    # Methodology page
    "methodik.inputs_heading": "## Eingaben und Standardwerte",
    "methodik.table_header": "| Bereich | Eingabe | Standard | Bedeutung |",
    # Charts
    "chart.real_subtitle": "inflationsbereinigt, in Kaufkraft von {year} (Jahr 1)",
    "chart.tranche.equity": "Einlagen",
    "chart.tranche.member_loan": "Mitgliederdarlehen",
    "chart.tranche.direct_loan": "Direktkredite",
    "chart.tranche.subsidy_loan": "Förderdarlehen",
    "chart.tranche.bank_loan": "Bankdarlehen",
    "chart.tranche.direct_loans_5y": "Direktkredite 5 Jahre",
    "chart.tranche.direct_loans_10y": "Direktkredite 10 Jahre",
    "chart.costs.title": "Jährliche Ausgaben und Mieteinnahmen",
    "chart.costs.y": "pro Jahr",
    "chart.costs.operating": "Betrieb inkl. Instandhaltungsrücklage",
    "chart.costs.senior_interest": "Zinsen Bank und Förderung",
    "chart.costs.senior_repayment": "Tilgung Bank und Förderung",
    "chart.costs.direct_interest": "Zinsen Direktkredite",
    "chart.costs.member_interest": "Zinsen Mitgliederdarlehen (bei Rückzahlung)",
    "chart.costs.sub_repayment": "Rückzahlung Direkt- und Mitgliederdarlehen (pünktlich)",
    "chart.costs.arrears": "Nachzahlung Rückstände inkl. Zinsen",
    "chart.costs.rebate": "Mietsenkung aus Überschuss",
    "chart.costs.payout": "Mietrückzahlung",
    "chart.costs.transfer": "Solidartransfer",
    "chart.costs.rent_income": "Mieteinnahmen",
    "chart.arrears.title": "Nicht pünktlich zurückgezahlte Direkt- und Mitgliederdarlehen",
    "chart.arrears.new": "Am Fälligkeitstag nicht zurückgezahlt",
    "chart.arrears.open": "Offener Rückstand zum Jahresende",
    "chart.debt.title": "Restschuld zum Jahresende",
    "chart.debt.arrears": "Rückstände",
    "chart.debt.total": "Summe",
    "chart.liquidity.title": "Liquidität und Rücklage",
    "chart.liquidity.liquidity": "Liquidität",
    "chart.liquidity.reserve": "Mindestreserve",
    "chart.liquidity.maintenance": "Instandhaltungsrücklage (eigener Topf)",
    "chart.member.title": "Vermögen des Mitglieds",
    "chart.member.project": "Im Projekt",
    "chart.member.market": "Marktmiete + Geld angelegt",
    "chart.member.default": "Im Projekt, Einlage und Darlehen verloren",
    "chart.curve.title": "Zulässige Investition je nach Zielmiete",
    "chart.curve.subtitle": "Preise von heute",
    "chart.curve.rent_limit": "Grenze durch Zielmiete",
    "chart.curve.bank_limit": "Grenze durch Eigenkapitalanforderung",
    "chart.curve.point": "Zulässig bei Zielmiete",
    "chart.curve.x": "Zielmiete (€ pro Person/Monat)",
    "chart.curve.hover_rent": "Zielmiete",
    "chart.curve.hover_investment": "Investition",
    "chart.uncertain.inflation": "Inflation",
    "chart.uncertain.bank_rate_change_pp": "Bankzins nach 10 Jahren",
    "chart.uncertain.vacancy_rate": "Mietausfall",
    "chart.uncertain.renovation_factor": "Sanierungskosten",
    "chart.uncertain.running_cost_factor": "Verwaltung und Versicherung",
    "chart.dist.title": "Erforderliche Miete über alle Varianten",
    "chart.dist.count": "Anzahl Varianten",
    "chart.dist.base": "Ohne Unsicherheit",
    "chart.dist.median": "Median",
    "chart.dist.safe": "Sichere Miete (reicht in 90 %)",
    "chart.dist.x": "Erforderliche Miete (€ pro Person/Monat)",
    "chart.dist.hover_variants": "Varianten",
    "chart.band.title": "Puffer über der Mindestreserve bei sicherer Miete",
    "chart.band.p90": "90. Perzentil",
    "chart.band.band": "10–90 %-Band",
    "chart.band.median": "Median",
    "chart.band.reserve": "Mindestreserve",
    "chart.sens.title": "Was treibt die Unsicherheit?",
    "chart.sens.y": "Rangkorrelation mit der Miete",
    "chart.sens.name": "Zusammenhang",
    # Additional uncertain inputs
    "label.member_loan_term_range": "Laufzeit Mitgliederdarlehen (Jahre)",
    "label.member_loan_range": "Mitgliederdarlehen (% der Planung)",
    "label.direct_loans_10y_range": "Direktkredite 10 J. (% der Planung)",
    "info.member_loan_term_range": (
        "Spanne der Laufzeit der Mitgliederdarlehen in ganzen Jahren. Wahrscheinlichster "
        "Wert: Startseite (unter „Erweitert“)."
    ),
    "info.member_loan_range": (
        "Wie viel Mitgliederdarlehen tatsächlich zusammenkommen, in % des geplanten Betrags. "
        "Fehlt Geld, springt das Bankdarlehen ein. Wahrscheinlichster Wert: 100 %."
    ),
    "info.direct_loans_10y_range": (
        "Wie viel 10-Jahres-Direktkredite tatsächlich eingeworben werden, in % des geplanten "
        "Betrags. Fehlt Geld, springt das Bankdarlehen ein. Wahrscheinlichster Wert: 100 %."
    ),
    "chart.uncertain.member_loan_term_years": "Laufzeit Mitgliederdarlehen",
    "chart.uncertain.member_loan_factor": "Umfang Mitgliederdarlehen",
    "chart.uncertain.direct_loans_10y_factor": "Umfang Direktkredite 10 Jahre",
    # Rates relative to inflation, member loan payoff, nominal display
    "label.member_loan_spread_pp": "Zins Mitgliederdarlehen (Pp. über Inflation)",
    "label.direct_loan_spread_5y_pp": "Zins 5 Jahre (Pp. über Inflation)",
    "label.direct_loan_spread_10y_pp": "Zins 10 Jahre (Pp. über Inflation)",
    "label.bank_spread_pp": "Bankzins (Pp. über Inflation)",
    "label.subsidy_spread_pp": "Zins Förderdarlehen (Pp. über Inflation)",
    "label.alt_return_spread_pp": "Alternativrendite (Pp. über Inflation)",
    "info.member_loan_spread_pp": (
        "Zins auf Mitgliederdarlehen in Prozentpunkten über der Inflation; er wird dem "
        "Darlehen gutgeschrieben. Beispiel: 3 bei 2 % Inflation ergibt 5 % Zins."
    ),
    "info.direct_loan_spread_5y_pp": (
        "Zins auf 5-Jahres-Direktkredite in Prozentpunkten über der Inflation, jährlich "
        "ausgezahlt. Negative Werte heißen: Zins unter der Inflation."
    ),
    "info.direct_loan_spread_10y_pp": (
        "Zins auf 10-Jahres-Direktkredite in Prozentpunkten über der Inflation, jährlich "
        "ausgezahlt."
    ),
    "info.bank_spread_pp": (
        "Sollzins des Bankdarlehens für die ersten 10 Jahre, in Prozentpunkten über der "
        "Inflation. Er hängt vom Marktzins ab, nicht direkt von der Inflation: oft lag er"
        " 1 bis 3 Prozentpunkte darüber, 2015 bis 2021 aber nahe an oder unter der "
        "Inflation. Der Zins steht bei Abschluss fest und ändert sich danach nicht mit "
        "der Inflation."
    ),
    "info.subsidy_spread_pp": (
        "Zins der Förderdarlehen in Prozentpunkten über der Inflation, fest über die "
        "ganze Laufzeit. Förderzinsen liegen oft unter der Inflation (negativer Wert)."
    ),
    "info.alt_return_spread_pp": (
        "Rendite pro Jahr in Prozentpunkten über der Inflation, wenn das Geld statt im "
        "Projekt anderswo angelegt würde (z. B. breit gestreuter Fonds). Mit derselben "
        "Rendite werden auch alle Ersparnisse des Mitglieds angelegt."
    ),
    "info.inflation_pct": (
        "Jährliche Inflation. Miete, Betriebskosten und Erbbauzins steigen damit. Alle "
        "Zinsen werden relativ zur Inflation eingegeben und ändern sich mit ihr; ist ein "
        "Darlehen abgeschlossen, bleiben Zins und Tilgung nominal fest. Deshalb ist meist"
        " das erste Jahr am engsten."
    ),
    "summary.rates": (
        "Nominal bei {inflation} Inflation: Bank {bank} (nach 10 J. {follow_up}), "
        "Förderung {subsidy}, Direktkredite {dk5} / {dk10}, Mitgliederdarlehen {member}"
    ),
    "label.member_loan_payoff": "Rückzahlung der Mitgliederdarlehen",
    "info.member_loan_payoff": (
        "Woher das Geld kommt, wenn die Mitgliederdarlehen samt Zinsen fällig werden. Aus"
        " Liquidität: das Konto zahlt, was ohne Unterschreiten der Reserve geht, der Rest"
        " wird als Rückstand nachgezahlt. Neues Bankdarlehen: die ganze Summe wird zum "
        "Anschlusszins der Bank finanziert, als Annuität bzw. Ratenkredit über die "
        "Restlaufzeit des Bankdarlehens, mindestens 10 Jahre. Neue Direktkredite: die "
        "ganze Summe wird mit 10-Jahres-Direktkrediten zum 10-Jahres-Zins finanziert, die"
        " nach 10 Jahren fällig werden."
    ),
    "option.member_loan_payoff.liquidity": "Aus Liquidität",
    "option.member_loan_payoff.bank": "Neues Bankdarlehen",
    "option.member_loan_payoff.direct_loans": "Neue Direktkredite 10 J.",
    "label.display": "Grafiken",
    "info.display": (
        "Inflationsbereinigt: alle Beträge in Kaufkraft von Jahr 1, so lassen sich Jahre "
        "direkt vergleichen. Nominal: die tatsächlichen Euro-Beträge des jeweiligen "
        "Jahres; Miete und Kosten wachsen dann sichtbar mit der Inflation."
    ),
    "option.display.real": "inflationsbereinigt",
    "option.display.nominal": "nominal",
    "chart.nominal_subtitle": "nominal, tatsächliche Euro-Beträge des jeweiligen Jahres",
    "help.nominal_note": (
        "*Die Grafik zeigt gerade nominale Beträge; die Erklärung unten bezieht sich auf "
        "die inflationsbereinigte Darstellung.*\n"
    ),
    "chart.tranche.bank_refinance": "Bankdarlehen für Mitgliederdarlehen",
    "chart.tranche.direct_loans_refinance": "Direktkredite für Mitgliederdarlehen",
    "chart.costs.refinancing": "Neues Darlehen für Mitgliederdarlehen (Zufluss)",
    # Direct loan rollover
    "label.direct_loan_rollover_pct": "Ersatz bei Fälligkeit (10 J.)",
    "info.direct_loan_rollover_pct": (
        "Welcher Anteil der 10-Jahres-Direktkredite alle 10 Jahre durch neue Direktkredite "
        "ersetzt wird; nur der Rest wird aus dem Konto zurückgezahlt. 0 % heißt: alles wird "
        "getilgt. Gilt auch für Direktkredite, die die Mitgliederdarlehen ablösen. 5-Jahres-"
        "Direktkredite werden immer getilgt."
    ),
    "option.direct_loan_rollover_pct.0": "0 %",
    "option.direct_loan_rollover_pct.25": "25 %",
    "option.direct_loan_rollover_pct.50": "50 %",
    "option.direct_loan_rollover_pct.75": "75 %",
    "option.direct_loan_rollover_pct.100": "100 %",
}
