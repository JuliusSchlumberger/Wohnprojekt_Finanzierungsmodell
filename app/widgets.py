"""Shared dashboard inputs; every page renders widgets bound to one `Inputs` instance."""

from __future__ import annotations

import panel as pn
import param

from app.layout import ADVANCED_BOX_HEIGHT, START_BOX_HEIGHT, START_BOX_WIDTH, box
from model.member import MemberInputs
from model.presets import BANK_RATE_CHANGE_STEP, ProjectInputs

_D = ProjectInputs()
_M = MemberInputs()

MEMBER_PRESETS = {
    "Eigene Angaben": None,
    "Wenig Kapital": (2_000.0, 2_000.0),
    "Mittel": (2_000.0, 20_000.0),
    "Viel": (2_000.0, 40_000.0),
}

INFO = {
    "land_price": (
        "Kaufpreis des Grundstücks. Bei Erbbaurecht wird es nicht gekauft; der Betrag gilt "
        "dann als Grundstückswert, auf den der Erbbauzins (Satz unter „Erweitert“) berechnet wird."
    ),
    "building_price": "Kaufpreis des Hauses ohne Grundstück.",
    "renovation_cost": (
        "Kosten für Sanierung und Umbau. Nur dafür können Förderdarlehen eingesetzt werden."
    ),
    "tenure": (
        "Kauf: das Grundstück wird mitfinanziert, auch die Kaufnebenkosten darauf. "
        "Erbbaurecht: das Grundstück wird nicht gekauft, stattdessen fällt jährlich ein "
        "Erbbauzins auf den Grundstückswert an (Standard 4 %, unter „Erweitert“), der mit der "
        "Inflation steigt."
    ),
    "persons": "Anzahl der Personen, die im Projekt wohnen und Miete zahlen.",
    "equity_per_person": (
        "Einlage pro Person (Genossenschaftsanteil bzw. Einlage in den Rechtsträger). "
        "Einlagen kosten keine Zinsen und werden nicht getilgt. Wer auszieht, bekommt die "
        "Einlage inflationsindexiert zurück; neue Mitglieder kaufen sich zum selben Wert ein. "
        "Der Bestand im Projekt bleibt deshalb konstant."
    ),
    "member_loan_per_person": (
        "Mitgliederdarlehen pro Person über 15 Jahre. Die Zinsen werden nicht ausgezahlt, "
        "sondern jährlich dem Darlehen gutgeschrieben (thesauriert). Nach 15 Jahren wird "
        "alles samt Zinseszins auf einmal zurückgezahlt."
    ),
    "member_loan_rate_pct": "Zins auf Mitgliederdarlehen, wird dem Darlehen gutgeschrieben.",
    "direct_loans_5y": (
        "Nachrangige Privatdarlehen von Unterstützer*innen über 5 Jahre. Zinsen werden "
        "jährlich ausgezahlt, der Betrag nach 5 Jahren auf einmal zurück. Banken werten "
        "Direktkredite wegen des Nachrangs meist als eigenkapitalähnlich."
    ),
    "direct_loan_rate_5y_pct": "Zins auf 5-Jahres-Direktkredite, jährlich ausgezahlt.",
    "direct_loans_10y": (
        "Wie oben, aber über 10 Jahre. Längere Laufzeiten haben meist einen höheren Zins."
    ),
    "direct_loan_rate_10y_pct": ("Zins auf 10-Jahres-Direktkredite, jährlich ausgezahlt."),
    "subsidy": (
        "Förderdarlehen (z. B. KfW oder Landesförderbank) als Annuität; Zins und Laufzeit "
        "unter „Erweitert“ (Standard 1,5 % über 30 Jahre). Nur für Sanierungskosten nutzbar, "
        "deshalb höchstens so hoch wie diese. "
        "Zählt nicht als eigenkapitalähnlich."
    ),
    "bank_rate_pct": (
        "Sollzins des Bankdarlehens für die ersten 10 Jahre. Er hängt vom Marktzins ab, "
        "nicht direkt von der Inflation: oft lag er 1 bis 3 Prozentpunkte darüber, "
        "2015 bis 2021 aber nahe an oder unter der Inflation."
    ),
    "bank_repayment": (
        "Annuität: gleichbleibende Rate aus Zins und Tilgung, anfangs viel Zins. "
        "Ratenkredit: gleichbleibende Tilgung, die Rate ist anfangs höher und sinkt dann."
    ),
    "bank_term_years": "Laufzeit, nach der das Bankdarlehen vollständig getilgt ist.",
    "bank_rate_change": (
        "Nach 10 Jahren endet die Zinsbindung. Für die Anschlussfinanzierung wird der Zins "
        f"um {100 * BANK_RATE_CHANGE_STEP:.0f} Prozentpunkt gesenkt, beibehalten oder erhöht."
    ),
    "inflation_pct": (
        "Jährliche Inflation. Miete, Betriebskosten und Erbbauzins steigen damit; Zins und "
        "Tilgung bleiben nominal fest. Deshalb ist meist das erste Jahr am engsten."
    ),
    "surplus_use": (
        "Gilt ab dem Jahr, in dem Bank- und Förderdarlehen getilgt sind (A4). Mietsenkung: "
        "die Miete sinkt um den frei gewordenen Kapitaldienst. Mietrückzahlung: der Betrag "
        "wird angespart und alle 15 Jahre an alle Mitglieder zurückgezahlt. "
        "Solidartransfer: das Geld geht an ein nächstes Projekt. Die erforderliche "
        "Anfangsmiete ändert sich dadurch in der Regel nicht, nur der Verlauf danach."
    ),
    "min_equity_like_pct": (
        "Banken verlangen meist, dass Eigenkapital und nachrangige Mittel (Einlagen, "
        "Mitgliederdarlehen, Direktkredite) einen Mindestanteil der Gesamtinvestition "
        "decken, oft 20 bis 30 %. Tragt hier die Anforderung eurer Bank ein."
    ),
    "vacancy_pct": (
        "Anteil der Miete, der im Schnitt ausfällt, z. B. durch Leerstand bei Wechseln oder "
        "Zahlungsausfälle. Gilt ab dem 4. Jahr."
    ),
    "initial_vacancy_pct": (
        "Mietausfall in den ersten 3 Jahren, solange das Haus noch bezogen und saniert wird."
    ),
    "maintenance_rate_pct": (
        "Was die laufende Instandhaltung tatsächlich kostet, in % des "
        "Wiederherstellungswerts pro Jahr. Wird aus der Instandhaltungsrücklage bezahlt."
    ),
    "admin_cost_per_year": (
        "Verwaltung, Buchhaltung, Prüfung (bei eG Prüfungsverband), Bankgebühren. Steigt mit "
        "der Inflation."
    ),
    "insurance_per_year": "Gebäude- und Haftpflichtversicherung. Steigt mit der Inflation.",
    "min_liquidity_months": (
        "So viele Monatsmieten muss das Konto immer mindestens enthalten. Sie wird zu Beginn "
        "über das Bankdarlehen finanziert. Mehr Reserve heißt mehr Sicherheit, aber auch eine "
        "höhere Miete."
    ),
    "max_arrears_years": (
        "Wie lange eine fällige Rückzahlung von Direkt- oder Mitgliederdarlehen höchstens "
        "aufgeschoben werden darf. 0 heißt: alles muss pünktlich gezahlt werden."
    ),
    "ancillary_cost_pct": (
        "Grunderwerbsteuer, Notar, Grundbuch und ggf. Makler, in % des Kaufpreises von Haus "
        "und (bei Kauf) Grundstück. Die Grunderwerbsteuer liegt je nach Bundesland bei "
        "3,5 bis 6,5 %."
    ),
    "leasehold_rate_pct": (
        "Jährlicher Erbbauzins in % des Grundstückswerts. Steigt mit der Inflation. Gilt nur "
        "bei Erbbaurecht."
    ),
    "subsidy_rate_pct": "Zins der Förderdarlehen, fest über die ganze Laufzeit.",
    "subsidy_term_years": "Laufzeit der Förderdarlehen; sie werden als Annuität getilgt.",
    "maintenance_reserve_pct": (
        "So viel vom Wiederherstellungswert fließt jedes Jahr in die "
        "Instandhaltungsrücklage, mit der Inflation steigend. Daraus wird die laufende "
        "Instandhaltung (Standard 1,5 %, unter „Erweitert“) bezahlt; der Rest bleibt für größere "
        "Arbeiten angespart. Die "
        "Rücklage ist ein eigener Topf und zählt nicht zur Liquidität."
    ),
    "member_type": (
        "Voreinstellungen für Einlage und Mitgliederdarlehen dieses Mitglieds. "
        "„Eigene Angaben“ lässt die Werte frei einstellen."
    ),
    "member_equity": (
        "Einlage dieses Mitglieds in heutigem Geld. Sie wird beim Einzug "
        "inflationsindexiert eingezahlt und beim Auszug inflationsindexiert zurückgezahlt."
    ),
    "member_loan_personal": (
        "Mitgliederdarlehen dieses Mitglieds. Es wird zum Zins der Mitgliederdarlehen "
        "thesauriert und nach 15 Jahren oder im Jahr nach dem Auszug samt Zinseszins "
        "zurückgezahlt."
    ),
    "entry_year": "Jahr des Einzugs, gezählt ab Projektstart (0 = von Anfang an).",
    "exit_year": "Jahr des Auszugs. Einlage und Darlehen kommen im Jahr danach zurück.",
    "market_rent": (
        "Was eine vergleichbare Wohnung bzw. ein Zimmer am Markt pro Person und Monat "
        "kostet, in derselben Einheit wie die Projektmiete. Steigt mit der Inflation."
    ),
    "alt_return_pct": (
        "Nominale Rendite pro Jahr, wenn das Geld statt im Projekt anderswo angelegt würde "
        "(z. B. breit gestreuter Fonds). Mit derselben Rendite werden auch alle "
        "Ersparnisse des Mitglieds angelegt."
    ),
    "target_rent": (
        "Die Miete, die eine Person im ersten Jahr zahlen will oder kann, pro Monat. "
        "Danach steigt sie mit der Inflation."
    ),
    "bank_loan": (
        "Das Bankdarlehen schließt die Lücke: Gesamtinvestition + Startliquidität "
        "(Mindestreserve) − Einlagen − Mitgliederdarlehen − Direktkredite − "
        "Förderdarlehen. Weil die Startliquidität von der Miete abhängt, wird es zusammen "
        "mit der Miete berechnet."
    ),
}

