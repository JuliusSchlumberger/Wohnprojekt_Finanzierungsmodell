"""Plotly figures for the dashboard pages.

Time series are shown in purchasing power of operating year 1, i.e. nominal
values divided by the inflation index relative to year 1. Every figure takes
a `Translator` for its texts and number format.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.i18n import Translator
from model import Result, Scenario
from model.cashflow import SENIOR_KINDS

GERMAN = Translator("de")
REFINANCE_TRANCHES = ("bank_refinance", "direct_loans_refinance")
NAMED_TRANCHES = ("direct_loans_5y", "direct_loans_10y", *REFINANCE_TRANCHES)
SUBORDINATED_KINDS = ("member_loan", "direct_loan")

# Categorical slots in validated order (dataviz reference palette, light mode);
# each chart assigns them to its series in this order so adjacent marks stay
# distinguishable with colour-vision deficiencies.
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6")
NEUTRAL = "#8f8e89"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e8e7e3"
SURFACE = "#fcfcfb"
DIVERGING_NEGATIVE = "#e34948"
TRANCHE_COLORS = {
    "bank": SERIES[0],
    "subsidy": SERIES[1],
    "direct_loans_5y": SERIES[2],
    "direct_loans": SERIES[2],
    "direct_loans_10y": SERIES[3],
    "member_loans": SERIES[4],
    "bank_refinance": SERIES[5],
    "direct_loans_refinance": SERIES[5],
}
SEQUENTIAL = [
    [0.0, "#cde2fb"],
    [0.25, "#86b6ef"],
    [0.5, "#3987e5"],
    [0.75, "#1c5cab"],
    [1.0, "#0d366b"],
]
# Sampled parameters stored as fractions and shown in percent.
EXPLORE_PERCENT = {
    "vacancy_rate": 100.0,
    "member_loan_share": 100.0,
    "direct_loans_10y_share": 100.0,
}
EXPLORE_COLUMNS = 4


def _deflator(result: Result, real: bool = True) -> pd.Series:
    """Divisor that turns nominal amounts into the shown unit (1 when nominal)."""
    index = result.table["cost_index"]
    return index / index.loc[1] if real else index * 0 + 1.0


def _title(title: str, year: int, tr: Translator, real: bool = True) -> str:
    subtitle = tr("chart.real_subtitle" if real else "chart.nominal_subtitle", year=year)
    return f"{title}<br><sup>{subtitle}</sup>"


def subordinated_debt_real(result: Result, scenario: Scenario) -> pd.Series:
    """Outstanding direct and member loans incl. arrears, in purchasing power of year 1."""
    kinds = _kinds(scenario)
    nominal = sum(
        (
            df["balance"]
            for name, df in result.tranches.items()
            if kinds[name] in SUBORDINATED_KINDS
        ),
        start=result.table["arrears"].copy(),
    )
    return nominal / _deflator(result)


def _layout(fig: go.Figure, title: str, yaxis: str, tr: Translator) -> go.Figure:
    prefix, suffix = tr.currency_affixes
    fig.update_traces(hovertemplate=tr.eur_hover("y"))
    fig.update_traces(line_width=2, selector={"mode": "lines"})
    fig.update_traces(marker_line={"color": SURFACE, "width": 1}, selector={"type": "bar"})
    axis = {"gridcolor": GRID, "zerolinecolor": GRID, "linecolor": GRID, "tickcolor": GRID}
    fig.update_layout(
        title={"text": title, "font": {"size": 16, "color": INK}, "x": 0, "xanchor": "left"},
        xaxis={"title": tr("ui.year"), "tickformat": "d", "hoverformat": "d", **axis},
        yaxis={
            "title": yaxis,
            "tickformat": ",.0f",
            "tickprefix": prefix,
            "ticksuffix": suffix,
            **axis,
        },
        font={"family": "system-ui, -apple-system, Segoe UI, sans-serif", "color": INK_SECONDARY},
        separators=tr.plotly_separators,
        hovermode="x unified",
        bargap=0.25,
        legend={"orientation": "h", "y": -0.18, "x": 0},
        margin={"l": 70, "r": 20, "t": 80, "b": 40},
        height=420,
        plot_bgcolor=SURFACE,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def _rent_axis(title: str, tr: Translator) -> dict:
    prefix, suffix = tr.currency_affixes
    return {
        "title": title,
        "tickformat": ",.0f",
        "tickprefix": prefix,
        "ticksuffix": suffix,
        "hoverformat": ",.0f",
    }


def figure_table(fig: go.Figure) -> pd.DataFrame:
    """The plotted values as a table, one column per trace."""
    columns = {
        trace.name: pd.Series(list(trace.y), index=list(trace.x))
        for trace in fig.data
        if trace.x is not None and len(trace.x) > 2
    }
    return pd.DataFrame(columns)


def _kinds(scenario: Scenario) -> dict[str, str]:
    return {tr.name: tr.kind for tr in scenario.tranches + scenario.member_tranches()}


def _label(name: str, kind: str, tr: Translator) -> str:
    return tr(f"chart.tranche.{name if name in NAMED_TRANCHES else kind}")


def _sum_by_kind(result: Result, kinds: dict[str, str], wanted: tuple[str, ...], column: str):
    return sum(
        (df[column] for name, df in result.tranches.items() if kinds[name] in wanted),
        start=pd.Series(0.0, index=result.table.index),
    )


def _accrued_interest_due(result: Result, kinds: dict[str, str]) -> pd.Series:
    """Interest content of member-loan repayments due, assuming bullet repayment."""
    content = pd.Series(0.0, index=result.table.index)
    for name, df in result.tranches.items():
        if kinds[name] != "member_loan":
            continue
        accrued = df["interest"].cumsum()
        principal = df["balance"].iloc[0] + df["inflow"].sum()
        content += df["repayment"] * accrued / (principal + accrued).where(lambda x: x > 0, 1.0)
    return content


def annual_costs(
    result: Result, scenario: Scenario, tr: Translator = GERMAN, real: bool = True
) -> go.Figure:
    """Stacked yearly cash outflows with rent income as a line.

    Interest is split by lender; member-loan interest shows when it is paid
    out with the loan. Direct and member loan repayments are split into the
    part paid on the due date and later payments of arrears. A new loan that
    pays off the member loans shows as a negative bar in its drawdown year.
    """
    tab = result.table
    kinds = _kinds(scenario)
    due = tab["sub_due"]
    on_time_share = (tab["sub_paid_on_time"] / due).where(due > 0, 0.0)
    member_interest = on_time_share * _accrued_interest_due(result, kinds)
    sub_principal = tab["sub_paid_on_time"] - member_interest
    refinancing = sum(
        (result.tranches[name]["inflow"] for name in REFINANCE_TRANCHES if name in result.tranches),
        start=0.0 * due,
    )
    senior_repayment = (
        tab["repayment"]
        - tab["loan_inflow"]
        + refinancing
        - tab["sub_paid_on_time"]
        - tab["arrears_paid"]
    )
    series = [
        ("operating", tab["operating"], NEUTRAL),
        (
            "senior_interest",
            _sum_by_kind(result, kinds, SENIOR_KINDS, "interest_paid"),
            SERIES[0],
        ),
        ("senior_repayment", senior_repayment, SERIES[1]),
        (
            "direct_interest",
            _sum_by_kind(result, kinds, ("direct_loan",), "interest_paid"),
            SERIES[2],
        ),
        ("member_interest", member_interest, SERIES[3]),
        ("sub_repayment", sub_principal, SERIES[4]),
        ("arrears", tab["arrears_paid"] + tab["arrears_interest"], SERIES[5]),
        ("rebate", tab["rent_rebate"], SERIES[6]),
        ("payout", tab["payout"], SERIES[6]),
        ("refinancing", -refinancing, SERIES[5]),
        ("transfer", tab["transfer_out"], SERIES[6]),
    ]
    years = tab["year"].loc[1:]
    deflator = _deflator(result, real).loc[1:]
    fig = go.Figure()
    for key, values, color in series:
        values = values.loc[1:]
        if np.any(np.abs(values) > 0.5):
            fig.add_bar(
                x=years, y=values / deflator, name=tr(f"chart.costs.{key}"), marker_color=color
            )
    fig.add_scatter(
        x=years,
        y=tab["rent_income"].loc[1:] / deflator,
        name=tr("chart.costs.rent_income"),
        mode="lines",
        line_color=INK,
    )
    fig.update_layout(barmode="relative")
    title = _title(tr("chart.costs.title"), int(tab["year"].loc[1]), tr, real)
    return _layout(fig, title, tr("chart.costs.y"), tr)


def arrears(result: Result, tr: Translator = GERMAN, real: bool = True) -> go.Figure:
    """Repayments not made on the due date and the open arrears per year."""
    tab = result.table.loc[1:]
    deflator = _deflator(result, real).loc[1:]
    fig = go.Figure()
    fig.add_bar(
        x=tab["year"],
        y=tab["arrears_new"] / deflator,
        name=tr("chart.arrears.new"),
        marker_color=SERIES[1],
    )
    fig.add_scatter(
        x=tab["year"],
        y=tab["arrears"] / deflator,
        name=tr("chart.arrears.open"),
        mode="lines",
        line_color=INK,
    )
    title = _title(tr("chart.arrears.title"), int(tab["year"].iloc[0]), tr, real)
    return _layout(fig, title, "", tr)


def debt_balances(
    result: Result, scenario: Scenario, tr: Translator = GERMAN, real: bool = True
) -> go.Figure:
    """Outstanding debt per loan tranche at year end and in total; member equity is omitted."""
    kinds = _kinds(scenario)
    years = result.table["year"]
    deflator = _deflator(result, real)
    fig = go.Figure()
    total = 0.0
    for name, schedule in result.tranches.items():
        kind = kinds[name]
        if kind == "equity" or not schedule["balance"].any():
            continue
        balance = schedule["balance"] / deflator
        total = total + balance
        color = TRANCHE_COLORS.get(name, NEUTRAL)
        fig.add_scatter(
            x=years, y=balance, name=_label(name, kind, tr), mode="lines", line_color=color
        )
    if result.table["arrears"].any():
        open_arrears = result.table["arrears"] / deflator
        total = total + open_arrears
        fig.add_scatter(
            x=years,
            y=open_arrears,
            name=tr("chart.debt.arrears"),
            mode="lines",
            line_color=SERIES[6],
        )
    fig.add_scatter(
        x=years,
        y=total,
        name=tr("chart.debt.total"),
        mode="lines",
        line={"dash": "dash", "color": INK},
    )
    title = _title(tr("chart.debt.title"), int(years.loc[1]), tr, real)
    return _layout(fig, title, "", tr)


def liquidity(result: Result, tr: Translator = GERMAN, real: bool = True) -> go.Figure:
    """Account balance against the required minimum reserve."""
    tab = result.table.loc[1:]
    deflator = _deflator(result, real).loc[1:]
    fig = go.Figure()
    fig.add_scatter(
        x=tab["year"],
        y=tab["liquidity"] / deflator,
        name=tr("chart.liquidity.liquidity"),
        mode="lines",
        line_color=SERIES[0],
    )
    fig.add_scatter(
        x=tab["year"],
        y=tab["reserve_required"] / deflator,
        name=tr("chart.liquidity.reserve"),
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    if tab["maintenance_reserve"].any():
        fig.add_scatter(
            x=tab["year"],
            y=tab["maintenance_reserve"] / deflator,
            name=tr("chart.liquidity.maintenance"),
            mode="lines",
            line={"dash": "dot", "color": SERIES[1]},
        )
    title = _title(tr("chart.liquidity.title"), int(tab["year"].iloc[0]), tr, real)
    return _layout(fig, title, "", tr)


def member_wealth(view: pd.DataFrame, tr: Translator = GERMAN, real: bool = True) -> go.Figure:
    """A member's wealth in the project against the market-rent alternative."""
    year1 = int(view["year"].iloc[0] - view.index[0] + 1)
    scale = 1.0 if real else view["deflator"]
    fig = go.Figure()
    fig.add_scatter(
        x=view["year"],
        y=view["project"] * scale,
        name=tr("chart.member.project"),
        mode="lines",
        line_color=SERIES[0],
    )
    fig.add_scatter(
        x=view["year"],
        y=view["alternative"] * scale,
        name=tr("chart.member.market"),
        mode="lines",
        line_color=SERIES[1],
    )
    fig.add_scatter(
        x=view["year"],
        y=view["default"] * scale,
        name=tr("chart.member.default"),
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    return _layout(fig, _title(tr("chart.member.title"), year1, tr, real), "", tr)


def investment_curve(
    rents: np.ndarray,
    rent_limited: np.ndarray,
    bank_limit: float,
    target_rent: float,
    investment: float,
    tr: Translator = GERMAN,
) -> go.Figure:
    """Admissible investment against target rent, with the bank's equity limit as a cap."""
    fig = go.Figure()
    fig.add_scatter(
        x=rents,
        y=rent_limited,
        name=tr("chart.curve.rent_limit"),
        mode="lines",
        line_color=SERIES[0],
    )
    if not math.isinf(bank_limit):
        fig.add_scatter(
            x=[rents[0], rents[-1]],
            y=[bank_limit, bank_limit],
            name=tr("chart.curve.bank_limit"),
            mode="lines",
            line={"dash": "dash", "color": SERIES[1]},
        )
    fig.add_scatter(
        x=[target_rent],
        y=[investment],
        name=tr("chart.curve.point"),
        mode="markers",
        marker={"size": 12, "color": INK, "line": {"color": SURFACE, "width": 2}},
    )
    title = f"{tr('chart.curve.title')}<br><sup>{tr('chart.curve.subtitle')}</sup>"
    _layout(fig, title, "", tr)
    fig.update_traces(
        hovertemplate=f"{tr('chart.curve.hover_rent')} {tr.eur_hover('x')}<br>"
        f"{tr('chart.curve.hover_investment')} {tr.eur_hover('y')}"
    )
    fig.update_layout(xaxis=_rent_axis(tr("chart.curve.x"), tr), hovermode="closest")
    return fig


def explore_value(name: str, value: float) -> float:
    """A sampled parameter in its display unit (shares and rates in %)."""
    return value * EXPLORE_PERCENT.get(name, 1.0)


def _explore_axes(fig: go.Figure, tr: Translator, title: str, height: int) -> go.Figure:
    axis = {"gridcolor": GRID, "zerolinecolor": GRID, "linecolor": GRID, "tickcolor": GRID}
    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)
    fig.update_layout(
        title={"text": title, "font": {"size": 16, "color": INK}, "x": 0, "xanchor": "left"},
        font={"family": "system-ui, -apple-system, Segoe UI, sans-serif", "color": INK_SECONDARY},
        separators=tr.plotly_separators,
        legend={"orientation": "h", "y": -0.12, "x": 0},
        margin={"l": 70, "r": 20, "t": 90, "b": 40},
        height=height,
        plot_bgcolor=SURFACE,
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="closest",
    )
    fig.update_annotations(font={"size": 12, "color": INK_SECONDARY})
    return fig


