"""Plotly figures for the dashboard pages.

Time series are shown in purchasing power of operating year 1, i.e. nominal
values divided by the inflation index relative to year 1.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from model import Result, Scenario
from model.cashflow import SENIOR_KINDS

TRANCHE_LABELS = {
    "equity": "Einlagen",
    "member_loan": "Mitgliederdarlehen",
    "direct_loan": "Direktkredite",
    "subsidy_loan": "Förderdarlehen",
    "bank_loan": "Bankdarlehen",
}
TRANCHE_NAME_LABELS = {
    "member_loans": "Mitgliederdarlehen",
    "direct_loans_5y": "Direktkredite 5 Jahre",
    "direct_loans_10y": "Direktkredite 10 Jahre",
}
SUBORDINATED_KINDS = ("member_loan", "direct_loan")
EUR_HOVER = "%{y:,.0f} €"

# Categorical slots in validated order (dataviz reference palette, light mode);
# each chart assigns them to its series in this order so adjacent marks stay
# distinguishable with colour-vision deficiencies.
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6")
NEUTRAL = "#8f8e89"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e8e7e3"
SURFACE = "#fcfcfb"
TRANCHE_COLORS = {
    "bank": SERIES[0],
    "subsidy": SERIES[1],
    "direct_loans_5y": SERIES[2],
    "direct_loans": SERIES[2],
    "direct_loans_10y": SERIES[3],
    "member_loans": SERIES[4],
}


def _deflator(result: Result) -> pd.Series:
    index = result.table["cost_index"]
    return index / index.loc[1]


def _real_title(result: Result, title: str) -> str:
    year = int(result.table["year"].loc[1])
    return f"{title}<br><sup>inflationsbereinigt, in Kaufkraft von {year} (Jahr 1)</sup>"


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


def _layout(fig: go.Figure, title: str, yaxis: str) -> go.Figure:
    fig.update_traces(hovertemplate=EUR_HOVER)
    fig.update_traces(line_width=2, selector={"mode": "lines"})
    fig.update_traces(marker_line={"color": SURFACE, "width": 1}, selector={"type": "bar"})
    axis = {"gridcolor": GRID, "zerolinecolor": GRID, "linecolor": GRID, "tickcolor": GRID}
    fig.update_layout(
        title={"text": title, "font": {"size": 16, "color": INK}, "x": 0, "xanchor": "left"},
        xaxis={"title": "Jahr", "tickformat": "d", "hoverformat": "d", **axis},
        yaxis={"title": yaxis, "tickformat": ",.0f", "ticksuffix": " €", **axis},
        font={"family": "system-ui, -apple-system, Segoe UI, sans-serif", "color": INK_SECONDARY},
        separators=",.",
        hovermode="x unified",
        bargap=0.25,
        legend={"orientation": "h", "y": -0.18, "x": 0},
        margin={"l": 70, "r": 20, "t": 80, "b": 40},
        height=420,
        plot_bgcolor=SURFACE,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def figure_table(fig: go.Figure) -> pd.DataFrame:
    """The plotted values as a table, one column per trace, rounded to whole euros."""
    columns = {
        trace.name: pd.Series(list(trace.y), index=list(trace.x))
        for trace in fig.data
        if trace.x is not None and len(trace.x) > 2
    }
    return pd.DataFrame(columns).round(0)


def _kinds(scenario: Scenario) -> dict[str, str]:
    return {tr.name: tr.kind for tr in scenario.tranches + scenario.member_tranches()}


def _label(name: str, kind: str) -> str:
    return TRANCHE_NAME_LABELS.get(name, TRANCHE_LABELS[kind])


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


def annual_costs(result: Result, scenario: Scenario) -> go.Figure:
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
        ("Betrieb inkl. Instandhaltungsrücklage", tab["operating"], NEUTRAL),
        (
            "Zinsen Bank und Förderung",
            _sum_by_kind(result, kinds, SENIOR_KINDS, "interest_paid"),
            SERIES[0],
        ),
        ("Tilgung Bank und Förderung", senior_repayment, SERIES[1]),
        (
            "Zinsen Direktkredite",
            _sum_by_kind(result, kinds, ("direct_loan",), "interest_paid"),
            SERIES[2],
        ),
        ("Zinsen Mitgliederdarlehen (bei Rückzahlung)", member_interest, SERIES[3]),
        ("Rückzahlung Direkt- und Mitgliederdarlehen (pünktlich)", sub_principal, SERIES[4]),
        (
            "Nachzahlung Rückstände inkl. Zinsen",
            tab["arrears_paid"] + tab["arrears_interest"],
            SERIES[5],
        ),
        ("Mietsenkung aus Überschuss", tab["rent_rebate"], SERIES[6]),
        ("Mietrückzahlung", tab["payout"], SERIES[6]),
        ("Solidartransfer", tab["transfer_out"], SERIES[6]),
    ]
    years = tab["year"].loc[1:]
    deflator = _deflator(result).loc[1:]
    fig = go.Figure()
    for label, values, color in series:
        values = values.loc[1:]
        if np.any(np.abs(values) > 0.5):
            fig.add_bar(x=years, y=values / deflator, name=label, marker_color=color)
    fig.add_scatter(
        x=years,
        y=tab["rent_income"].loc[1:] / deflator,
        name="Mieteinnahmen",
        mode="lines",
        line_color=INK,
    )
    fig.update_layout(barmode="stack")
    return _layout(fig, _real_title(result, "Jährliche Ausgaben und Mieteinnahmen"), "pro Jahr")


def arrears(result: Result) -> go.Figure:
    """Repayments not made on the due date and the open arrears per year."""
    tab = result.table.loc[1:]
    deflator = _deflator(result).loc[1:]
    fig = go.Figure()
    fig.add_bar(
        x=tab["year"],
        y=tab["arrears_new"] / deflator,
        name="Am Fälligkeitstag nicht zurückgezahlt",
        marker_color=SERIES[1],
    )
    fig.add_scatter(
        x=tab["year"],
        y=tab["arrears"] / deflator,
        name="Offener Rückstand zum Jahresende",
        mode="lines",
        line_color=INK,
    )
    return _layout(
        fig,
        _real_title(result, "Nicht pünktlich zurückgezahlte Direkt- und Mitgliederdarlehen"),
        "",
    )


def debt_balances(result: Result, scenario: Scenario) -> go.Figure:
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
        fig.add_scatter(x=years, y=real, name=_label(name, kind), mode="lines", line_color=color)
    if result.table["arrears"].any():
        open_arrears = result.table["arrears"] / deflator
        total = total + open_arrears
        fig.add_scatter(
            x=years, y=open_arrears, name="Rückstände", mode="lines", line_color=SERIES[6]
        )
    fig.add_scatter(
        x=years, y=total, name="Summe", mode="lines", line={"dash": "dash", "color": INK}
    )
    return _layout(fig, _real_title(result, "Restschuld zum Jahresende"), "")


def liquidity(result: Result) -> go.Figure:
    """Account balance against the required minimum reserve."""
    tab = result.table.loc[1:]
    deflator = _deflator(result).loc[1:]
    fig = go.Figure()
    fig.add_scatter(
        x=tab["year"],
        y=tab["liquidity"] / deflator,
        name="Liquidität",
        mode="lines",
        line_color=SERIES[0],
    )
    fig.add_scatter(
        x=tab["year"],
        y=tab["reserve_required"] / deflator,
        name="Mindestreserve",
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    if tab["maintenance_reserve"].any():
        fig.add_scatter(
            x=tab["year"],
            y=tab["maintenance_reserve"] / deflator,
            name="Instandhaltungsrücklage (eigener Topf)",
            mode="lines",
            line={"dash": "dot", "color": SERIES[1]},
        )
    return _layout(fig, _real_title(result, "Liquidität und Rücklage"), "")


def member_wealth(view: pd.DataFrame) -> go.Figure:
    """A member's wealth in the project against the market-rent alternative."""
    year1 = int(view["year"].iloc[0] - view.index[0] + 1)
    fig = go.Figure()
    fig.add_scatter(
        x=view["year"], y=view["project"], name="Im Projekt", mode="lines", line_color=SERIES[0]
    )
    fig.add_scatter(
        x=view["year"],
        y=view["alternative"],
        name="Marktmiete + Geld angelegt",
        mode="lines",
        line_color=SERIES[1],
    )
    fig.add_scatter(
        x=view["year"],
        y=view["default"],
        name="Im Projekt, Einlage und Darlehen verloren",
        mode="lines",
        line={"dash": "dash", "color": NEUTRAL},
    )
    title = (
        "Vermögen des Mitglieds<br><sup>inflationsbereinigt, in Kaufkraft von "
        f"{year1} (Jahr 1)</sup>"
    )
    return _layout(fig, title, "")