_EUR = {"type": pn.widgets.FloatInput, "format": "0,0", "step": 10_000}
_EUR_PERSON = {"type": pn.widgets.FloatInput, "format": "0,0", "step": 500}
_SLIDER = {"type": pn.widgets.FloatSlider}
_INT = {"type": pn.widgets.IntSlider}
_RADIO = {"type": pn.widgets.RadioButtonGroup, "color": "primary", "variant": "outline"}
UNLABELLED_WIDGETS = (pn.widgets.RadioButtonGroup, pn.widgets.RadioBoxGroup)

WIDGETS = {
    "land_price": _EUR,
    "building_price": _EUR,
    "renovation_cost": _EUR,
    "tenure": _RADIO,
    "persons": _INT,
    "equity_per_person": _EUR_PERSON,
    "member_loan_per_person": _EUR_PERSON,
    "member_loan_rate_pct": _SLIDER,
    "direct_loans_5y": _EUR,
    "direct_loan_rate_5y_pct": _SLIDER,
    "direct_loans_10y": _EUR,
    "direct_loan_rate_10y_pct": _SLIDER,
    "subsidy": _EUR,
    "bank_rate_pct": _SLIDER,
    "bank_repayment": _RADIO,
    "bank_term_years": _INT,
    "bank_rate_change": _RADIO,
    "inflation_pct": _SLIDER,
    "surplus_use": {"type": pn.widgets.RadioBoxGroup},
    "min_equity_like_pct": _SLIDER,
    "target_rent": {"type": pn.widgets.FloatSlider, "step": 10},
    "maintenance_reserve_pct": _SLIDER,
    "maintenance_rate_pct": _SLIDER,
    "admin_cost_per_year": _EUR_PERSON,
    "insurance_per_year": _EUR_PERSON,
    "min_liquidity_months": _SLIDER,
    "max_arrears_years": _INT,
    "ancillary_cost_pct": _SLIDER,
    "leasehold_rate_pct": _SLIDER,
    "subsidy_rate_pct": _SLIDER,
    "subsidy_term_years": _INT,
    "vacancy_pct": _SLIDER,
    "initial_vacancy_pct": _SLIDER,
    "member_type": {"type": pn.widgets.Select},
    "member_equity": _EUR,
    "member_loan_personal": _EUR,
    "entry_year": _INT,
    "exit_year": _INT,
    "market_rent": {"type": pn.widgets.FloatSlider, "step": 10},
    "alt_return_pct": _SLIDER,
}

