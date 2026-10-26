"""Dutch UI texts; German legal and financing terms are given in brackets on first use."""

TEXTS = {
    # App frame and navigation
    "app.title": "Woonproject-calculator",
    "app.language": "Taal",
    "nav.start": "Start",
    "nav.mode1": "Modus 1: Huur",
    "nav.mode2": "Modus 2: Leden",
    "nav.mode3": "Modus 3: Doelhuur",
    "nav.uncertainty": "Onzekerheid",
    "nav.methodik": "Methodiek",
    # Start page
    "start.intro": """
Met deze calculator kan een woonprojectgroep doorrekenen hoe een samen gekocht huis, of een
huis in erfpacht (Erbbaurecht), gefinancierd kan worden. Hier stellen jullie alle aannames
in; de belangrijkste kunnen ook direct op de modus-pagina's worden aangepast. Elke wijziging
geldt meteen op alle pagina's. Het **?** naast een veld of kengetal legt uit wat erachter
zit.
""",
    "start.mode1.question": "Welke huur per persoon heeft ons huis minstens nodig?",
    "start.mode2.question": "Loont het project voor een lid vergeleken met markthuur?",
    "start.mode3.question": "Hoeveel huis kan onze groep zich bij een doelhuur veroorloven?",
    "start.heading": "Aannames instellen",
    "start.disclaimer": (
        "**Disclaimer:** Deze calculator is een planningsinstrument en geen financieel, "
        "fiscaal of juridisch advies. Alle uitkomsten hangen af van de aannames."
    ),
    "start.advanced": "Uitgebreid: exploitatie, reserve, kosten koper, subsidievoorwaarden",
    # Assumptions A1-A9
    "assumptions.title": "Aannames van het model (A1–A9)",
    "assumptions.header": "| Nr. | Aanname | Vastlegging |",
    "assumption.1.title": "Eigendomsmodel",
    "assumption.1.text": (
        "Een gezamenlijke rechtspersoon (coöperatie/eG, GmbH, GmbH & Co. KG) koopt het huis of "
        "gebruikt het in erfpacht (Erbbaurecht). Leden betalen een gebruiksvergoeding "
        "(„huur”). Geen individueel eigendom."
    ),
    "assumption.2.title": "Huureenheid",
    "assumption.2.text": (
        "Huur per persoon per maand, voor iedereen gelijk. Gemeenschappelijke ruimtes zijn "
        "inbegrepen."
    ),
    "assumption.3.title": "Kapitaalinbreng",
    "assumption.3.text": "Personen brengen verschillende bedragen in (ledentypes).",
    "assumption.4.title": "Vrijkomend geld",
    "assumption.4.text": (
        "Nadat bank- en subsidieleningen zijn afgelost en alle directe en ledenleningen "
        "gedekt zijn: huurverlaging, huurteruggave elke 15 jaar of een "
        "solidariteitsoverdracht aan een volgend project."
    ),
    "assumption.5.title": "Inleg",
    "assumption.5.text": (
        "Bij vertrek geïndexeerd terugbetaald; nieuwe leden kopen zich in tegen dezelfde "
        "waarde. Het bedrag in het project blijft constant."
    ),
    "assumption.6.title": "Looptijd en inflatie",
    "assumption.6.text": (
        "50 jaar. Huur, exploitatiekosten en erfpachtcanon stijgen met de inflatie; rente en "
        "aflossing liggen nominaal vast."
    ),
    "assumption.7.title": "Minimale liquiditeit",
    "assumption.7.text": (
        "De rekening komt nooit onder de minimale reserve (standaard 6 maandhuren)."
    ),
    "assumption.8.title": "Belastingen",
    "assumption.8.text": "Niet gemodelleerd.",
    "assumption.9.title": "Directe en ledenleningen",
    "assumption.9.text": (
        "Achtergesteld en ineens aflosbaar. Directe leningen (Direktkredite) lopen 5 of "
        "10 jaar met jaarlijkse rente; ledenleningen (Mitgliederdarlehen) hebben een "
        "instelbare looptijd (standaard 15 jaar) met bijgeschreven rente. Wat op de "
        "vervaldag niet kan worden terugbetaald zonder onder de minimale reserve te komen, "
        "wordt zo snel mogelijk nabetaald, binnen een termijn (standaard 3 jaar), en draagt "
        "tot dan rente."
    ),
    # Input sections
    "section.house": "Huis en kosten",
    "section.group": "Groep en exploitatie",
    "section.own_funds": "Eigen middelen",
    "section.direct_loans": "Directe leningen",
    "section.bank": "Bank en subsidie",
    "section.surplus": "Overschot en doelhuur",
    "section.member_capital": "Lid: kapitaal (modus 2)",
    "section.member_compare": "Lid: vergelijking (modus 2)",
    "section.adv_operations": "Exploitatie",
    "section.adv_liquidity": "Liquiditeit en achterstanden",
    "section.adv_purchase": "Aankoop en erfpacht",
    "section.adv_subsidy": "Subsidieleningen",
    "section.adv_member_loans": "Ledenleningen",
    # Input labels
    "label.land_price": "Grond (€)",
    "label.building_price": "Huis (€)",
    "label.renovation_cost": "Renovatie (€)",
    "label.tenure": "Grond",
    "label.persons": "Aantal personen",
    "label.equity_per_person": "Inleg per persoon (€)",
    "label.member_loan_per_person": "Ledenlening per persoon (€)",
    "label.direct_loans_5y": "Directe leningen 5 jaar (€)",
    "label.direct_loans_10y": "Directe leningen 10 jaar (€)",
    "label.subsidy": "Subsidielening (€)",
    "label.bank_repayment": "Aflossingsvorm bank",
    "label.bank_term_years": "Looptijd bank (jaar)",
    "label.bank_rate_change": "Bankrente na 10 jaar",
    "label.inflation_pct": "Inflatie (%)",
    "label.surplus_use": "Na aflossing van bank- en subsidieleningen",
    "label.min_equity_like_pct": "Minimaal eigen verm. + achtergesteld (%)",
    "label.target_rent": "Doelhuur per persoon (€/maand)",
    "label.maintenance_reserve_pct": "Onderhoudsreserve (%)",
    "label.vacancy_pct": "Huurderving (%)",
    "label.initial_vacancy_pct": "Huurderving eerste 3 jaar (%)",
    "label.admin_cost_per_year": "Beheer per jaar (€)",
    "label.insurance_per_year": "Verzekering per jaar (€)",
    "label.min_liquidity_months": "Minimale reserve (maandhuren)",
    "label.max_arrears_years": "Achterstand hoogstens (jaar)",
    "label.ancillary_cost_pct": "Kosten koper (%)",
    "label.leasehold_rate_pct": "Erfpachtcanon (%)",
    "label.subsidy_term_years": "Looptijd subsidieleningen (jaar)",
    "label.member_loan_term_years": "Looptijd ledenleningen (jaar)",
    "label.member_type": "Type lid",
    "label.member_equity": "Inleg (€)",
    "label.member_loan_personal": "Ledenlening (€)",
    "label.entry_year": "Intrek (jaar)",
    "label.exit_year": "Vertrek (jaar)",
    "label.market_rent": "Markthuur per persoon (€/maand)",
    "label.inflation_range": "Inflatie (%)",
    "label.bank_change_range": "Bankrente na 10 jr. (± %-punt)",
    "label.vacancy_range": "Huurderving (%)",
    "label.renovation_range": "Renovatie (% van schatting)",
    "label.running_range": "Beheer, verzekering (%)",
    "label.n_samples": "Aantal varianten",
    # Options of choice inputs
    "option.tenure.purchase": "Koop",
    "option.tenure.leasehold": "Erfpacht",
    "option.bank_repayment.annuity": "Annuïteit",
    "option.bank_repayment.linear": "Lineair",
    "option.bank_rate_change.down": "daalt",
    "option.bank_rate_change.same": "gelijk",
    "option.bank_rate_change.up": "stijgt",
    "option.surplus_use.rent_reduction": "Huurverlaging",
    "option.surplus_use.payout_15y": "Huurteruggave elke 15 jaar",
    "option.surplus_use.next_project": "Solidariteitsoverdracht",
    "option.member_type.custom": "Eigen waarden",
    "option.member_type.low": "Weinig kapitaal",
    "option.member_type.mid": "Gemiddeld",
    "option.member_type.high": "Veel",
    # Input explanations
    "info.land_price": (
        "Koopprijs van de grond. Bij erfpacht (Erbbaurecht) wordt die niet gekocht; het "
        "bedrag geldt dan als grondwaarde waarover de erfpachtcanon (tarief onder "
        "„Uitgebreid”) wordt berekend."
    ),
    "info.building_price": "Koopprijs van het huis zonder grond.",
    "info.renovation_cost": (
        "Kosten van renovatie en verbouwing. Alleen hiervoor kunnen subsidieleningen worden "
        "ingezet."
    ),
    "info.tenure": (
        "Koop: de grond wordt meegefinancierd, inclusief de kosten koper daarop. Erfpacht "
        "(Erbbaurecht): de grond wordt niet gekocht; in plaats daarvan wordt jaarlijks een "
        "erfpachtcanon (Erbbauzins) over de grondwaarde betaald (standaard 4 %, onder "
        "„Uitgebreid”), die met de inflatie stijgt."
    ),
    "info.persons": "Aantal personen dat in het project woont en huur betaalt.",
    "info.equity_per_person": (
        "Inleg per persoon (coöperatief aandeel of inbreng in de rechtspersoon, Einlage). "
        "Inleg kost geen rente en wordt niet volgens schema afgelost. Wie vertrekt, krijgt de "
        "inleg geïndexeerd terug; nieuwe leden kopen zich in tegen dezelfde waarde. Het "
        "bedrag in het project blijft daardoor constant."
    ),
    "info.member_loan_per_person": (
        "Ledenlening (Mitgliederdarlehen) per persoon. De rente wordt niet uitbetaald maar "
        "jaarlijks bij de lening opgeteld (bijgeschreven). Aan het einde van de looptijd "
        "(standaard 15 jaar, onder „Uitgebreid”) wordt alles inclusief samengestelde rente "
        "ineens terugbetaald."
    ),
    "info.direct_loans_5y": (
        "Achtergestelde particuliere leningen van sympathisanten (Direktkredite) over 5 jaar. "
        "De rente wordt jaarlijks uitbetaald, het bedrag na 5 jaar ineens terugbetaald. Omdat "
        "ze achtergesteld zijn, rekenen banken directe leningen meestal als quasi-eigen "
        "vermogen."
    ),
    "info.direct_loans_10y": (
        "Als hierboven, maar over 10 jaar. Langere looptijden hebben meestal een hogere rente."
    ),
    "info.subsidy": (
        "Subsidielening (Förderdarlehen, bijv. KfW of een regionale ontwikkelingsbank) als "
        "annuïteit; rente en looptijd onder „Uitgebreid” (standaard 1,5 % over 30 jaar). "
        "Alleen bruikbaar voor renovatiekosten, dus hoogstens zo hoog als die. Telt niet als "
        "quasi-eigen vermogen."
    ),
    "info.bank_repayment": (
        "Annuïteit: gelijkblijvende termijn van rente en aflossing, in het begin veel rente. "
        "Lineair: gelijkblijvende aflossing; de termijn is eerst hoger en daalt daarna."
    ),
    "info.bank_term_years": "Looptijd waarna de banklening volledig is afgelost.",
    "info.bank_rate_change": (
        "Na 10 jaar eindigt de rentevaste periode. Voor de herfinanciering wordt de rente met "
        "1 procentpunt verlaagd, gelijk gehouden of verhoogd."
    ),
    "info.surplus_use": (
        "Geldt vanaf het jaar waarin bank- en subsidieleningen zijn afgelost (A4). "
        "Huurverlaging: de huur daalt met de vrijgekomen rente en aflossing. Huurteruggave: "
        "het bedrag wordt gespaard en elke 15 jaar aan alle leden terugbetaald. "
        "Solidariteitsoverdracht (Solidartransfer): het geld gaat naar een volgend project. "
        "De benodigde aanvangshuur verandert daardoor meestal niet, alleen het verloop "
        "daarna."
    ),
    "info.min_equity_like_pct": (
        "Banken eisen meestal dat eigen vermogen en achtergestelde middelen (inleg, "
        "ledenleningen, directe leningen) een minimumdeel van de totale investering dekken, "
        "vaak 20 tot 30 %. Vul hier de eis van jullie bank in."
    ),
    "info.vacancy_pct": (
        "Deel van de huur dat gemiddeld wegvalt, bijv. door leegstand bij wisselingen of "
        "betalingsachterstanden. Geldt vanaf het 4e jaar."
    ),
    "info.initial_vacancy_pct": (
        "Huurderving in de eerste 3 jaar, zolang het huis nog wordt betrokken en gerenoveerd."
    ),
    "info.admin_cost_per_year": (
        "Beheer, boekhouding, controle (bij een coöperatie de controlerende federatie), "
        "bankkosten. Stijgt met de inflatie."
    ),
    "info.insurance_per_year": "Opstal- en aansprakelijkheidsverzekering. Stijgt met de inflatie.",
    "info.min_liquidity_months": (
        "Zoveel maandhuren moet de rekening altijd minstens bevatten. Bij de start wordt dit "
        "met de banklening gefinancierd. Meer reserve betekent meer zekerheid, maar ook een "
        "hogere huur."
    ),
    "info.max_arrears_years": (
        "Hoe lang een verschuldigde terugbetaling van directe of ledenleningen hoogstens mag "
        "worden uitgesteld. 0 betekent: alles moet op tijd worden betaald."
    ),
    "info.ancillary_cost_pct": (
        "Overdrachtsbelasting, notaris, kadaster en eventueel makelaar, in % van de koopprijs "
        "van huis en (bij koop) grond. De Duitse overdrachtsbelasting (Grunderwerbsteuer) "
        "ligt per deelstaat tussen 3,5 en 6,5 %."
    ),
    "info.leasehold_rate_pct": (
        "Jaarlijkse erfpachtcanon (Erbbauzins) in % van de grondwaarde. Stijgt met de "
        "inflatie. Geldt alleen bij erfpacht."
    ),
    "info.member_loan_term_years": (
        "Na zoveel jaar worden ledenleningen inclusief bijgeschreven rente ineens "
        "terugbetaald. Langere looptijden schuiven de grote terugbetaling naar achteren, "
        "maar laten meer samengestelde rente oplopen."
    ),
    "info.subsidy_term_years": (
        "Looptijd van de subsidieleningen; ze worden als annuïteit afgelost."
    ),
    "info.maintenance_reserve_pct": (
        "Dit deel van de herbouwwaarde (60 % van huis plus renovatie, zonder grond) wordt "
        "elk jaar opzij gezet en aan onderhoud besteed, stijgend met de inflatie."
    ),
    "info.member_type": (
        "Voorinstellingen voor inleg en ledenlening van dit lid. „Eigen waarden” laat de "
        "waarden vrij instellen."
    ),
    "info.member_equity": (
        "Inleg van dit lid in geld van vandaag. Die wordt bij intrek geïndexeerd ingebracht "
        "en bij vertrek geïndexeerd terugbetaald."
    ),
    "info.member_loan_personal": (
        "Ledenlening van dit lid. Ze groeit met de rente van de ledenleningen en wordt aan "
        "het einde van de looptijd of in het jaar na vertrek inclusief samengestelde rente "
        "terugbetaald."
    ),
    "info.entry_year": (
        "Jaar van intrek, geteld vanaf de start van het project (0 = vanaf het begin)."
    ),
    "info.exit_year": "Jaar van vertrek. Inleg en lening komen het jaar daarna terug.",
    "info.market_rent": (
        "Wat een vergelijkbare woning of kamer op de markt per persoon per maand kost, in "
        "dezelfde eenheid als de projecthuur. Stijgt met de inflatie."
    ),
    "info.target_rent": (
        "De huur die een persoon in het eerste jaar per maand wil of kan betalen. Daarna "
        "stijgt ze met de inflatie."
    ),
    "info.bank_loan": (
        "De banklening sluit het gat: totale investering + startliquiditeit (minimale "
        "reserve) − inleg − ledenleningen − directe leningen − subsidieleningen. Omdat de "
        "startliquiditeit van de huur afhangt, wordt ze samen met de huur berekend."
    ),
    "info.inflation_range": (
        "Bandbreedte van de jaarlijkse inflatie. Meest waarschijnlijk: startpagina."
    ),
    "info.bank_change_range": (
        "Wijziging van de bankrente na de rentevaste periode (10 jaar), in procentpunten. "
        "Meest waarschijnlijk: de keuze op de startpagina (daalt −1, gelijk 0, stijgt +1)."
    ),
    "info.vacancy_range": (
        "Bandbreedte van de huurderving vanaf het 4e jaar. Meest waarschijnlijk: startpagina."
    ),
    "info.renovation_range": (
        "Renovatiekosten in % van jullie schatting. 130 % betekent: de renovatie wordt 30 % "
        "duurder. Meest waarschijnlijk: 100 %."
    ),
    "info.running_range": (
        "Beheer en verzekering in % van jullie schatting. Meest waarschijnlijk: 100 %."
    ),
    "info.n_samples": (
        "Meer varianten maken de uitkomst stabieler, maar duren langer (in de browser "
        "ongeveer 2,5 seconde per 100 varianten)."
    ),
    # Summaries under input boxes
    "summary.costs": "Kosten koper ({rate}): **{ancillary}**  \nTotale investering: **{total}**",
    "summary.costs_unknown": "Totale investering: –",
    "summary.capital": "Inleg totaal: **{equity}**  \nLedenleningen totaal: **{member_loans}**",
    # Shared page elements
    "ui.levers": "Belangrijkste instellingen",
    "ui.more_on_start": "*Alle andere aannames staan op de startpagina.*",
    "ui.how_computed": "Zo wordt gerekend",
    "ui.no_solution": "Geen oplossing: {error}",
    "ui.how_to_read": "Hoe lees ik deze grafiek?",
    "ui.values_table": "Waarden als tabel",
    "ui.year": "Jaar",
    # Errors
    "error.subsidy_above_renovation": (
        "Subsidieleningen ({subsidy}) zijn alleen voor renovatie bruikbaar en zijn hoger dan "
        "de renovatiekosten ({renovation})."
    ),
    "error.zero_price": "Grond en huis kunnen niet allebei 0 € kosten.",
    "error.own_funds_above_investment": (
        "Eigen middelen en subsidieleningen ({own}) zijn hoger dan de totale investering "
        "({total}). Verlaag de bedragen."
    ),
    "error.exit_before_entry": "Het vertrek moet na de intrek liggen.",
    "error.rent_too_low_for_own_funds": (
        "Zelfs een huis ter waarde van jullie eigen middelen ({lower}) heeft meer dan "
        "{target} huur per persoon nodig. Verhoog de doelhuur of pas de eigen middelen aan."
    ),
    "error.no_upper_bound": "Geen bovengrens voor de investering gevonden; controleer de invoer.",
    "error.bank_rule_no_house": (
        "De eigenvermogenseis van de bank laat geen huis toe dat jullie eigen middelen kan "
        "opnemen: inleg, ledenleningen en directe leningen zijn te klein ten opzichte van de "
        "subsidieleningen."
    ),
    # Bank loan and equity check
    "bank.line": "**Banklening (automatisch): {amount}**",
    "bank.check": (
        "Eigen vermogen + achtergesteld: {equity_like} = {share} van de totale investering "
        "(minimum {min_share}). Banklening : eigen vermogen + achtergesteld = {ratio}."
    ),
    "bank.missing": (
        "{check} Er ontbreekt {gap} aan inleg, ledenleningen of directe leningen; zo "
        "financiert een bank waarschijnlijk niet."
    ),
    # Methods
    "method.mode1": """
Het model rekent 50 jaar in stappen van een jaar. Elk jaar geldt:
**nieuw saldo = oud saldo + huurinkomsten − exploitatiekosten − rente − aflossing**
(min terugbetaling van vervallen directe en ledenleningen, huurverlaging uit het overschot,
huurteruggave of solidariteitsoverdracht).

- **Huurinkomsten**: huur × personen × 12, min huurderving (in de eerste 3 jaar hoger).
- **Exploitatiekosten**: storting in de onderhoudsreserve (deel van de herbouwwaarde),
  beheer en verzekering.
- **Rente en aflossing**: per lening volgens de voorwaarden, nominaal vast.
- **Minimale reserve**: de rekening mag nooit onder de minimale reserve komen (standaard
  6 maandhuren, onder „Uitgebreid”).
- **Achterstanden**: als een vervallen terugbetaling de rekening onder de reserve zou
  drukken, wordt alleen het mogelijke deel betaald; de rest wordt zo snel mogelijk
  nabetaald en moet binnen een termijn zijn voldaan (standaard 3 jaar, onder
  „Uitgebreid”). Tot dan is er rente verschuldigd.
- **Overschot (A4)**: pas als er geen achterstand openstaat en de rekening boven de reserve
  alle nog openstaande directe en ledenleningen zou kunnen dekken, gaat de rest naar
  huurverlaging, huurteruggave of solidariteitsoverdracht.

De **benodigde huur** is de laagste aanvangshuur waarbij aan deze voorwaarden in alle
50 jaar wordt voldaan, tot op de cent. Het **bepalende jaar** is het jaar waarin de
berekening met iets minder huur zou mislukken: daar zou de rekening onder de reserve komen
of een achterstand te lang openstaan. Jaren waarin de rekening precies op de reserve staat
omdat een terugbetaling wordt uitgesteld, bepalen de huur niet.
""",
    "method.mode2": """
Uitgangspunt is de benodigde huur uit modus 1 met alle aannames van de startpagina. Er
worden twee wegen voor een lid vergeleken, beide gecorrigeerd voor inflatie:

- **In het project**: het lid brengt inleg en eventueel een ledenlening in en betaalt de
  projecthuur. Alles wat het ten opzichte van de markthuur bespaart, plus huurteruggaven en
  de terugbetaalde inleg en lening, belegt het tegen het alternatieve rendement. Inleg
  (reëel) en lening (met samengestelde rente) tellen als vermogen zolang ze in het project
  zitten.
- **Markthuur + geld belegd**: inleg en leenbedrag worden in plaats daarvan tegen het
  alternatieve rendement belegd, en het lid betaalt markthuur.
- **Inleg en lening verloren** (gestreept): als „In het project”, maar inleg en lening
  vallen weg, bijv. bij een faillissement. Achtergesteld kapitaal draagt dit risico.

Huurverlagingen uit het overschot (A4) verlagen de projecthuur en verhogen zo de besparing.
Het individuele lid heeft geen invloed op de projectfinanciering.
""",
    "method.mode3": """
Jullie eigen middelen (inleg, ledenleningen, directe leningen, subsidieleningen) liggen
vast; de banklening groeit mee met het huis. Grond, huis en renovatie worden daarbij naar
verhouding van jullie kostenschatting op- of afgeschaald. Twee grenzen bepalen hoe duur het
huis mag zijn:

- **Doelhuur**: hoe duurder het huis, hoe groter de banklening en hoe hoger de benodigde
  huur (modus 1). Gezocht wordt de grootste investering waarvan de benodigde huur de
  doelhuur niet overschrijdt, tot op 1.000 € nauwkeurig.
- **Eigenvermogenseis van de bank**: inleg, ledenleningen en directe leningen moeten
  minstens het minimumdeel van de investering dekken, dus
  investering ≤ (inleg + ledenleningen + directe leningen) / minimumdeel.

De toelaatbare investering is de kleinste van de twee grenzen.
""",
    "method.uncertainty": """
Veel aannames kennen jullie vandaag niet precies. Hier geven jullie voor de vijf
belangrijkste een bandbreedte op. De calculator trekt daaruit veel varianten
(Latin-hypercube-steekproef) en zoekt voor elke variant de benodigde huur zoals in modus 1,
tot op 50 cent.

- Binnen elke bandbreedte is de waarde van de startpagina het **meest waarschijnlijk**;
  waarden naar de randen toe worden zeldzamer (driehoeksverdeling).
- De **veilige huur** is de huur die in 90 % van de varianten volstaat.
- Alle overige aannames komen ongewijzigd van de startpagina.
- Dezelfde invoer geeft altijd dezelfde uitkomst (vaste toevalsstartwaarde).
""",
    # Chart reading guides
    "help.annual_costs": """
Elke balk laat zien waaraan het project in een jaar geld uitgeeft; de zwarte lijn zijn de
huurinkomsten na huurderving.

- **Balken boven de lijn**: het project betaalt dat jaar bij uit de rekening.
- **Balken onder de lijn**: de rekening groeit.
- Alle waarden zijn **gecorrigeerd voor inflatie** (koopkracht van jaar 1). Een
  horizontale lijn betekent dus: de huur stijgt precies met de inflatie. Rente en
  aflossing van de bank liggen nominaal vast en worden daardoor reëel elk jaar kleiner.
- De hoge balken in afzonderlijke jaren zijn **vervaldata** van directe en ledenleningen.
  Wat daar niet meteen lukt, verschijnt in de volgende jaren als nabetaling.
- Vanaf het jaar waarin het **overschot** vrijkomt, vult huurverlaging, huurteruggave of
  solidariteitsoverdracht het gat tot de lijn.

Ga met de muis over een jaar om alle bedragen te zien.
""",
    "help.debt_balances": """
Hoeveel het project aan het einde van elk jaar nog schuldig is, per lening en in totaal
(gestreept), gecorrigeerd voor inflatie.

- **Bank en subsidie** dalen gestaag door de aflossing.
- **Directe leningen** blijven staan tot ze vervallen (5 of 10 jaar) en vallen dan naar
  nul. **Ledenleningen** groeien tot de vervaldatum (standaard 15 jaar) door de
  samengestelde rente.
- **Achterstanden** tonen wat na de vervaldatum nog moet worden nabetaald.
""",
    "help.liquidity": """
Saldo aan het einde van het jaar vergeleken met de minimale reserve (gestreept, standaard
6 maandhuren), gecorrigeerd voor inflatie.

- De huur is zo gekozen dat de rekening **nooit onder** de reserve komt. Waar de lijnen
  elkaar raken, wordt er een terugbetaling uitgesteld (rekening precies op de reserve) of
  het is het bepalende jaar.
- Voor vervaldata van leningen spaart de rekening op, daarna daalt ze.
- Zodra er geen achterstand openstaat en alle directe en ledenleningen gedekt zouden zijn,
  wordt het **overschot** afgeroomd; daarom groeit de rekening dan niet verder.
- Gestippeld: de **onderhoudsreserve**, een aparte pot die niet als liquiditeit telt.
""",
    "help.arrears": """
- **Balken**: hoeveel van de vervallen directe en ledenleningen op de vervaldag niet kon
  worden betaald zonder onder de minimale reserve te komen.
- **Lijn**: hoeveel daarvan aan het einde van het jaar nog openstaat. Ze moet binnen de
  termijn weer op nul staan; tot dan betaalt het project rente over de achterstand.

Voor geldschieters betekent een balk: ze krijgen hun geld later dan afgesproken.
""",
    "help.investment_curve": """
Hoeveel huis (totale investering) bij een bepaalde doelhuur per persoon te financieren is,
in prijzen van vandaag.

- De **lijn** stijgt, omdat een hogere huur een grotere banklening kan dragen.
- **Gestreept**: de bovengrens door de eigenvermogenseis van de bank; die hangt niet van
  de huur af.
- Toelaatbaar is steeds de **laagste** van de twee lijnen. Het punt markeert jullie
  doelhuur.
""",
    "help.liquidity_mode3": """
Saldo van het huis dat bij jullie doelhuur nog net te financieren is, vergeleken met de
minimale reserve (gestreept), gecorrigeerd voor inflatie. Waar de lijn de reserve raakt,
zit het huis op de grens van wat de doelhuur kan dragen.
""",
    "help.member_wealth": """
Vermogen van het lid in de loop van de tijd, gecorrigeerd voor inflatie.

- **In het project** boven **Markthuur + geld belegd**: het project loont financieel. Het
  verschil is het voordeel.
- In het begin ligt de vergelijking vaak voor, omdat geld op de markt meer rendement
  oplevert dan inleg en lening. De huurbesparing haalt dat in de loop van de jaren in.
- **Gestreept**: als inleg en lening verloren zouden gaan, bijv. bij een faillissement.
  Ligt ook deze lijn boven de vergelijking, dan loont het project zelfs dan.
""",
    "help.rent_distribution": """
Elke balk telt hoeveel varianten een benodigde huur in dat bereik hebben.

- **Gestippeld**: de huur uit modus 1, met de waarden van de startpagina.
- **Doorgetrokken**: de mediaan; de helft van de varianten heeft minder nodig, de helft
  meer.
- **Gestreept**: de veilige huur. Slechts 10 % van de varianten heeft meer nodig.

Hoe breder de verdeling, hoe meer de huur afhangt van aannames die jullie vandaag niet
kennen. Een verschil tussen de huur uit modus 1 en de veilige huur is een buffer die jullie
kunnen inplannen.
""",
    "help.headroom_band": """
Hoeveel geld er boven de minimale reserve op de rekening staat als jullie de veilige huur
rekenen, gecorrigeerd voor inflatie.

- **Lijn**: mediaan over alle varianten.
- **Band**: 80 % van de varianten ligt daarbinnen (tussen het 10e en 90e percentiel).
- De buffer is elk jaar hoogstens zo hoog totdat het overschot wordt afgeroomd; daarna
  ligt hij dicht bij nul.

Ligt de onderkant van de band onder nul, dan komen in dat jaar enkele varianten onder de
reserve. Dat zijn de 10 % waarvoor de veilige huur niet volstaat.
""",
    "help.sensitivity": """
Hoe sterk elke onzekere aanname samenhangt met de benodigde huur (rangcorrelatie, −1 tot
+1).

- **Positief** (blauw): is de aanname hoger, dan stijgt de huur, bijv. hogere
  renovatiekosten.
- **Negatief** (rood): is de aanname hoger, dan daalt de huur. Bij inflatie komt dat
  doordat de huur met de inflatie meegroeit, rente en aflossing niet.
- Hoe langer de balk, hoe meer het loont om deze aanname nauwkeuriger uit te zoeken.
""",
    # Mode 1 KPIs
    "kpi.required_rent.label": "Benodigde huur",
    "kpi.required_rent.help": (
        "Laagste huur per persoon per maand waarbij de rekening in alle 50 jaar boven de "
        "minimale reserve blijft en elke achterstand binnen {years} jaar is voldaan. Daarna "
        "stijgt ze met de inflatie."
    ),
    "kpi.per_person_month": "per persoon per maand",
    "kpi.rent_income.label": "Huurinkomsten jaar 1",
    "kpi.rent_income.help": "Huur van alle personen in het eerste jaar, voor huurderving.",
    "kpi.rent_income.note": "per jaar, alle personen",
    "kpi.investment.label": "Totale investering",
    "kpi.investment.help": "Grond (bij koop), huis, renovatie en kosten koper.",
    "kpi.binding.label": "Bepalend jaar",
    "kpi.binding.help": (
        "Het jaar dat de benodigde huur vastlegt: met iets minder huur zou in dit jaar de "
        "minimale reserve worden onderschreden of een achterstand te lang openstaan. Latere "
        "lasten veranderen de huur pas als ze dit jaar overnemen."
    ),
    "kpi.binding.note_reserve": "jaar {year}, reserve",
    "kpi.binding.note_arrears": "jaar {year}, achterstand te lang open",
    "kpi.payoff.label": "Bank en subsidie afgelost",
    "kpi.payoff.help": (
        "Vanaf het jaar daarna komen de rente- en aflossingslasten vrij en worden ze gebruikt "
        "zoals gekozen voor het overschot."
    ),
    "kpi.surplus_start.label": "Overschot vanaf",
    "kpi.surplus_start.help": (
        "Vanaf dit jaar staat er geen achterstand open en dekt de rekening de reserve plus "
        "alle openstaande directe en ledenleningen. De rest gaat naar huurverlaging, "
        "huurteruggave of solidariteitsoverdracht."
    ),
    "kpi.late.label": "Niet op tijd terugbetaald",
    "kpi.late.help": (
        "Deel van de vervallen directe en ledenleningen dat op de vervaldag niet kon worden "
        "betaald (nominaal). Het wordt binnen {years} jaar nabetaald; details in de grafiek "
        "hieronder."
    ),
    "alert.sub_debt_grew": (
        "Na {years} jaar zijn directe en ledenleningen reëel hoger dan aan het begin, omdat "
        "rente op ledenleningen sneller oploopt dan wordt terugbetaald. Deze schuld zit niet "
        "in de benodigde huur."
    ),
    # Mode 2 KPIs
    "kpi.project_rent.label": "Projecthuur",
    "kpi.project_rent.help": (
        "Benodigde huur uit modus 1, per persoon per maand in het eerste jaar."
    ),
    "kpi.from_mode1": "uit modus 1",
    "kpi.saving.label": "Besparing t.o.v. markthuur",
    "kpi.saving.help": (
        "Markthuur min projecthuur in het eerste jaar na intrek. Later groeit de besparing "
        "zodra het overschot de huur verlaagt."
    ),
    "kpi.saving.note": "per maand, eerste jaar",
    "kpi.advantage.label": "Voordeel",
    "kpi.advantage.help": (
        "Vermogen in het project min vermogen met markthuur en belegd geld, aan het einde, "
        "gecorrigeerd voor inflatie."
    ),
    "kpi.advantage.note": "tot {end}",
    "kpi.wealth_project.label": "Vermogen in het project",
    "kpi.wealth_project.help": (
        "Belegde besparingen en terugbetalingen plus inleg en lening zolang ze in het project "
        "zitten; gecorrigeerd voor inflatie."
    ),
    "kpi.wealth_market.label": "Vermogen met markthuur",
    "kpi.wealth_market.help": (
        "Inleg en leenbedrag tegen het alternatieve rendement belegd, markthuur betaald; "
        "gecorrigeerd voor inflatie."
    ),
    "kpi.default.label": "Bij verlies van inleg en lening",
    "kpi.default.help": (
        "Voordeel als inleg en lening volledig verloren zouden gaan, bijv. bij een "
        "faillissement van het project."
    ),
    "kpi.default.note": "voordeel t.o.v. markthuur",
    # Mode 3 KPIs
    "kpi.admissible.label": "Toelaatbare investering",
    "kpi.admissible.help": (
        "De kleinste van de twee grenzen: wat de doelhuur kan dragen en wat de "
        "eigenvermogenseis van de bank toelaat."
    ),
    "kpi.admissible.by_rent": "begrensd door doelhuur",
    "kpi.admissible.by_equity": "begrensd door eigen vermogen",
    "kpi.share.label": "Deel van jullie kostenschatting",
    "kpi.share.help": (
        "Toelaatbare investering gedeeld door jullie kostenschatting (grond, huis, renovatie "
        "en kosten koper van de startpagina). Vanaf 100 % is het huis te financieren."
    ),
    "kpi.share.note": "schatting {estimate}",
    "kpi.rent_limit.label": "Grens door doelhuur",
    "kpi.rent_limit.help": (
        "Grootste investering waarvan de benodigde huur de doelhuur niet overschrijdt."
    ),
    "kpi.bank_limit.label": "Grens door eigen vermogen",
    "kpi.bank_limit.help": (
        "(Inleg + ledenleningen + directe leningen) / minimumdeel dat de bank eist."
    ),
    "kpi.bank_limit.none": "geen",
    # Uncertainty page
    "unc.ranges": "Bandbreedtes",
    "unc.compute": "Berekenen",
    "unc.hint": "*Meest waarschijnlijke waarde steeds van de startpagina.*",
    "unc.prompt": "Stel de bandbreedtes in en klik op „Berekenen”.",
    "unc.stale": (
        "Aannames zijn gewijzigd. De uitkomsten hieronder zijn verouderd; bereken opnieuw."
    ),
    "kpi.base.label": "Huur zonder onzekerheid",
    "kpi.base.help": "Benodigde huur uit modus 1, met de waarden van de startpagina.",
    "kpi.median.label": "Mediaan",
    "kpi.median.help": "De helft van de varianten heeft minder nodig, de helft meer.",
    "kpi.spread.label": "Bandbreedte 10–90 %",
    "kpi.spread.help": "80 % van de varianten heeft een huur in dit bereik nodig.",
    "kpi.safe.label": "Veilige huur",
    "kpi.safe.help": (
        "Volstaat in 90 % van de varianten. Het verschil met de huur zonder onzekerheid is "
        "een buffer voor ongunstige ontwikkelingen."
    ),
    "kpi.safe.note": "{amount} boven modus 1",
    "kpi.failed.label": "Varianten zonder oplossing",
    "kpi.failed.help": (
        "In deze varianten volstaat geen huur tot 5.000 € per persoon; ze ontbreken in de "
        "evaluatie."
    ),
    # Methodology page
    "methodik.inputs_heading": "## Invoer en standaardwaarden",
    "methodik.table_header": "| Onderdeel | Invoer | Standaard | Betekenis |",
    # Charts
    "chart.real_subtitle": "gecorrigeerd voor inflatie, in koopkracht van {year} (jaar 1)",
    "chart.tranche.equity": "Inleg",
    "chart.tranche.member_loan": "Ledenleningen",
    "chart.tranche.direct_loan": "Directe leningen",
    "chart.tranche.subsidy_loan": "Subsidielening",
    "chart.tranche.bank_loan": "Banklening",
    "chart.tranche.direct_loans_5y": "Directe leningen 5 jaar",
    "chart.tranche.direct_loans_10y": "Directe leningen 10 jaar",
    "chart.costs.title": "Jaarlijkse uitgaven en huurinkomsten",
    "chart.costs.y": "per jaar",
    "chart.costs.operating": "Exploitatie incl. onderhoudsreserve",
    "chart.costs.senior_interest": "Rente bank en subsidie",
    "chart.costs.senior_repayment": "Aflossing bank en subsidie",
    "chart.costs.direct_interest": "Rente directe leningen",
    "chart.costs.member_interest": "Rente ledenleningen (bij terugbetaling)",
    "chart.costs.sub_repayment": "Terugbetaling directe en ledenleningen (op tijd)",
    "chart.costs.arrears": "Nabetaling achterstanden incl. rente",
    "chart.costs.rebate": "Huurverlaging uit overschot",
    "chart.costs.payout": "Huurteruggave",
    "chart.costs.transfer": "Solidariteitsoverdracht",
    "chart.costs.rent_income": "Huurinkomsten",
    "chart.arrears.title": "Niet op tijd terugbetaalde directe en ledenleningen",
    "chart.arrears.new": "Niet terugbetaald op de vervaldag",
    "chart.arrears.open": "Openstaande achterstand aan het einde van het jaar",
    "chart.debt.title": "Restschuld aan het einde van het jaar",
    "chart.debt.arrears": "Achterstanden",
    "chart.debt.total": "Totaal",
    "chart.liquidity.title": "Liquiditeit en reserve",
    "chart.liquidity.liquidity": "Liquiditeit",
    "chart.liquidity.reserve": "Minimale reserve",
    "chart.liquidity.maintenance": "Onderhoudsreserve (aparte pot)",
    "chart.member.title": "Vermogen van het lid",
    "chart.member.project": "In het project",
    "chart.member.market": "Markthuur + geld belegd",
    "chart.member.default": "In het project, inleg en lening verloren",
    "chart.curve.title": "Toelaatbare investering per doelhuur",
    "chart.curve.subtitle": "prijzen van vandaag",
    "chart.curve.rent_limit": "Grens door doelhuur",
    "chart.curve.bank_limit": "Grens door eigenvermogenseis",
    "chart.curve.point": "Toelaatbaar bij doelhuur",
    "chart.curve.x": "Doelhuur (€ per persoon/maand)",
    "chart.curve.hover_rent": "Doelhuur",
    "chart.curve.hover_investment": "Investering",
    "chart.uncertain.inflation": "Inflatie",
    "chart.uncertain.bank_rate_change_pp": "Bankrente na 10 jaar",
    "chart.uncertain.vacancy_rate": "Huurderving",
    "chart.uncertain.renovation_factor": "Renovatiekosten",
    "chart.uncertain.running_cost_factor": "Beheer en verzekering",
    "chart.dist.title": "Benodigde huur over alle varianten",
    "chart.dist.count": "Aantal varianten",
    "chart.dist.base": "Zonder onzekerheid",
    "chart.dist.median": "Mediaan",
    "chart.dist.safe": "Veilige huur (volstaat in 90 %)",
    "chart.dist.x": "Benodigde huur (€ per persoon/maand)",
    "chart.dist.hover_variants": "varianten",
    "chart.band.title": "Buffer boven de minimale reserve bij veilige huur",
    "chart.band.p90": "90e percentiel",
    "chart.band.band": "10–90 %-band",
    "chart.band.median": "Mediaan",
    "chart.band.reserve": "Minimale reserve",
    "chart.sens.title": "Wat drijft de onzekerheid?",
    "chart.sens.y": "Rangcorrelatie met de huur",
    "chart.sens.name": "Samenhang",
    # Additional uncertain inputs
    "label.member_loan_term_range": "Looptijd ledenleningen (jaar)",
    "label.member_loan_range": "Ledenleningen (% van planning)",
    "label.direct_loans_10y_range": "Directe leningen 10 jr. (% van planning)",
    "info.member_loan_term_range": (
        "Bandbreedte van de looptijd van de ledenleningen in hele jaren. Meest "
        "waarschijnlijk: startpagina (onder „Uitgebreid”)."
    ),
    "info.member_loan_range": (
        "Hoeveel ledenleningen er werkelijk binnenkomen, in % van het geplande bedrag. "
        "Ontbreekt er geld, dan springt de banklening bij. Meest waarschijnlijk: 100 %."
    ),
    "info.direct_loans_10y_range": (
        "Hoeveel directe leningen van 10 jaar er werkelijk worden opgehaald, in % van het "
        "geplande bedrag. Ontbreekt er geld, dan springt de banklening bij. Meest "
        "waarschijnlijk: 100 %."
    ),
    "chart.uncertain.member_loan_term_years": "Looptijd ledenleningen",
    "chart.uncertain.member_loan_factor": "Omvang ledenleningen",
    "chart.uncertain.direct_loans_10y_factor": "Omvang directe leningen 10 jaar",
    # Rates relative to inflation, member loan payoff, nominal display
    "label.member_loan_spread_pp": "Rente ledenleningen (%-punt boven inflatie)",
    "label.direct_loan_spread_5y_pp": "Rente 5 jaar (%-punt boven inflatie)",
    "label.direct_loan_spread_10y_pp": "Rente 10 jaar (%-punt boven inflatie)",
    "label.bank_spread_pp": "Bankrente (%-punt boven inflatie)",
    "label.subsidy_spread_pp": "Rente subsidieleningen (%-punt boven inflatie)",
    "label.alt_return_spread_pp": "Alternatief rendement (%-punt boven inflatie)",
    "info.member_loan_spread_pp": (
        "Rente op ledenleningen in procentpunten boven de inflatie; ze wordt bij de "
        "lening bijgeschreven. Voorbeeld: 3 bij 2 % inflatie geeft 5 % rente."
    ),
    "info.direct_loan_spread_5y_pp": (
        "Rente op directe leningen van 5 jaar in procentpunten boven de inflatie, "
        "jaarlijks uitbetaald. Negatieve waarden betekenen: rente onder de inflatie."
    ),
    "info.direct_loan_spread_10y_pp": (
        "Rente op directe leningen van 10 jaar in procentpunten boven de inflatie, "
        "jaarlijks uitbetaald."
    ),
    "info.bank_spread_pp": (
        "Rente van de banklening voor de eerste 10 jaar, in procentpunten boven de "
        "inflatie. Die hangt af van de marktrente, niet direct van de inflatie: vaak lag "
        "ze 1 tot 3 procentpunt hoger, maar van 2015 tot 2021 rond of onder de inflatie. "
        "De rente ligt vast bij het afsluiten en volgt daarna de inflatie niet meer."
    ),
    "info.subsidy_spread_pp": (
        "Rente van de subsidieleningen in procentpunten boven de inflatie, vast over de "
        "hele looptijd. Subsidierentes liggen vaak onder de inflatie (negatieve waarde)."
    ),
    "info.alt_return_spread_pp": (
        "Rendement per jaar in procentpunten boven de inflatie als het geld elders in "
        "plaats van in het project zou worden belegd (bijv. een breed gespreid fonds). "
        "Alle besparingen van het lid worden tegen hetzelfde rendement belegd."
    ),
    "info.inflation_pct": (
        "Jaarlijkse inflatie. Huur, exploitatiekosten en erfpachtcanon stijgen daarmee. "
        "Alle rentes worden ten opzichte van de inflatie ingevoerd en bewegen mee; is een"
        " lening eenmaal afgesloten, dan liggen rente en aflossing nominaal vast. Daarom "
        "is meestal het eerste jaar het krapst."
    ),
    "summary.rates": (
        "Nominaal bij {inflation} inflatie: bank {bank} (na 10 jr. {follow_up}), subsidie"
        " {subsidy}, directe leningen {dk5} / {dk10}, ledenleningen {member}"
    ),
    "label.member_loan_payoff": "Terugbetaling van ledenleningen",
    "info.member_loan_payoff": (
        "Waar het geld vandaan komt als de ledenleningen inclusief rente vervallen. Uit "
        "liquiditeit: de rekening betaalt wat kan zonder onder de reserve te komen, de "
        "rest wordt als achterstand nabetaald. Nieuwe banklening: het hele bedrag wordt "
        "tegen de nieuwe bankrente gefinancierd, als annuïteit of lineaire lening over de"
        " resterende looptijd van de banklening, minstens 10 jaar. Nieuwe directe "
        "leningen: het hele bedrag wordt met directe leningen van 10 jaar tegen de "
        "10-jaarsrente gefinancierd, die na 10 jaar vervallen."
    ),
    "option.member_loan_payoff.liquidity": "Uit liquiditeit",
    "option.member_loan_payoff.bank": "Nieuwe banklening",
    "option.member_loan_payoff.direct_loans": "Nieuwe directe leningen 10 jr.",
    "label.display": "Grafieken",
    "info.display": (
        "Gecorrigeerd voor inflatie: alle bedragen in koopkracht van jaar 1, zodat jaren "
        "direct vergelijkbaar zijn. Nominaal: de werkelijke eurobedragen van elk jaar; "
        "huur en kosten groeien dan zichtbaar met de inflatie."
    ),
    "option.display.real": "gecorrigeerd voor inflatie",
    "option.display.nominal": "nominaal",
    "chart.nominal_subtitle": "nominaal, werkelijke eurobedragen van elk jaar",
    "help.nominal_note": (
        "*De grafiek toont nu nominale bedragen; de uitleg hieronder gaat over de "
        "weergave gecorrigeerd voor inflatie.*\n"
    ),
    "chart.tranche.bank_refinance": "Banklening voor ledenleningen",
    "chart.tranche.direct_loans_refinance": "Directe leningen voor ledenleningen",
    "chart.costs.refinancing": "Nieuwe lening voor ledenleningen (instroom)",
    # Direct loan rollover
    "label.direct_loan_rollover_pct": "Vervangen bij vervaldatum (10 jr.)",
    "info.direct_loan_rollover_pct": (
        "Welk deel van de directe leningen van 10 jaar elke 10 jaar door nieuwe directe "
        "leningen wordt vervangen; alleen de rest wordt van de rekening terugbetaald. 0 % "
        "betekent: alles wordt afgelost. Geldt ook voor directe leningen die de ledenleningen"
        " aflossen. Directe leningen van 5 jaar worden altijd afgelost."
    ),
    "option.direct_loan_rollover_pct.0": "0 %",
    "option.direct_loan_rollover_pct.25": "25 %",
    "option.direct_loan_rollover_pct.50": "50 %",
    "option.direct_loan_rollover_pct.75": "75 %",
    "option.direct_loan_rollover_pct.100": "100 %",
}
