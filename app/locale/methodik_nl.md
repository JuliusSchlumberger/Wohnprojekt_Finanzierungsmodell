# Methodiek

De calculator rekent een gezamenlijk woonproject door over 50 jaar in stappen van een jaar.
Alle bedragen worden nominaal berekend; de grafieken tonen ze naar keuze gecorrigeerd voor
inflatie, in koopkracht van jaar 1, of nominaal. Alle rentetarieven worden ingevoerd als
opslag boven de inflatie in procentpunten; de nominale rente is inflatie plus opslag,
minimaal 0 %.

## Financiering bij de start

- **Totale investering** = huis + grond (alleen bij koop) + kosten koper op beide
  + renovatie.
- **Eigen middelen**: inleg (Einlagen) en ledenleningen (Mitgliederdarlehen), elk per
  persoon; directe leningen (Direktkredite) met een looptijd van 5 en 10 jaar;
  subsidieleningen (Förderdarlehen, hoogstens zo hoog als de renovatiekosten).
- **Banklening** sluit het gat naar de totale investering plus startliquiditeit. De
  startliquiditeit is de minimale reserve van het eerste jaar en wordt meegefinancierd.
- **Eigenvermogenstoets**: inleg, ledenleningen en directe leningen samen ten opzichte van
  de totale investering, vergeleken met het minimumdeel dat de bank eist.

## Elk jaar

**nieuw saldo = oud saldo + huurinkomsten − exploitatiekosten − rente − aflossing**,
plus terugbetalingen van vervallen directe en ledenleningen en de besteding van het
overschot.

- **Huurinkomsten**: huur per persoon × personen × 12, min huurderving (in de eerste drie
  jaar een eigen, meestal hoger percentage). De huur stijgt met de inflatie.
- **Exploitatiekosten**: storting in de onderhoudsreserve, beheer, verzekering en bij
  erfpacht (Erbbaurecht) de erfpachtcanon (Erbbauzins); alle stijgen met de inflatie. Het
  werkelijke onderhoud wordt uit de reserve betaald, een aparte pot buiten de rekening.
- **Bank**: annuïteit of lineaire aflossing over de gekozen looptijd; na de rentevaste
  periode van 10 jaar geldt de nieuwe rente.
- **Subsidielening**: annuïteit met vaste rente.
- **Directe leningen**: jaarlijks rente, terugbetaling aan het einde van de looptijd (5 of
  10 jaar).
- **Ledenleningen**: de rente wordt bijgeschreven (samengestelde rente), terugbetaling
  inclusief rente aan het einde van de looptijd (standaard 15 jaar, instelbaar onder
  „Uitgebreid”). De terugbetaling komt naar keuze van de rekening (met achterstanden, zie
  hieronder), uit een nieuwe banklening tegen de vervolgrente (looptijd: rest van de
  banklooptijd, minimaal 10 jaar) of uit nieuwe directe leningen van 10 jaar tegen de rente
  van de 10-jaarsleningen. De nieuwe lening dekt het volledige verschuldigde bedrag inclusief
  rente en wordt vanaf het volgende jaar bediend.
- **Achterstanden**: als een vervallen terugbetaling de rekening onder de minimale reserve
  zou drukken, wordt alleen het mogelijke deel betaald. De rest wordt zo snel mogelijk
  nabetaald, oudste eerst, draagt tot dan rente en moet binnen de ingestelde termijn zijn
  voldaan. Behalve de gekozen herfinanciering van de ledenleningen worden geen nieuwe
  leningen opgenomen.
- **Overschot**: als er geen achterstand openstaat en de rekening boven de reserve alle nog
  openstaande directe en ledenleningen dekt, wordt de rest afgeroomd: als huurverlaging, als
  huurteruggave elke 15 jaar of als solidariteitsoverdracht (Solidartransfer). Na aflossing
  van bank en subsidie worden de vrijgekomen lasten op dezelfde manier besteed.

## Wat wordt gezocht

- **Modus 1, benodigde huur**: de laagste aanvangshuur waarbij de rekening in alle 50 jaar
  boven de minimale reserve blijft en elke achterstand op tijd is voldaan. Gevonden door
  intervalhalvering tot op de cent.
- **Modus 2, leden**: vermogen van een lid in het project (belegde huurbesparing,
  terugbetalingen, inleg reëel, lening met samengestelde rente) vergeleken met markthuur en
  belegd kapitaal, beide tegen hetzelfde alternatieve rendement en gecorrigeerd voor
  inflatie.
- **Modus 3, doelhuur**: de grootste totale investering die een doelhuur kan dragen,
  begrensd door de eigenvermogenseis van de bank. Grond, huis en renovatie worden daarvoor
  naar verhouding van de kostenschatting geschaald.
- **Onzekerheid**: voor acht invoerwaarden met een bandbreedte worden varianten getrokken
  (Latin hypercube, driehoeksverdeling met de huidige waarde als meest waarschijnlijke) en
  wordt per variant de benodigde huur gezocht, tot op 50 cent. De rentetarieven bewegen mee
  met de getrokken inflatie en houden hun opslag.

## Grenzen van het model

- **Belastingen** zijn niet gemodelleerd.
- **Eén type lid**: inleg en ledenlening zijn per persoon voor iedereen gelijk; modus 2
  bekijkt één lid dat geen invloed heeft op de projectfinanciering.
- **Vaste soorten leningen**: directe leningen van 5 en 10 jaar, ledenleningen met
  instelbare looptijd, één banklening en één subsidielening. Leningen worden niet vervroegd
  opgezegd en na de vervaldatum wordt geen vervanging opgenomen, behalve de optionele
  herfinanciering van de ledenleningen.
- **Verwachtingswaarden**: behalve op de onzekerheidspagina wordt met vaste waarden
  gerekend; leegstand, renteveranderingen en inflatie zijn aannames, geen voorspellingen.
- **Rechtsvorm** wordt niet onderscheiden; het effect ervan (bijv. hogere beheerkosten bij
  een coöperatie) kan via de invoer worden weergegeven.
- **Aannames zonder bron**: de standaardwaarden zijn plausibele startpunten voor een
  voorbeeldgroep, geen onderzochte marktwaarden. Vervang ze door eigen offertes en
  berekeningen.
- **Duitse context**: begrippen en standaardwaarden (bijv. erfpacht, KfW,
  overdrachtsbelasting) volgen de Duitse praktijk.

Deze calculator is een planningsinstrument en geen financieel, fiscaal of juridisch advies.