SECTIONS = {
    "Haus und Kosten": ["land_price", "tenure", "building_price", "renovation_cost"],
    "Gruppe und Betrieb": [
        "persons",
        "inflation_pct",
        "vacancy_pct",
        "initial_vacancy_pct",
        "maintenance_reserve_pct",
    ],
    "Eigenmittel": [
        "equity_per_person",
        "member_loan_per_person",
        "member_loan_rate_pct",
        "min_equity_like_pct",
    ],
    "Direktkredite": [
        "direct_loans_5y",
        "direct_loan_rate_5y_pct",
        "direct_loans_10y",
        "direct_loan_rate_10y_pct",
    ],
    "Bank und Förderung": [
        "subsidy",
        "bank_rate_pct",
        "bank_repayment",
        "bank_term_years",
        "bank_rate_change",
    ],
    "Überschuss und Zielmiete": ["surplus_use", "target_rent"],
    "Mitglied: Kapital (Modus 2)": ["member_type", "member_equity", "member_loan_personal"],
    "Mitglied: Vergleich (Modus 2)": ["entry_year", "exit_year", "market_rent", "alt_return_pct"],
}

ADVANCED_SECTIONS = {
    "Betrieb": ["admin_cost_per_year", "insurance_per_year", "maintenance_rate_pct"],
    "Liquidität und Rückstände": ["min_liquidity_months", "max_arrears_years"],
    "Kauf und Erbbaurecht": ["ancillary_cost_pct", "leasehold_rate_pct"],
    "Förderdarlehen": ["subsidy_rate_pct", "subsidy_term_years"],
}