def _grid(names: list[str], tr: Translator, **kwargs):
    rows = math.ceil(len(names) / EXPLORE_COLUMNS)
    titles = [tr(f"explore.param.{n}") for n in names]
    return make_subplots(
        rows=rows,
        cols=EXPLORE_COLUMNS,
        subplot_titles=titles,
        horizontal_spacing=0.06,
        vertical_spacing=0.16,
        **kwargs,
    )


def importance(table: pd.DataFrame, tr: Translator = GERMAN) -> go.Figure:
    """Share of the rent's spread each input explains alone, split linear / non-linear."""
    labels = [tr(f"explore.param.{n}") for n in table.index]
    fig = go.Figure()
    for key, values, color in [
        ("linear", table["linear"], SERIES[0]),
        ("nonlinear", table["total"] - table["linear"], SERIES[1]),
    ]:
        fig.add_bar(
            y=labels,
            x=100 * values.to_numpy(),
            name=tr(f"chart.explore.importance.{key}"),
            orientation="h",
            marker={"color": color, "line": {"color": SURFACE, "width": 1}},
            hovertemplate="%{y}: %{x:.1f} %<extra></extra>",
        )
    _explore_axes(fig, tr, tr("chart.explore.importance.title"), 420)
    fig.update_layout(
        barmode="stack",
        bargap=0.3,
        xaxis={"title": tr("chart.explore.importance.x"), "ticksuffix": " %"},
        yaxis={"autorange": "reversed"},
        margin={"l": 260},
    )
    return fig


