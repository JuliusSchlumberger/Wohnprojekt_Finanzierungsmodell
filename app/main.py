"""Panel app: start page, modes 1-3, sensitivity report, methodology; `panel serve app/main.py`."""

from __future__ import annotations

import math

import numpy as np
import panel as pn
import param
import plotly.graph_objects as go

from app import charts
from app.explore_page import ExplorationPage
from app.i18n import LANGUAGES, Translator
from app.layout import ACCENT, START_BOX_WIDTH, Kpi, box, chart_block, kpi_grid
from app.widgets import ADVANCED_SECTIONS, SECTIONS, Inputs, with_info
from model import Result, Scenario, max_investment, required_rent, simulate
from model.cashflow import capital_structure
from model.member import member_view
from model.presets import build_scenario
from model.solve import binding_year, is_affordable

ASSUMPTION_COUNT = 9
PAGE_KEYS = ["start", "mode1", "mode2", "mode3", "uncertainty", "methodik"]

MODE1_LEVERS = [
    "land_price",
    "tenure",
    "building_price",
    "renovation_cost",
    "equity_per_person",
    "member_loan_per_person",
    "member_loan_payoff",
    "direct_loans_5y",
    "direct_loans_10y",
    "subsidy",
    "bank_spread_pp",
    "inflation_pct",
]
MODE2_LEVERS = [
    "member_type",
    "member_equity",
    "member_loan_personal",
    "member_loan_spread_pp",
    "entry_year",
    "exit_year",
    "market_rent",
    "alt_return_spread_pp",
    "inflation_pct",
    "surplus_use",
]
MODE3_LEVERS = [
    "target_rent",
    "equity_per_person",
    "member_loan_per_person",
    "direct_loans_5y",
    "direct_loans_10y",
    "subsidy",
    "bank_spread_pp",
    "inflation_pct",
    "min_equity_like_pct",
]
CURVE_RENTS_EUR_PERSON = np.arange(200.0, 1_200.01, 50.0)
MIN_INVESTMENT_EUR = 50_000.0
LEVER_WIDTH = 360


def assumptions_table(tr: Translator) -> str:
    rows = "\n".join(
        f"| A{i} | {tr(f'assumption.{i}.title')} | {tr(f'assumption.{i}.text')} |"
        for i in range(1, ASSUMPTION_COUNT + 1)
    )
    return tr("assumptions.header") + "\n|---|---|---|\n" + rows


def _bank_line(capital: dict[str, float], tr: Translator) -> pn.viewable.Viewable:
    return with_info(
        pn.pane.Markdown(tr("bank.line", amount=tr.eur(capital["bank_loan"]))),
        tr("info.bank_loan"),
    )


def _on_demand(title: str, text: str) -> pn.viewable.Viewable:
    return pn.Accordion(
        (title, pn.pane.Markdown(text, sizing_mode="stretch_width")),
        active=[],
        sizing_mode="stretch_width",
        margin=(0, 0, 12, 0),
    )