class Inputs(param.Parameterized):
    """All inputs in UI units (EUR, percent, years); one instance shared by all pages."""

    land_price = param.Number(_D.land_price, bounds=(0, None), label="Grundstück (€)")
    building_price = param.Number(_D.building_price, bounds=(0, None), label="Haus (€)")
    renovation_cost = param.Number(_D.renovation_cost, bounds=(0, None), label="Sanierung (€)")
    tenure = param.Selector(
        objects={"Kauf": "purchase", "Erbbaurecht": "leasehold"}, label="Grundstück"
    )
    persons = param.Integer(_D.persons, bounds=(1, 200), label="Personenzahl")
    equity_per_person = param.Number(
        _D.equity / _D.persons, bounds=(0, None), label="Einlage pro Person (€)"
    )
    member_loan_per_person = param.Number(
        _D.member_loans / _D.persons,
        bounds=(0, None),
        label="Mitgliederdarlehen pro Person (€)",
    )
    member_loan_rate_pct = param.Number(
        100 * _D.member_loan_rate, bounds=(0, 8), step=0.1, label="Zins Mitgliederdarlehen (%)"
    )
    direct_loans_5y = param.Number(
        _D.direct_loans_5y, bounds=(0, None), label="Direktkredite 5 Jahre (€)"
    )
    direct_loan_rate_5y_pct = param.Number(
        100 * _D.direct_loan_rate_5y, bounds=(0, 5), step=0.1, label="Zins 5 Jahre (%)"
    )
    direct_loans_10y = param.Number(
        _D.direct_loans_10y, bounds=(0, None), label="Direktkredite 10 Jahre (€)"
    )
    direct_loan_rate_10y_pct = param.Number(
        100 * _D.direct_loan_rate_10y, bounds=(0, 5), step=0.1, label="Zins 10 Jahre (%)"
    )
    subsidy = param.Number(_D.subsidy, bounds=(0, None), label="Förderdarlehen (€)")
    bank_rate_pct = param.Number(100 * _D.bank_rate, bounds=(0, 10), step=0.1, label="Bankzins (%)")
    bank_repayment = param.Selector(
        objects={"Annuität": "annuity", "Ratenkredit": "linear"}, label="Tilgungsform Bank"
    )
    bank_term_years = param.Integer(
        _D.bank_term_years, bounds=(10, 50), label="Laufzeit Bank (Jahre)"
    )
    bank_rate_change = param.Selector(
        objects={"sinkt": -1, "bleibt": 0, "steigt": 1},
        default=_D.bank_rate_change,
        label="Bankzins nach 10 Jahren",
    )
    inflation_pct = param.Number(100 * _D.inflation, bounds=(0, 6), step=0.1, label="Inflation (%)")
    surplus_use = param.Selector(
        objects={
            "Mietsenkung": "rent_reduction",
            "Mietrückzahlung alle 15 Jahre": "payout_15y",
            "Solidartransfer": "next_project",
        },
        label="Nach Tilgung von Bank- und Förderdarlehen",
    )
    min_equity_like_pct = param.Number(
        20.0, bounds=(0, 100), step=1, label="Mindestanteil EK + Nachrang (%)"
    )
    target_rent = param.Number(500.0, bounds=(100, 2_000), label="Zielmiete pro Person (€/Monat)")
    maintenance_reserve_pct = param.Number(
        100 * _D.maintenance_reserve_rate,
        bounds=(1.5, 4),
        step=0.1,
        label="Instandhaltungsrücklage (%)",
    )
    vacancy_pct = param.Number(
        100 * _D.vacancy_rate, bounds=(0, 15), step=0.5, label="Mietausfall (%)"
    )
    initial_vacancy_pct = param.Number(
        100 * _D.initial_vacancy_rate,
        bounds=(0, 50),
        step=1,
        label="Mietausfall erste 3 Jahre (%)",
    )
    maintenance_rate_pct = param.Number(
        100 * _D.maintenance_rate, bounds=(0.5, 3), step=0.1, label="Instandhaltung (%)"
    )
    admin_cost_per_year = param.Number(
        _D.admin_cost_per_year, bounds=(0, None), label="Verwaltung pro Jahr (€)"
    )
    insurance_per_year = param.Number(
        _D.insurance_per_year, bounds=(0, None), label="Versicherung pro Jahr (€)"
    )
    min_liquidity_months = param.Number(
        _D.min_liquidity_months, bounds=(1, 12), step=1, label="Mindestreserve (Monatsmieten)"
    )
    max_arrears_years = param.Integer(
        _D.max_arrears_years, bounds=(0, 10), label="Rückstand höchstens (Jahre)"
    )
    ancillary_cost_pct = param.Number(
        100 * _D.ancillary_cost_rate, bounds=(0, 15), step=0.5, label="Kaufnebenkosten (%)"
    )
    leasehold_rate_pct = param.Number(
        100 * _D.leasehold_rate, bounds=(0, 8), step=0.1, label="Erbbauzins (%)"
    )
    subsidy_rate_pct = param.Number(
        100 * _D.subsidy_rate, bounds=(0, 5), step=0.1, label="Zins Förderdarlehen (%)"
    )
    subsidy_term_years = param.Integer(
        _D.subsidy_term_years, bounds=(10, 40), label="Laufzeit Förderdarlehen (Jahre)"
    )
    member_type = param.Selector(
        objects=list(MEMBER_PRESETS), default="Eigene Angaben", label="Mitgliedertyp"
    )
    member_equity = param.Number(_M.equity, bounds=(0, None), label="Einlage (€)")
    member_loan_personal = param.Number(
        _M.member_loan, bounds=(0, None), label="Mitgliederdarlehen (€)"
    )
    entry_year = param.Integer(_M.entry_year, bounds=(0, 49), label="Einzug (Jahr)")
    exit_year = param.Integer(_M.exit_year, bounds=(1, 50), label="Auszug (Jahr)")
    market_rent = param.Number(
        _M.market_rent, bounds=(100, 2_000), label="Marktmiete pro Person (€/Monat)"
    )
    alt_return_pct = param.Number(
        100 * _M.alt_return, bounds=(0, 10), step=0.1, label="Alternativrendite (%)"
    )

    def to_project(self) -> ProjectInputs:
        return ProjectInputs(
            land_price=self.land_price,
            building_price=self.building_price,
            renovation_cost=self.renovation_cost,
            tenure=self.tenure,
            persons=self.persons,
            equity=self.equity_per_person * self.persons,
            member_loans=self.member_loan_per_person * self.persons,
            member_loan_rate=self.member_loan_rate_pct / 100,
            direct_loans_5y=self.direct_loans_5y,
            direct_loan_rate_5y=self.direct_loan_rate_5y_pct / 100,
            direct_loans_10y=self.direct_loans_10y,
            direct_loan_rate_10y=self.direct_loan_rate_10y_pct / 100,
            subsidy=self.subsidy,
            bank_rate=self.bank_rate_pct / 100,
            bank_repayment=self.bank_repayment,
            bank_term_years=self.bank_term_years,
            bank_rate_change=self.bank_rate_change,
            inflation=self.inflation_pct / 100,
            maintenance_reserve_rate=self.maintenance_reserve_pct / 100,
            vacancy_rate=self.vacancy_pct / 100,
            maintenance_rate=self.maintenance_rate_pct / 100,
            admin_cost_per_year=self.admin_cost_per_year,
            insurance_per_year=self.insurance_per_year,
            min_liquidity_months=self.min_liquidity_months,
            max_arrears_years=self.max_arrears_years,
            ancillary_cost_rate=self.ancillary_cost_pct / 100,
            leasehold_rate=self.leasehold_rate_pct / 100,
            subsidy_rate=self.subsidy_rate_pct / 100,
            subsidy_term_years=self.subsidy_term_years,
            initial_vacancy_rate=self.initial_vacancy_pct / 100,
            surplus_use=self.surplus_use,
        )

    def to_member(self) -> MemberInputs:
        return MemberInputs(
            equity=self.member_equity,
            member_loan=self.member_loan_personal,
            member_loan_rate=self.member_loan_rate_pct / 100,
            entry_year=self.entry_year,
            exit_year=self.exit_year,
            market_rent=self.market_rent,
            alt_return=self.alt_return_pct / 100,
        )

    @param.depends("member_type", watch=True)
    def _apply_member_preset(self) -> None:
        preset = MEMBER_PRESETS[self.member_type]
        if preset is not None:
            self.param.update(member_equity=preset[0], member_loan_personal=preset[1])

    def input_names(self) -> list[str]:
        return [p for p in self.param if p != "name"]

    def widget(self, name: str) -> pn.viewable.Viewable:
        """A new widget bound to the shared parameter, with its info icon."""
        spec = dict(WIDGETS[name])
        kind = spec.pop("type")
        widget = kind.from_param(self.param[name], **spec)
        if kind in UNLABELLED_WIDGETS:
            label = pn.pane.HTML(
                f"<div style='font-size:13px'>{self.param[name].label}</div>", margin=(4, 10, 0, 10)
            )
            widget = pn.Column(label, widget, margin=0)
        return with_info(widget, INFO[name])

    def widgets(self, names: list[str]) -> list[pn.viewable.Viewable]:
        return [self.widget(n) for n in names]

    @param.depends(
        "land_price", "building_price", "renovation_cost", "tenure", "ancillary_cost_pct"
    )
    def cost_summary(self) -> pn.viewable.Viewable:
        try:
            p = self.to_project()
            total = p.total_investment
        except ValueError:
            return pn.pane.Markdown("Gesamtinvestition: –")
        rate = f"{100 * p.ancillary_cost_rate:.0f} %"
        return pn.pane.Markdown(
            f"Kaufnebenkosten ({rate}): **{eur(p.ancillary_cost)}**  \n"
            f"Gesamtinvestition: **{eur(total)}**"
        )

    @param.depends("persons", "equity_per_person", "member_loan_per_person")
    def capital_summary(self) -> pn.viewable.Viewable:
        return pn.pane.Markdown(
            f"Einlagen gesamt: **{eur(self.equity_per_person * self.persons)}**  \n"
            f"Mitgliederdarlehen gesamt: **{eur(self.member_loan_per_person * self.persons)}**",
            styles={"font-size": "13px"},
        )

    def all_inputs(self) -> pn.viewable.Viewable:
        """Every input in boxes of equal height; used on the start page."""
        boxes = []
        for title, names in SECTIONS.items():
            extra = {
                "Haus und Kosten": [self.cost_summary],
                "Eigenmittel": [self.capital_summary],
            }.get(title, [])
            boxes.append(
                box(
                    title,
                    *self.widgets(names),
                    *extra,
                    height=START_BOX_HEIGHT,
                    width=START_BOX_WIDTH,
                )
            )
        advanced = [
            box(title, *self.widgets(names), height=ADVANCED_BOX_HEIGHT, width=START_BOX_WIDTH)
            for title, names in ADVANCED_SECTIONS.items()
        ]
        return pn.Column(
            pn.FlexBox(*boxes, sizing_mode="stretch_width"),
            pn.Accordion(
                (
                    "Erweitert: Betrieb, Reserve, Nebenkosten, Förderkonditionen",
                    pn.FlexBox(*advanced, sizing_mode="stretch_width"),
                ),
                active=[],
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )


def eur(value: float, digits: int = 0) -> str:
    text = f"{value:,.{digits}f}".replace(",", " ").replace(".", ",").replace(" ", ".")
    return f"{text} €"


def with_info(widget: pn.viewable.Viewable, text: str) -> pn.viewable.Viewable:
    """Widget with a hover icon that explains the mechanism behind it."""
    widget.sizing_mode = "stretch_width"
    return pn.Row(widget, pn.widgets.TooltipIcon(value=text, align="end"))
