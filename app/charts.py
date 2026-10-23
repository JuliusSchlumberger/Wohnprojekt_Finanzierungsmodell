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

from app.i18n import Translator
from model import Result, Scenario
from model.cashflow import SENIOR_KINDS

GERMAN = Translator("de")
NAMED_TRANCHES = ("direct_loans_5y", "direct_loans_10y")
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
}
UNCERTAIN_INPUTS = (
    "inflation",
    "bank_rate_change_pp",
    "vacancy_rate",
    "renovation_factor",
    "running_cost_factor",
    "member_loan_term_years",
    "member_loan_factor",
    "direct_loans_10y_factor",
)


def _deflator(result: Result) -> pd.Series:
    index = result.table["cost_index"]
    return index / index.loc[1]


def _real_title(title: str, year: int, tr: Translator) -> str:
    return f"{title}<br><sup>{tr('chart.real_subtitle', year=year)}</sup>"


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


def annual_costs(result: Result, scenario: Scenario, tr: Translator = GERMAN) -> go.Figure:
    """Stacked yearly cash outflows with rent income as a line.

    Interest is split by lender; member-loan interest shows when it is paid
    out with the loan. Direct and member loan repayments are split into the
    part paid on the due date and later payments of arrears.
    """
    tab = result.table
    kinds = _kinds(scenario)
    due = tab["sub_due"]
    on_time_share = (tab["sub_paid_on_time"] / due).where(due > 0, 0.0)
    member_interest = on_time_share * _accrued_interest_due(result, kinds)
    sub_principal = tab["sub_paid_on_time"] - member_interest
    senior_repayment = (
        tab["repayment"] - tab["loan_inflow"] - tab["sub_paid_on_time"] - tab["arrears_paid"]
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
        ("transfer", tab["transfer_out"], SERIES[6]),
    ]
    years = tab["year"].loc[1:]
    deflator = _deflator(result).loc[1:]
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
    fig.update_layout(barmode="stack")
    title = _real_title(tr("chart.costs.title"), int(tab["year"].loc[1]), tr)
    return _layout(fig, title, tr("chart.costs.y"), tr)


def arrears(result: Result, tr: Translator = GERMAN) -> go.Figure:
    """Repayments not made on the due date and the open arrears per year."""
    tab = result.table.loc[1:]
    deflator = _deflator(result).loc[1:]
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
    title = _real_title(tr("chart.arrears.title"), int(tab["year"].iloc[0]), tr)
    return _layout(fig, title, "", tr)


