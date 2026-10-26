"""Shared dashboard inputs; every page renders widgets bound to one `Inputs` instance."""

from __future__ import annotations

import panel as pn
import param

from app.i18n import DEFAULT_LANGUAGE, LANGUAGES, Translator
from app.layout import ADVANCED_BOX_HEIGHT, START_BOX_HEIGHT, START_BOX_WIDTH, box
from model.member import MemberInputs
from model.presets import BANK_RATE_CHANGE_STEP, ProjectInputs

_D = ProjectInputs()
_M = MemberInputs()


def _spread(nominal_rate: float) -> float:
    """Default spread in percentage points above the default inflation."""
    return round(100 * (nominal_rate - _D.inflation), 2)


MEMBER_PRESETS = {
    "custom": None,
    "low": (2_000.0, 2_000.0),
    "mid": (2_000.0, 20_000.0),
    "high": (2_000.0, 40_000.0),
}

# Choice inputs: stored value -> text key suffix of its display name.
OPTIONS = {
    "tenure": {"purchase": "purchase", "leasehold": "leasehold"},
    "bank_repayment": {"annuity": "annuity", "linear": "linear"},
    "bank_rate_change": {-1: "down", 0: "same", 1: "up"},
    "direct_loan_rollover_pct": {v: str(v) for v in (0, 25, 50, 75, 100)},
    "surplus_use": {
        "rent_reduction": "rent_reduction",
        "payout_15y": "payout_15y",
        "next_project": "next_project",
    },
    "member_type": {key: key for key in MEMBER_PRESETS},
    "member_loan_payoff": {
        "liquidity": "liquidity",
        "bank": "bank",
        "direct_loans": "direct_loans",
    },
    "display": {"real": "real", "nominal": "nominal"},
}
# Inputs that only change how results are shown, not the results.
DISPLAY_INPUTS = ("language", "display")

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
    "member_loan_spread_pp": _SLIDER,
    "direct_loans_5y": _EUR,
    "direct_loan_spread_5y_pp": _SLIDER,
    "direct_loans_10y": _EUR,
    "direct_loan_spread_10y_pp": _SLIDER,
    "direct_loan_rollover_pct": _RADIO,
    "subsidy": _EUR,
    "bank_spread_pp": _SLIDER,
    "bank_repayment": _RADIO,
    "bank_term_years": _INT,
    "bank_rate_change": _RADIO,
    "inflation_pct": _SLIDER,
    "surplus_use": {"type": pn.widgets.RadioBoxGroup},
    "min_equity_like_pct": _SLIDER,
    "target_rent": {"type": pn.widgets.FloatSlider, "step": 10},
    "maintenance_reserve_pct": _SLIDER,
    "admin_cost_per_year": _EUR_PERSON,
    "insurance_per_year": _EUR_PERSON,
    "min_liquidity_months": _SLIDER,
    "max_arrears_years": _INT,
    "ancillary_cost_pct": _SLIDER,
    "leasehold_rate_pct": _SLIDER,
    "subsidy_spread_pp": _SLIDER,
    "subsidy_term_years": _INT,
    "member_loan_term_years": _INT,
    "member_loan_payoff": {"type": pn.widgets.RadioBoxGroup},
    "display": _RADIO,
    "vacancy_pct": _SLIDER,
    "initial_vacancy_pct": _SLIDER,
    "member_type": {"type": pn.widgets.Select},
    "member_equity": _EUR,
    "member_loan_personal": _EUR,
    "entry_year": _INT,
    "exit_year": _INT,
    "market_rent": {"type": pn.widgets.FloatSlider, "step": 10},
    "alt_return_spread_pp": _SLIDER,
}

SECTIONS = {
    "house": ["land_price", "tenure", "building_price", "renovation_cost"],
    "group": [
        "persons",
        "inflation_pct",
        "vacancy_pct",
        "initial_vacancy_pct",
        "maintenance_reserve_pct",
    ],
    "own_funds": [
        "equity_per_person",
        "member_loan_per_person",
        "member_loan_spread_pp",
        "min_equity_like_pct",
    ],
    "direct_loans": [
        "direct_loans_5y",
        "direct_loan_spread_5y_pp",
        "direct_loans_10y",
        "direct_loan_spread_10y_pp",
        "direct_loan_rollover_pct",
    ],
    "bank": [
        "subsidy",
        "bank_spread_pp",
        "bank_repayment",
        "bank_term_years",
        "bank_rate_change",
    ],
    "surplus": ["surplus_use", "target_rent"],
    "member_capital": ["member_type", "member_equity", "member_loan_personal"],
    "member_compare": ["entry_year", "exit_year", "market_rent", "alt_return_spread_pp"],
}

