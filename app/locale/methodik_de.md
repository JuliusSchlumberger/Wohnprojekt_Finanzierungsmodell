# Methodik

Der Rechner bildet ein gemeinsames Wohnprojekt über 50 Jahre in Jahresschritten ab. Alle
Beträge werden nominal gerechnet; die Grafiken zeigen sie wahlweise inflationsbereinigt in
Kaufkraft von Jahr 1 oder nominal. Alle Zinssätze werden als Abstand zur Inflation in
Prozentpunkten eingegeben; der Nominalzins ist Inflation plus Abstand, mindestens 0 %.

## Finanzierung zu Beginn

- **Gesamtinvestition** = Haus + Grundstück (nur bei Kauf) + Kaufnebenkosten auf beides
  + Sanierung.
- **Eigenmittel**: Einlagen und Mitgliederdarlehen (je pro Person), Direktkredite mit 5 und
  10 Jahren Laufzeit, Förderdarlehen (höchstens so hoch wie die Sanierungskosten).
- **Bankdarlehen** schließt die Lücke zur Gesamtinvestition plus Startliquidität. Die
  Startliquidität ist die Mindestreserve des ersten Jahres und wird mitfinanziert.
- **Eigenkapitalprüfung**: Einlagen, Mitgliederdarlehen und Direktkredite zusammen im
  Verhältnis zur Gesamtinvestition, verglichen mit dem Mindestanteil, den die Bank verlangt.

## Jedes Jahr

**Konto neu = Konto alt + Mieteinnahmen − Betriebskosten − Zinsen − Tilgung**,
dazu Rückzahlungen fälliger Direkt- und Mitgliederdarlehen und die Verwendung des
Überschusses.

- **Mieteinnahmen**: Miete pro Person × Personen × 12, abzüglich Mietausfall (in den ersten
  drei Jahren ein eigener, meist höherer Satz). Die Miete steigt mit der Inflation.
- **Betriebskosten**: Zuführung zur Instandhaltungsrücklage, Verwaltung, Versicherung und
  bei Erbbaurecht der Erbbauzins; alle steigen mit der Inflation. Die Zuführung ist ein
  fester Anteil des Wiederherstellungswerts (60 % von Haus plus Sanierung, ohne Grundstück)
  und wird im selben Jahr für Instandhaltung ausgegeben.
- **Bank**: Annuität oder Ratenkredit über die gewählte Laufzeit; nach 10 Jahren
  Zinsbindung gilt der Anschlusszins.
- **Förderdarlehen**: Annuität mit festem Zins.
- **Direktkredite**: Zinsen jährlich, Rückzahlung am Ende der Laufzeit (5 oder 10 Jahre).
  Bei den 10-Jahres-Direktkrediten wird bei jeder Fälligkeit der eingestellte Anteil
  (Standard 50 %) durch neue Direktkredite ersetzt; nur der Rest wird zurückgezahlt.
- **Mitgliederdarlehen**: Zinsen werden gutgeschrieben (Zinseszins), Rückzahlung samt
  Zinsen am Ende der Laufzeit (Standard 15 Jahre, einstellbar unter „Erweitert“). Die
  Rückzahlung kommt wahlweise aus dem Konto (mit Rückständen, s. u.), aus einem neuen
  Bankdarlehen zum Anschlusszins (Laufzeit: Rest der Banklaufzeit, mindestens 10 Jahre)
  oder aus neuen Direktkrediten mit 10 Jahren zum Zins der 10-Jahres-Direktkredite. Das
  neue Darlehen deckt den vollen fälligen Betrag samt Zinsen und wird ab dem Folgejahr
  bedient.
- **Rückstände**: Würde eine fällige Rückzahlung das Konto unter die Mindestreserve drücken,
  wird nur der mögliche Teil gezahlt. Der Rest wird so schnell wie möglich nachgezahlt,
  älteste zuerst, verzinst sich bis dahin und muss innerhalb der eingestellten Frist
  beglichen sein. Außer der gewählten Ablösung der Mitgliederdarlehen werden keine neuen
  Darlehen aufgenommen.
- **Überschuss**: Ist kein Rückstand offen und deckt das Konto über der Reserve alle noch
  offenen Direkt- und Mitgliederdarlehen, wird der Rest abgeschöpft: als Mietsenkung, als
  Mietrückzahlung alle 15 Jahre oder als Solidartransfer. Nach Tilgung von Bank und Förderung
  wird außerdem deren frei gewordener Kapitaldienst so verwendet.

## Was gesucht wird

- **Modus 1, erforderliche Miete**: die niedrigste Anfangsmiete, bei der das Konto in allen
  50 Jahren über der Mindestreserve bleibt und jeder Rückstand fristgerecht beglichen ist.
  Gesucht durch Intervallhalbierung auf 1 Cent genau.
- **Modus 2, Vorsorge**: Vermögen eines Mitglieds im Projekt (angelegte Mietersparnis,
  Rückzahlungen, Einlage real, Darlehen mit Zinseszins) gegenüber Marktmiete mit
  angelegtem Kapital, beide zur selben Alternativrendite und inflationsbereinigt.
- **Modus 3, Zielmiete**: die größte Gesamtinvestition, die eine Zielmiete trägt, begrenzt
  durch die Eigenkapitalanforderung der Bank. Grundstück, Haus und Sanierung werden dafür
  im Verhältnis der Kostenschätzung skaliert.
- **Unsicherheit**: Für acht Eingaben mit Spanne werden Varianten gezogen
  (Latin-Hypercube, Dreiecksverteilung mit dem aktuellen Wert als wahrscheinlichstem) und je
  die erforderliche Miete gesucht, auf 50 Cent genau. Die Zinssätze bewegen sich mit der
  gezogenen Inflation, ihr Abstand zur Inflation bleibt gleich.

## Grenzen des Modells

- **Steuern** sind nicht abgebildet.
- **Ein Mitgliedertyp**: Einlage und Mitgliederdarlehen gelten pro Person für alle gleich;
  Modus 2 betrachtet ein einzelnes Mitglied, das nicht auf die Projektfinanzierung
  zurückwirkt.
- **Feste Darlehensarten**: Direktkredite mit 5 und 10 Jahren, Mitgliederdarlehen mit
  einstellbarer Laufzeit, ein Bank- und ein Förderdarlehen. Darlehen werden nicht vorzeitig gekündigt,
  und nach Fälligkeit wird kein Ersatz aufgenommen, außer der wählbaren Ablösung der
  Mitgliederdarlehen und dem Neueinwerben der 10-Jahres-Direktkredite.
- **Erwartungswerte**: Abgesehen von der Unsicherheitsseite wird mit festen Werten
  gerechnet; Leerstand, Zinsänderungen und Inflation sind Annahmen, keine Prognosen.
- **Rechtsform** wird nicht unterschieden; ihre Wirkung (z. B. höhere Verwaltungskosten in
  einer eG) lässt sich über die Eingaben abbilden.
- **Annahmen ohne Quelle**: Die Standardwerte sind plausible Startpunkte für eine
  Beispielgruppe, keine recherchierten Marktwerte. Bitte durch eigene Angebote und
  Kalkulationen ersetzen.

Dieser Rechner ist ein Planungswerkzeug und keine Finanz-, Steuer- oder Rechtsberatung.