def debt_balances(result: Result, scenario: Scenario, tr: Translator = GERMAN) -> go.Figure:
    """Outstanding debt per loan tranche at year end and in total; member equity is omitted."""
    kinds = _kinds(scenario)
    years = result.table["year"]
    deflator = _deflator(result)
    fig = go.Figure()
    total = 0.0
    for name, schedule in result.tranches.items():
        kind = kinds[name]
        if kind == "equity" or not schedule["balance"].any():
            continue
        real = schedule["balance"] / deflator
        total = total + real
        color = TRANCHE_COLORS.get(name, NEUTRAL)
        fig.add_scatter(
            x=years, y=real, name=_label(name, kind, tr), mode="lines", line_color=color
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
    title = _real_title(tr("chart.debt.title"), int(years.loc[1]), tr)
    return _layout(fig, title, "", tr)


def liquidity(result: Result, tr: Translator = GERMAN) -> go.Figure:
    """Account balance against the required minimum reserve."""
    tab = result.table.loc[1:]
    deflator = _deflator(result).loc[1:]
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
    title = _real_title(tr("chart.liquidity.title"), int(tab["year"].iloc[0]), tr)
    return _layout(fig, title, "", tr)


def member_wealth(view: pd.DataFrame, tr: Translator = GERMAN) -> go.Figure:
    """A member's wealth in the project against the market-rent alternative."""
    year1 = int(view["year"].iloc[0] - view.index[0] + 1)
    fig = go.Figure()
    fig.add_scatter(
        x=view["year"],
        y=view["project"],
        name=tr("chart.member.project"),
        mode="lines",
        line_color=SERIES[0],
    )
    fig.add_scatter(
        x=view["year"],
        y=view["alternative"],
        name=tr("chart.member.market"),
        mode="lines",
        line_color=SERIES[1],
    )
    fig.add_scatter(
        x=view["year"],
        y=view["default"],
        name=tr("chart.member.default"),
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    return _layout(fig, _real_title(tr("chart.member.title"), year1, tr), "", tr)


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


def rent_distribution(
    rents: pd.Series, base_rent: float, median: float, safe_rent: float, tr: Translator = GERMAN
) -> go.Figure:
    """How often each required rent occurs across the sampled variants."""
    counts, edges = np.histogram(rents.dropna(), bins=20)
    centers = 0.5 * (edges[:-1] + edges[1:])
    fig = go.Figure()
    fig.add_bar(x=centers, y=counts, name=tr("chart.dist.count"), marker_color=SERIES[0])
    top = counts.max() * 1.1
    for value, key, color, dash in [
        (base_rent, "base", NEUTRAL, "dot"),
        (median, "median", INK, "solid"),
        (safe_rent, "safe", SERIES[1], "dash"),
    ]:
        fig.add_scatter(
            x=[value, value],
            y=[0, top],
            name=tr(f"chart.dist.{key}"),
            mode="lines",
            line={"color": color, "dash": dash},
        )
    _layout(fig, tr("chart.dist.title"), tr("chart.dist.count"), tr)
    fig.update_traces(
        hovertemplate=f"{tr.eur_hover('x')}: %{{y}} {tr('chart.dist.hover_variants')}",
        selector={"type": "bar"},
    )
    fig.update_traces(hovertemplate=tr.eur_hover("x", 2), selector={"mode": "lines"})
    fig.update_layout(
        xaxis=_rent_axis(tr("chart.dist.x"), tr),
        yaxis={"tickprefix": "", "ticksuffix": "", "tickformat": "d"},
        hovermode="closest",
        bargap=0.05,
    )
    return fig


def headroom_band(band: pd.DataFrame, tr: Translator = GERMAN) -> go.Figure:
    """Liquidity above the minimum reserve at the safe rent: median and 10-90 % band."""
    upper, middle = tr("chart.band.p90"), tr("chart.band.band")
    fig = go.Figure()
    fig.add_scatter(
        x=band["year"],
        y=band["p90"],
        name=upper,
        mode="lines",
        line={"color": SERIES[0], "width": 0},
        showlegend=False,
    )
    fig.add_scatter(
        x=band["year"],
        y=band["p10"],
        name=middle,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(42, 120, 214, 0.18)",
        line={"color": SERIES[0], "width": 0},
    )
    fig.add_scatter(
        x=band["year"],
        y=band["p50"],
        name=tr("chart.band.median"),
        mode="lines",
        line_color=SERIES[0],
    )
    fig.add_scatter(
        x=band["year"],
        y=0 * band["p50"],
        name=tr("chart.band.reserve"),
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    title = _real_title(tr("chart.band.title"), int(band["year"].iloc[0]), tr)
    fig = _layout(fig, title, "", tr)
    fig.update_traces(line_width=0, selector={"name": middle})
    fig.update_traces(line_width=0, selector={"name": upper})
    return fig


def sensitivity(correlations: pd.Series, tr: Translator = GERMAN) -> go.Figure:
    """Rank correlation of each uncertain input with the required rent."""
    labels = [
        tr(f"chart.uncertain.{k}") if k in UNCERTAIN_INPUTS else k for k in correlations.index
    ]
    colors = [SERIES[0] if v >= 0 else DIVERGING_NEGATIVE for v in correlations]
    fig = go.Figure()
    fig.add_bar(
        x=labels, y=correlations.to_numpy(), name=tr("chart.sens.name"), marker_color=colors
    )
    _layout(fig, tr("chart.sens.title"), tr("chart.sens.y"), tr)
    fig.update_traces(hovertemplate="%{x}: %{y:.2f}")
    fig.update_layout(
        xaxis={"title": "", "tickformat": None, "hoverformat": None},
        yaxis={"tickprefix": "", "ticksuffix": "", "tickformat": ".1f", "range": [-1, 1]},
        hovermode="closest",
        showlegend=False,
    )
    return fig