class _Page(param.Parameterized):
    """A mode page: recomputes from the shared inputs whenever any of them changes."""

    inputs = param.ClassSelector(class_=Inputs)
    scenario = param.ClassSelector(class_=Scenario, allow_None=True)
    result = param.ClassSelector(class_=Result, allow_None=True)
    capital = param.Dict(default={})
    error = param.String(default="")

    levers: list[str] = []
    method_key: str = ""

    def __init__(self, **params):
        super().__init__(inputs=params.pop("inputs", None) or Inputs(), **params)
        self.inputs.param.watch(self._update, self.inputs.input_names())
        self._update()

    @property
    def tr(self) -> Translator:
        return self.inputs.tr

    @property
    def real(self) -> bool:
        return self.inputs.display == "real"

    def _help(self, key: str) -> str:
        """Help text for a chart; flagged when the chart shows nominal amounts."""
        text = self.tr(key)
        return text if self.real else self.tr("help.nominal_note") + text

    def _update(self, *_events) -> None:
        raise NotImplementedError

    def kpi_items(self) -> list[Kpi]:
        raise NotImplementedError

    def alerts(self) -> list[pn.viewable.Viewable]:
        return []

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        raise NotImplementedError

    def bank_status(self) -> pn.viewable.Viewable:
        return pn.Spacer(height=0)

    def _input_error(self) -> str:
        inp, tr = self.inputs, self.tr
        if inp.subsidy > inp.renovation_cost:
            return tr(
                "error.subsidy_above_renovation",
                subsidy=tr.eur(inp.subsidy),
                renovation=tr.eur(inp.renovation_cost),
            )
        if inp.land_price + inp.building_price <= 0:
            return tr("error.zero_price")
        return ""

    def _fail(self, message: str) -> None:
        self.param.update(scenario=None, result=None, capital={}, error=message)

    @param.depends("result", "error")
    def kpis(self) -> pn.viewable.Viewable:
        if self.error:
            return pn.pane.Alert(self.tr("ui.no_solution", error=self.error), alert_type="danger")
        return pn.Column(kpi_grid(self.kpi_items()), *self.alerts(), sizing_mode="stretch_width")

    @param.depends("result", "inputs.display")
    def figures(self) -> pn.viewable.Viewable:
        if self.result is None:
            return pn.Spacer(height=0)
        blocks = [chart_block(fig, text, self.tr) for fig, text in self.chart_items()]
        return pn.Column(*blocks, sizing_mode="stretch_width")

    def view(self) -> pn.viewable.Viewable:
        tr = self.tr
        levers = box(
            tr("ui.levers"),
            *self.inputs.widgets(self.levers),
            self.bank_status,
            pn.pane.Markdown(tr("ui.more_on_start"), styles={"font-size": "13px"}),
            width=LEVER_WIDTH,
        )
        return pn.Row(
            levers,
            pn.Column(
                self.kpis,
                _on_demand(tr("ui.how_computed"), tr(self.method_key)),
                self.inputs.widget("display"),
                self.figures,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )


class Mode1(_Page):
    """Required rent per person for the shared inputs."""

    levers = MODE1_LEVERS
    method_key = "method.mode1"

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        p = self.inputs.to_project()
        if p.own_funds > p.total_investment:
            tr = self.tr
            self._fail(
                tr(
                    "error.own_funds_above_investment",
                    own=tr.eur(p.own_funds),
                    total=tr.eur(p.total_investment),
                )
            )
            return
        try:
            scenario = build_scenario(p)
            rent = required_rent(scenario)
        except ValueError as exc:
            self._fail(str(exc))
            return
        self.param.update(
            scenario=scenario,
            result=simulate(scenario, rent),
            capital=capital_structure(scenario, rent),
            error="",
        )

    @param.depends("capital")
    def bank_status(self) -> pn.viewable.Viewable:
        if not self.capital:
            return pn.Spacer(height=0)
        tr, c = self.tr, self.capital
        min_share = self.inputs.min_equity_like_pct / 100
        share = c["equity_like_share"]
        ratio = c["bank_loan"] / c["equity_like"] if c["equity_like"] else math.inf
        check = tr(
            "bank.check",
            equity_like=tr.eur(c["equity_like"]),
            share=tr.pct(share),
            min_share=tr.pct(min_share),
            ratio=tr.ratio(ratio),
        )
        if share >= min_share:
            alert = pn.pane.Alert(check, alert_type="success")
        else:
            gap = (min_share - share) * self.scenario.property.total_investment
            alert = pn.pane.Alert(
                tr("bank.missing", check=check, gap=tr.eur(gap)), alert_type="warning"
            )
        return pn.Column(_bank_line(c, tr), alert, sizing_mode="stretch_width")

    def kpi_items(self) -> list[Kpi]:
        tr = self.tr
        m, tab = self.result.metrics, self.result.table
        start = self.scenario.property.start_year
        payoff = m["senior_payoff_year"]
        binding = binding_year(self.scenario, m["rent_per_person"])
        years = self.inputs.max_arrears_years
        if binding is None:
            binding_note = ""
        else:
            binding_note = tr(f"kpi.binding.note_{binding[1]}", year=binding[0])
        items = [
            Kpi(
                tr("kpi.required_rent.label"),
                tr.eur(m["rent_per_person"], 2),
                tr("kpi.required_rent.help", years=years),
                note=tr("kpi.per_person_month"),
            ),
            Kpi(
                tr("kpi.rent_income.label"),
                tr.eur(m["rent_per_year"]),
                tr("kpi.rent_income.help"),
                note=tr("kpi.rent_income.note"),
            ),
            Kpi(
                tr("kpi.investment.label"),
                tr.eur(self.scenario.property.total_investment),
                tr("kpi.investment.help"),
            ),
            Kpi(
                tr("kpi.binding.label"),
                "–" if binding is None else str(start + binding[0]),
                tr("kpi.binding.help"),
                note=binding_note,
            ),
            Kpi(
                tr("kpi.payoff.label"),
                "–" if math.isnan(payoff) else str(int(start + payoff)),
                tr("kpi.payoff.help"),
            ),
        ]
        first_surplus = tab["year"][tab["surplus"] > 0.5]
        if not first_surplus.empty:
            items.append(
                Kpi(
                    tr("kpi.surplus_start.label"),
                    str(int(first_surplus.iloc[0])),
                    tr("kpi.surplus_start.help"),
                )
            )
        late = tab["arrears_new"][tab["arrears_new"] > 0.5]
        if not late.empty:
            items.append(
                Kpi(
                    tr("kpi.late.label"),
                    tr.eur(late.sum()),
                    tr("kpi.late.help", years=years),
                    note=", ".join(str(int(tab["year"][t])) for t in late.index),
                    tone="warning",
                )
            )
        return items

    def alerts(self) -> list[pn.viewable.Viewable]:
        sub = charts.subordinated_debt_real(self.result, self.scenario)
        if not sub.any() or sub.iloc[-1] <= sub.iloc[0]:
            return []
        message = self.tr("alert.sub_debt_grew", years=len(sub) - 1)
        return [pn.pane.Alert(message, alert_type="warning")]

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        tr = self.tr
        items = [
            (
                charts.annual_costs(self.result, self.scenario, tr, self.real),
                self._help("help.annual_costs"),
            ),
            (charts.liquidity(self.result, tr, self.real), self._help("help.liquidity")),
            (
                charts.debt_balances(self.result, self.scenario, tr, self.real),
                self._help("help.debt_balances"),
            ),
        ]
        if self.result.table["arrears_new"].any():
            items.append((charts.arrears(self.result, tr, self.real), self._help("help.arrears")))
        return items


class Mode2(_Page):
    """One member's wealth in the project versus market rent and investing elsewhere."""

    view_table = param.DataFrame(default=None, allow_None=True)

    levers = MODE2_LEVERS
    method_key = "method.mode2"

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        if self.inputs.entry_year >= self.inputs.exit_year:
            self._fail(self.tr("error.exit_before_entry"))
            return
        try:
            scenario = build_scenario(self.inputs.to_project())
            result = simulate(scenario, required_rent(scenario))
        except ValueError as exc:
            self._fail(str(exc))
            return
        self.param.update(
            scenario=scenario,
            result=result,
            view_table=member_view(scenario, result, self.inputs.to_member()),
            error="",
        )

    def _fail(self, message: str) -> None:
        super()._fail(message)
        self.view_table = None

    def kpi_items(self) -> list[Kpi]:
        tr = self.tr
        v = self.view_table
        first, last = v.iloc[1], v.iloc[-1]
        end = int(last["year"])
        advantage = last["advantage"]
        return [
            Kpi(
                tr("kpi.project_rent.label"),
                tr.eur(self.result.metrics["rent_per_person"], 2),
                tr("kpi.project_rent.help"),
                note=tr("kpi.from_mode1"),
            ),
            Kpi(
                tr("kpi.saving.label"),
                tr.eur(first["rent_saving_month"]),
                tr("kpi.saving.help"),
                note=tr("kpi.saving.note"),
            ),
            Kpi(
                tr("kpi.advantage.label"),
                tr.eur(advantage),
                tr("kpi.advantage.help"),
                note=tr("kpi.advantage.note", end=end),
                tone="good" if advantage >= 0 else "warning",
            ),
            Kpi(
                tr("kpi.wealth_project.label"),
                tr.eur(last["project"]),
                tr("kpi.wealth_project.help"),
                note=f"{end}",
            ),
            Kpi(
                tr("kpi.wealth_market.label"),
                tr.eur(last["alternative"]),
                tr("kpi.wealth_market.help"),
                note=f"{end}",
            ),
            Kpi(
                tr("kpi.default.label"),
                tr.eur(last["default"] - last["alternative"]),
                tr("kpi.default.help"),
                note=tr("kpi.default.note"),
            ),
        ]

    @param.depends("view_table", "error")
    def kpis(self) -> pn.viewable.Viewable:
        return super().kpis()

    @param.depends("view_table", "inputs.display")
    def figures(self) -> pn.viewable.Viewable:
        return super().figures()

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        if self.view_table is None:
            return []
        tr = self.tr
        figure = charts.member_wealth(self.view_table, tr, self.real)
        return [(figure, self._help("help.member_wealth"))]


class Mode3(_Page):
    """Admissible investment for a target rent, limited by rent and by the bank's equity rule."""

    rent_limit = param.Number(default=math.nan)
    bank_limit = param.Number(default=math.inf)
    investment = param.Number(default=math.nan)
    curve = param.Array(default=None, allow_None=True)

    levers = MODE3_LEVERS
    method_key = "method.mode3"

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        tr = self.tr
        p = self.inputs.to_project()
        lower = max(p.own_funds, MIN_INVESTMENT_EUR)

        def scenario_for(total: float) -> Scenario:
            return build_scenario(p.scaled_to(total))

        def rent_limit_at(rent: float) -> float:
            try:
                return max_investment(scenario_for, rent, lower)
            except ValueError:
                return math.nan

        target = self.inputs.target_rent
        if not is_affordable(scenario_for(lower), target):
            self._fail(
                tr("error.rent_too_low_for_own_funds", lower=tr.eur(lower), target=tr.eur(target))
            )
            return
        rent_limit = rent_limit_at(target)
        if math.isnan(rent_limit):
            self._fail(tr("error.no_upper_bound"))
            return
        min_share = self.inputs.min_equity_like_pct / 100
        bank_limit = p.equity_like / min_share if min_share > 0 else math.inf
        investment = min(rent_limit, bank_limit)
        if investment < lower:
            self._fail(tr("error.bank_rule_no_house"))
            return
        scenario = scenario_for(investment)
        self.param.update(
            rent_limit=rent_limit,
            bank_limit=bank_limit,
            investment=investment,
            scenario=scenario,
            result=simulate(scenario, target),
            capital=capital_structure(scenario, target),
            curve=np.array([rent_limit_at(r) for r in CURVE_RENTS_EUR_PERSON]),
            error="",
        )

    def _fail(self, message: str) -> None:
        super()._fail(message)
        self.param.update(investment=math.nan, curve=None)

    @param.depends("capital")
    def bank_status(self) -> pn.viewable.Viewable:
        return _bank_line(self.capital, self.tr) if self.capital else pn.Spacer(height=0)

    def kpi_items(self) -> list[Kpi]:
        tr = self.tr
        estimate = self.inputs.to_project().total_investment
        rent_binds = self.rent_limit <= self.bank_limit
        share = self.investment / estimate
        return [
            Kpi(
                tr("kpi.admissible.label"),
                tr.eur(self.investment),
                tr("kpi.admissible.help"),
                note=tr("kpi.admissible.by_rent" if rent_binds else "kpi.admissible.by_equity"),
                tone="good" if share >= 1 else "warning",
            ),
            Kpi(
                tr("kpi.share.label"),
                tr.pct(share),
                tr("kpi.share.help"),
                note=tr("kpi.share.note", estimate=tr.eur(estimate)),
            ),
            Kpi(tr("kpi.rent_limit.label"), tr.eur(self.rent_limit), tr("kpi.rent_limit.help")),
            Kpi(
                tr("kpi.bank_limit.label"),
                tr("kpi.bank_limit.none")
                if math.isinf(self.bank_limit)
                else tr.eur(self.bank_limit),
                tr("kpi.bank_limit.help"),
            ),
        ]

    @param.depends("investment", "error")
    def kpis(self) -> pn.viewable.Viewable:
        return super().kpis()

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        tr = self.tr
        curve = charts.investment_curve(
            CURVE_RENTS_EUR_PERSON,
            self.curve,
            self.bank_limit,
            self.inputs.target_rent,
            self.investment,
            tr,
        )
        return [
            (curve, tr("help.investment_curve")),
            (charts.liquidity(self.result, tr, self.real), self._help("help.liquidity_mode3")),
        ]


def _default_text(inputs: Inputs, name: str) -> str:
    tr = inputs.tr
    parameter = inputs.param[name]
    value = parameter.default
    if isinstance(parameter, param.Selector):
        names = getattr(parameter, "names", None) or {}
        return next((k for k, v in names.items() if v == value), str(value))
    if isinstance(value, float) and "(€" in parameter.label:
        return tr.eur(value)
    if isinstance(value, float):
        text = f"{value:g}"
        return text.replace(".", ",") if tr.decimal_comma else text
    return str(value)


def parameter_table(inputs: Inputs) -> str:
    """Markdown table of every input with its default and explanation."""
    tr = inputs.tr
    rows = []
    for key, names in {**SECTIONS, **ADVANCED_SECTIONS}.items():
        for name in names:
            label = inputs.param[name].label
            info = tr(f"info.{name}").replace("|", "/")
            section = tr(f"section.{key}")
            rows.append(f"| {section} | {label} | {_default_text(inputs, name)} | {info} |")
    return tr("methodik.table_header") + "\n|---|---|---|---|\n" + "\n".join(rows)


def methodik_page(inputs: Inputs) -> pn.viewable.Viewable:
    tr = inputs.tr
    return pn.Column(
        pn.pane.Markdown(tr.markdown("methodik"), max_width=1000),
        pn.pane.Markdown(tr("methodik.inputs_heading"), max_width=1000),
        pn.pane.Markdown(parameter_table(inputs), sizing_mode="stretch_width"),
        _on_demand(tr("assumptions.title"), assumptions_table(tr)),
        sizing_mode="stretch_width",
    )


def start_page(inputs: Inputs) -> pn.viewable.Viewable:
    tr = inputs.tr
    mode_tiles = [
        box(
            tr(f"nav.{key}"),
            pn.pane.Markdown(tr(f"start.{key}.question"), margin=(0, 0)),
            width=START_BOX_WIDTH,
        )
        for key in ("mode1", "mode2", "mode3")
    ]
    return pn.Column(
        pn.pane.Markdown(tr("start.intro"), max_width=1000, styles={"font-size": "15px"}),
        pn.FlexBox(*mode_tiles, sizing_mode="stretch_width"),
        pn.pane.HTML(
            f"<h3 style='margin:8px 0 4px 0'>{tr('start.heading')}</h3>",
            sizing_mode="stretch_width",
        ),
        inputs.all_inputs(),
        _on_demand(tr("assumptions.title"), assumptions_table(tr)),
        pn.pane.Markdown(tr("start.disclaimer"), max_width=1000, styles={"font-size": "13px"}),
        sizing_mode="stretch_width",
    )


# Compact buttons so that the navigation fits next to the title on laptop screens.
COMPACT_NAV_CSS = ".bk-btn { padding: 4px 8px; font-size: 13px; }"
# Shown in every language so that the choice can be found from any of them.
LANGUAGE_LABEL = "Sprache · Language · Taal"
# The template header carries the page navigation, so the tab bar itself is hidden.
HIDDEN_TAB_BAR_CSS = ":host > .bk-header { display: none; }"


class Dashboard:
    """All pages on one set of inputs; `render` rebuilds the views, e.g. after a language change."""

    def __init__(self, inputs: Inputs | None = None) -> None:
        pn.extension("plotly")
        self.inputs = inputs or Inputs()
        self.mode1 = Mode1(inputs=self.inputs)
        self.mode2 = Mode2(inputs=self.inputs)
        self.mode3 = Mode3(inputs=self.inputs)
        self.explore = ExplorationPage(inputs=self.inputs)
        self.tabs = pn.Tabs(sizing_mode="stretch_width", dynamic=True)
        self.render()

    def page_names(self) -> list[str]:
        return [self.inputs.tr(f"nav.{key}") for key in PAGE_KEYS]

    def render(self) -> None:
        active = self.tabs.active
        views = [
            start_page(self.inputs),
            self.mode1.view(),
            self.mode2.view(),
            self.mode3.view(),
            self.explore.view(),
            methodik_page(self.inputs),
        ]
        self.tabs[:] = list(zip(self.page_names(), views, strict=True))
        self.tabs.active = active


def build_app() -> pn.viewable.Viewable:
    return Dashboard().tabs


def serve() -> pn.template.BaseTemplate:
    """App in a template; the fixed header holds the page navigation, the language
    choice sits above the pages and scrolls away with them."""
    dashboard = Dashboard()
    inputs, tabs = dashboard.inputs, dashboard.tabs
    tabs.stylesheets = [HIDDEN_TAB_BAR_CSS]
    nav = pn.widgets.RadioButtonGroup(
        options={name: i for i, name in enumerate(dashboard.page_names())},
        value=0,
        color="light",
        variant="outline",
        margin=(8, 8),
        stylesheets=[COMPACT_NAV_CSS],
    )
    nav.link(tabs, value="active", bidirectional=True)
    language = pn.widgets.Select(
        label=LANGUAGE_LABEL,
        options={name: code for code, name in LANGUAGES.items()},
        value=inputs.language,
        width=200,
    )
    template = pn.template.FastListTemplate(
        title=inputs.tr("app.title"),
        header=[nav],
        main=[pn.Row(pn.HSpacer(), language, sizing_mode="stretch_width"), tabs],
        accent=ACCENT,
        header_background=ACCENT,
        theme_toggle=False,
        main_max_width="1500px",
    )

    def switch_language(event) -> None:
        inputs.language = event.new
        dashboard.render()
        page = nav.value
        nav.options = {name: i for i, name in enumerate(dashboard.page_names())}
        nav.value = page
        template.title = inputs.tr("app.title")

    language.param.watch(switch_language, "value")
    return template


if pn.state.served:
    serve().servable()