def parameter_effects(per_parameter: dict, tr: Translator = GERMAN) -> go.Figure:
    """Required rent against each input: 10-90 % band, median and lowest reachable rent."""
    names = list(per_parameter)
    fig = _grid(names, tr, shared_yaxes=True)
    for i, name in enumerate(names):
        row, col = divmod(i, EXPLORE_COLUMNS)
        data = per_parameter[name]
        x = [explore_value(name, v) for v in data["x"]]
        first = i == 0
        cell = {"row": row + 1, "col": col + 1}
        fig.add_scatter(
            x=x,
            y=data["p90"],
            mode="lines",
            line={"width": 0, "color": SERIES[0]},
            showlegend=False,
            hoverinfo="skip",
            **cell,
        )
        fig.add_scatter(
            x=x,
            y=data["p10"],
            mode="lines",
            line={"width": 0, "color": SERIES[0]},
            fill="tonexty",
            fillcolor="rgba(42, 120, 214, 0.18)",
            name=tr("chart.explore.effects.band"),
            legendgroup="band",
            showlegend=first,
            hoverinfo="skip",
            **cell,
        )
        for key, color, dash in [("p50", SERIES[0], "solid"), ("min", SERIES[1], "dot")]:
            fig.add_scatter(
                x=x,
                y=data[key],
                mode="lines+markers" if key == "min" else "lines",
                line={"color": color, "width": 2, "dash": dash},
                marker={"size": 4},
                name=tr(f"chart.explore.effects.{key}"),
                legendgroup=key,
                showlegend=first,
                hovertemplate=f"%{{x:.1f}}: {tr.eur_hover('y')}<extra></extra>",
                **cell,
            )
    prefix, suffix = tr.currency_affixes
    fig.update_yaxes(tickformat=",.0f", tickprefix=prefix, ticksuffix=suffix)
    return _explore_axes(fig, tr, tr("chart.explore.effects.title"), 640)