def investment_curve(
    rents: np.ndarray,
    rent_limited: np.ndarray,
    bank_limit: float,
    target_rent: float,
    investment: float,
) -> go.Figure:
    """Admissible investment against target rent, with the bank's equity limit as a cap."""
    fig = go.Figure()
    fig.add_scatter(
        x=rents, y=rent_limited, name="Grenze durch Zielmiete", mode="lines", line_color=SERIES[0]
    )
    if not math.isinf(bank_limit):
        fig.add_scatter(
            x=[rents[0], rents[-1]],
            y=[bank_limit, bank_limit],
            name="Grenze durch Eigenkapitalanforderung",
            mode="lines",
            line={"dash": "dash", "color": SERIES[1]},
        )
    fig.add_scatter(
        x=[target_rent],
        y=[investment],
        name="Zulässig bei Zielmiete",
        mode="markers",
        marker={"size": 12, "color": INK, "line": {"color": SURFACE, "width": 2}},
    )
    _layout(fig, "Zulässige Investition je nach Zielmiete<br><sup>Preise von heute</sup>", "")
    fig.update_traces(hovertemplate="Zielmiete %{x:,.0f} €<br>Investition " + EUR_HOVER)
    fig.update_layout(
        xaxis={
            "title": "Zielmiete (€ pro Person/Monat)",
            "tickformat": ",.0f",
            "ticksuffix": " €",
            "hoverformat": ",.0f",
        },
        hovermode="closest",
    )
    return fig