ADVANCED_SECTIONS = {
    "adv_operations": ["admin_cost_per_year", "insurance_per_year"],
    "adv_liquidity": ["min_liquidity_months", "max_arrears_years"],
    "adv_purchase": ["ancillary_cost_pct", "leasehold_rate_pct"],
    "adv_subsidy": ["subsidy_spread_pp", "subsidy_term_years"],
    "adv_member_loans": ["member_loan_term_years", "member_loan_payoff"],
}


class Inputs(param.Parameterized):
    """All inputs in UI units (EUR, percent, years); one instance shared by all pages.

    Labels and option names follow `language`; stored values do not.
    """

    language = param.Selector(objects=list(LANGUAGES), default=DEFAULT_LANGUAGE)
    land_price = param.Number(_D.land_price, bounds=(0, None))
    building_price = param.Number(_D.building_price, bounds=(0, None))
    renovation_cost = param.Number(_D.renovation_cost, bounds=(0, None))
    tenure = param.Selector(objects=list(OPTIONS["tenure"]), default=_D.tenure)
    persons = param.Integer(_D.persons, bounds=(1, 200))
    equity_per_person = param.Number(_D.equity / _D.persons, bounds=(0, None))
    member_loan_per_person = param.Number(_D.member_loans / _D.persons, bounds=(0, None))
    member_loan_spread_pp = param.Number(_spread(_D.member_loan_rate), bounds=(-2, 8), step=0.1)
    direct_loans_5y = param.Number(_D.direct_loans_5y, bounds=(0, None))
    direct_loan_spread_5y_pp = param.Number(
        _spread(_D.direct_loan_rate_5y), bounds=(-2, 5), step=0.1
    )
    direct_loans_10y = param.Number(_D.direct_loans_10y, bounds=(0, None))
    direct_loan_rollover_pct = param.Selector(
        objects=list(OPTIONS["direct_loan_rollover_pct"]),
        default=round(100 * _D.direct_loan_rollover_rate),
    )
    direct_loan_spread_10y_pp = param.Number(
        _spread(_D.direct_loan_rate_10y), bounds=(-2, 5), step=0.1
    )
    subsidy = param.Number(_D.subsidy, bounds=(0, None))
    bank_spread_pp = param.Number(_spread(_D.bank_rate), bounds=(-2, 10), step=0.1)
    bank_repayment = param.Selector(objects=list(OPTIONS["bank_repayment"]), default="annuity")
    bank_term_years = param.Integer(_D.bank_term_years, bounds=(10, 50))
    bank_rate_change = param.Selector(
        objects=list(OPTIONS["bank_rate_change"]), default=_D.bank_rate_change
    )
    inflation_pct = param.Number(100 * _D.inflation, bounds=(0, 6), step=0.1)
    surplus_use = param.Selector(objects=list(OPTIONS["surplus_use"]), default=_D.surplus_use)
    min_equity_like_pct = param.Number(20.0, bounds=(0, 100), step=1)
    target_rent = param.Number(500.0, bounds=(100, 2_000))
    maintenance_reserve_pct = param.Number(
        100 * _D.maintenance_reserve_rate, bounds=(1.5, 4), step=0.1
    )
    vacancy_pct = param.Number(100 * _D.vacancy_rate, bounds=(0, 15), step=0.5)
    initial_vacancy_pct = param.Number(100 * _D.initial_vacancy_rate, bounds=(0, 50), step=1)
    admin_cost_per_year = param.Number(_D.admin_cost_per_year, bounds=(0, None))
    insurance_per_year = param.Number(_D.insurance_per_year, bounds=(0, None))
    min_liquidity_months = param.Number(_D.min_liquidity_months, bounds=(1, 12), step=1)
    max_arrears_years = param.Integer(_D.max_arrears_years, bounds=(0, 10))
    ancillary_cost_pct = param.Number(100 * _D.ancillary_cost_rate, bounds=(0, 15), step=0.5)
    leasehold_rate_pct = param.Number(100 * _D.leasehold_rate, bounds=(0, 8), step=0.1)
    subsidy_spread_pp = param.Number(_spread(_D.subsidy_rate), bounds=(-3, 5), step=0.1)
    subsidy_term_years = param.Integer(_D.subsidy_term_years, bounds=(10, 40))
    member_loan_term_years = param.Integer(_D.member_loan_term_years, bounds=(5, 30))
    member_loan_payoff = param.Selector(
        objects=list(OPTIONS["member_loan_payoff"]), default=_D.member_loan_payoff
    )
    display = param.Selector(objects=list(OPTIONS["display"]), default="real")
    member_type = param.Selector(objects=list(MEMBER_PRESETS), default="custom")
    member_equity = param.Number(_M.equity, bounds=(0, None))
    member_loan_personal = param.Number(_M.member_loan, bounds=(0, None))
    entry_year = param.Integer(_M.entry_year, bounds=(0, 49))
    exit_year = param.Integer(_M.exit_year, bounds=(1, 50))
    market_rent = param.Number(_M.market_rent, bounds=(100, 2_000))
    alt_return_spread_pp = param.Number(_spread(_M.alt_return), bounds=(-3, 10), step=0.1)

    def __init__(self, **params):
        super().__init__(**params)
        self.apply_language()

    @property
    def tr(self) -> Translator:
        return Translator(self.language)

    @param.depends("language", watch=True)
    def apply_language(self) -> None:
        """Set labels and option names of every input to the current language."""
        tr = self.tr
        for name in [*self.input_names(), "display"]:
            self.param[name].label = tr(f"label.{name}")
        for name, options in OPTIONS.items():
            value = getattr(self, name)
            self.param[name].objects = {
                tr(f"option.{name}.{key}"): option for option, key in options.items()
            }
            setattr(self, name, value)

    def _nominal(self, spread_pp: float) -> float:
        """Nominal rate (fraction) for a spread above inflation; never negative."""
        return max((self.inflation_pct + spread_pp) / 100, 0.0)

    def to_project(self) -> ProjectInputs:
        return ProjectInputs(
            land_price=self.land_price,
            building_price=self.building_price,
            renovation_cost=self.renovation_cost,
            tenure=self.tenure,
            persons=self.persons,
            equity=self.equity_per_person * self.persons,
            member_loans=self.member_loan_per_person * self.persons,
            member_loan_rate=self._nominal(self.member_loan_spread_pp),
            direct_loans_5y=self.direct_loans_5y,
            direct_loan_rate_5y=self._nominal(self.direct_loan_spread_5y_pp),
            direct_loans_10y=self.direct_loans_10y,
            direct_loan_rate_10y=self._nominal(self.direct_loan_spread_10y_pp),
            direct_loan_rollover_rate=self.direct_loan_rollover_pct / 100,
            subsidy=self.subsidy,
            bank_rate=self._nominal(self.bank_spread_pp),
            bank_repayment=self.bank_repayment,
            bank_term_years=self.bank_term_years,
            bank_rate_change=self.bank_rate_change,
            inflation=self.inflation_pct / 100,
            maintenance_reserve_rate=self.maintenance_reserve_pct / 100,
            vacancy_rate=self.vacancy_pct / 100,
            admin_cost_per_year=self.admin_cost_per_year,
            insurance_per_year=self.insurance_per_year,
            min_liquidity_months=self.min_liquidity_months,
            max_arrears_years=self.max_arrears_years,
            ancillary_cost_rate=self.ancillary_cost_pct / 100,
            leasehold_rate=self.leasehold_rate_pct / 100,
            subsidy_rate=self._nominal(self.subsidy_spread_pp),
            subsidy_term_years=self.subsidy_term_years,
            member_loan_term_years=self.member_loan_term_years,
            member_loan_payoff=self.member_loan_payoff,
            initial_vacancy_rate=self.initial_vacancy_pct / 100,
            surplus_use=self.surplus_use,
        )

    def to_member(self) -> MemberInputs:
        return MemberInputs(
            equity=self.member_equity,
            member_loan=self.member_loan_personal,
            member_loan_rate=self._nominal(self.member_loan_spread_pp),
            member_loan_term_years=self.member_loan_term_years,
            entry_year=self.entry_year,
            exit_year=self.exit_year,
            market_rent=self.market_rent,
            alt_return=(self.inflation_pct + self.alt_return_spread_pp) / 100,
        )

    @param.depends("member_type", watch=True)
    def _apply_member_preset(self) -> None:
        preset = MEMBER_PRESETS[self.member_type]
        if preset is not None:
            self.param.update(member_equity=preset[0], member_loan_personal=preset[1])

    def input_names(self) -> list[str]:
        """Inputs that change results; language and display only change how they are shown."""
        return [p for p in self.param if p not in ("name", *DISPLAY_INPUTS)]

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
        return with_info(widget, self.tr(f"info.{name}"))

    def widgets(self, names: list[str]) -> list[pn.viewable.Viewable]:
        return [self.widget(n) for n in names]

    @param.depends(
        "land_price", "building_price", "renovation_cost", "tenure", "ancillary_cost_pct"
    )
    def cost_summary(self) -> pn.viewable.Viewable:
        tr = self.tr
        try:
            p = self.to_project()
            total = p.total_investment
        except ValueError:
            return pn.pane.Markdown(tr("summary.costs_unknown"))
        return pn.pane.Markdown(
            tr(
                "summary.costs",
                rate=tr.pct(p.ancillary_cost_rate, 0),
                ancillary=tr.eur(p.ancillary_cost),
                total=tr.eur(total),
            )
        )

    @param.depends(
        "inflation_pct",
        "bank_spread_pp",
        "bank_rate_change",
        "subsidy_spread_pp",
        "direct_loan_spread_5y_pp",
        "direct_loan_spread_10y_pp",
        "member_loan_spread_pp",
    )
    def rates_summary(self) -> pn.viewable.Viewable:
        tr, p = self.tr, self.to_project()
        follow_up = max(p.bank_rate + p.bank_rate_change * BANK_RATE_CHANGE_STEP, 0.0)
        return pn.pane.Markdown(
            tr(
                "summary.rates",
                inflation=tr.pct(p.inflation),
                bank=tr.pct(p.bank_rate),
                follow_up=tr.pct(follow_up),
                subsidy=tr.pct(p.subsidy_rate),
                dk5=tr.pct(p.direct_loan_rate_5y),
                dk10=tr.pct(p.direct_loan_rate_10y),
                member=tr.pct(p.member_loan_rate),
            ),
            styles={"font-size": "12px"},
        )

    @param.depends("persons", "equity_per_person", "member_loan_per_person")
    def capital_summary(self) -> pn.viewable.Viewable:
        tr = self.tr
        return pn.pane.Markdown(
            tr(
                "summary.capital",
                equity=tr.eur(self.equity_per_person * self.persons),
                member_loans=tr.eur(self.member_loan_per_person * self.persons),
            ),
            styles={"font-size": "13px"},
        )

    def all_inputs(self) -> pn.viewable.Viewable:
        """Every input in boxes of equal height; used on the start page."""
        tr = self.tr
        extras = {
            "house": [self.cost_summary],
            "own_funds": [self.capital_summary],
            "group": [self.rates_summary],
        }
        boxes = [
            box(
                tr(f"section.{key}"),
                *self.widgets(names),
                *extras.get(key, []),
                height=START_BOX_HEIGHT,
                width=START_BOX_WIDTH,
            )
            for key, names in SECTIONS.items()
        ]
        advanced = [
            box(
                tr(f"section.{key}"),
                *self.widgets(names),
                height=ADVANCED_BOX_HEIGHT,
                width=START_BOX_WIDTH,
            )
            for key, names in ADVANCED_SECTIONS.items()
        ]
        return pn.Column(
            pn.FlexBox(*boxes, sizing_mode="stretch_width"),
            pn.Accordion(
                (tr("start.advanced"), pn.FlexBox(*advanced, sizing_mode="stretch_width")),
                active=[],
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )


def with_info(widget: pn.viewable.Viewable, text: str) -> pn.viewable.Viewable:
    """Widget with a hover icon that explains the mechanism behind it."""
    widget.sizing_mode = "stretch_width"
    return pn.Row(widget, pn.widgets.TooltipIcon(value=text, align="end"))