def pair_heatmap(pair: dict, x_name: str, y_name: str, tr: Translator = GERMAN) -> go.Figure:
    """Median required rent over a grid of two inputs."""
    z = np.array(pair["z"], dtype=float).T
    prefix, suffix = tr.currency_affixes
    fig = go.Figure(
        go.Heatmap(
            x=[explore_value(x_name, v) for v in pair["x"]],
            y=[explore_value(y_name, v) for v in pair["y"]],
            z=z,
            colorscale=SEQUENTIAL,
            colorbar={
                "title": tr("chart.explore.pair.colorbar"),
                "tickformat": ",.0f",
                "tickprefix": prefix,
                "ticksuffix": suffix,
            },
            hovertemplate=(
                f"{tr(f'explore.param.{x_name}')}: %{{x:.1f}}<br>"
                f"{tr(f'explore.param.{y_name}')}: %{{y:.1f}}<br>"
                f"{tr('chart.explore.pair.colorbar')}: {tr.eur_hover('z')}<extra></extra>"
            ),
        )
    )
    _explore_axes(fig, tr, tr("chart.explore.pair.title"), 480)
    fig.update_layout(
        xaxis={"title": tr(f"explore.param.{x_name}")},
        yaxis={"title": tr(f"explore.param.{y_name}")},
    )
    return fig


def cheapest_profile(cheapest: dict, tr: Translator = GERMAN) -> go.Figure:
    """Per input: how all variants and the cheapest ones are spread over its range."""
    names = list(cheapest)
    fig = _grid(names, tr)
    for i, name in enumerate(names):
        row, col = divmod(i, EXPLORE_COLUMNS)
        data = cheapest[name]
        x = [explore_value(name, v) for v in data["x"]]
        for key, color in [("all", NEUTRAL), ("cheapest", SERIES[0])]:
            fig.add_bar(
                x=x,
                y=[100 * v for v in data[key]],
                marker_color=color,
                name=tr(f"chart.explore.cheapest.{key}"),
                legendgroup=key,
                showlegend=i == 0,
                hovertemplate="%{x:.1f}: %{y:.1f} %<extra></extra>",
                row=row + 1,
                col=col + 1,
            )
    fig.update_yaxes(ticksuffix=" %")
    fig.update_layout(barmode="group", bargap=0.15, bargroupgap=0.05)
    return _explore_axes(fig, tr, tr("chart.explore.cheapest.title"), 640)
