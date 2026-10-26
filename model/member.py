"""Mode 2: one member's wealth in the project versus paying market rent; see `member_view`."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from model.cashflow import Result
from model.types import Scenario


@dataclass(frozen=True)
class MemberInputs:
    """One member's capital and comparison assumptions.

    `equity` is in money of year 0 and is paid in and repaid inflation-indexed
    (A5). `member_loan` is lent at entry, accrues `member_loan_rate` and is
    repaid after `member_loan_term_years` or in the year after exit, whichever
    comes first.
    `market_rent` is EUR per month in the unit of the project rent input and
    is indexed like it.
    `alt_return` is the nominal yearly return on money invested elsewhere.
    """

    equity: float = 2_000.0
    member_loan: float = 20_000.0
    member_loan_rate: float = 0.055
    member_loan_term_years: int = 15
    entry_year: int = 0
    exit_year: int = 20
    market_rent: float = 800.0
    alt_return: float = 0.055


def member_view(scenario: Scenario, result: Result, m: MemberInputs) -> pd.DataFrame:
    """Yearly wealth of a member versus the market-rent alternative, in money of year 1.

    Project path: every payment to the member (rent saved against market
    rent, rent payouts, repaid member loan and equity) is invested at
    `alt_return`; the member's equity and outstanding loan count as wealth
    while held. Alternative path: equity and loan amount are invested at
    `alt_return` instead and market rent is paid. The default path is the
    project path with equity and loan lost. Rows run from entry to the year
    after exit, or to the horizon; multiplying by `deflator` gives nominal euros.
    """
    horizon = scenario.horizon_years
    if not 0 <= m.entry_year < m.exit_year <= horizon:
        raise ValueError("need 0 <= entry_year < exit_year <= horizon")
    tab = result.table
    cidx = tab["cost_index"].to_numpy()
    end = min(m.exit_year + 1, horizon)
    years = np.arange(m.entry_year, end + 1)

    project_rent = 12 * tab["rent_per_person"].fillna(0.0).to_numpy()
    market_rent = 12 * m.market_rent * cidx
    payout = tab["payout"].to_numpy() / scenario.persons
    loan_due = min(m.entry_year + m.member_loan_term_years, m.exit_year + 1)

    equity_in = m.equity * cidx[m.entry_year]
    invested = default = 0.0
    alternative = equity_in + m.member_loan
    rows = []
    for t in years:
        if t > m.entry_year:
            invested *= 1 + m.alt_return
            default *= 1 + m.alt_return
            alternative *= 1 + m.alt_return
        resident = m.entry_year < t <= m.exit_year
        saving = market_rent[t] - project_rent[t] if resident else 0.0
        payout_share = payout[t] if resident else 0.0
        loan_balance = m.member_loan * (1 + m.member_loan_rate) ** (t - m.entry_year)
        loan_repaid = loan_balance if t == loan_due else 0.0
        equity_repaid = m.equity * cidx[t] if t == m.exit_year + 1 else 0.0
        invested += saving + payout_share + loan_repaid + equity_repaid
        default += saving + payout_share
        holdings = (m.equity * cidx[t] if t <= m.exit_year else 0.0) + (
            loan_balance if t < loan_due else 0.0
        )
        rows.append(
            {
                "t": t,
                "year": int(tab["year"].iloc[t]),
                "rent_saving_month": saving / 12,
                "project": invested + holdings,
                "alternative": alternative,
                "default": default,
            }
        )
    out = pd.DataFrame(rows).set_index("t")
    deflator = cidx[out.index] / cidx[1]
    for column in ("rent_saving_month", "project", "alternative", "default"):
        out[column] = out[column] / deflator
    out["advantage"] = out["project"] - out["alternative"]
    out["deflator"] = deflator
    return out


def _final_advantage(scenario: Scenario, result: Result, m: MemberInputs) -> float:
    return float(member_view(scenario, result, m)["advantage"].iloc[-1])


def _advantage_line(scenario: Scenario, result: Result, m: MemberInputs) -> tuple[float, float]:
    """Advantage at market rent 0 and its change per EUR of market rent.

    Exact because the advantage is linear in the market rent: the rent saving
    is market minus project rent and is invested the same way every year.
    """
    at_zero = _final_advantage(scenario, result, replace(m, market_rent=0.0))
    at_one = _final_advantage(scenario, result, replace(m, market_rent=1_000.0))
    return at_zero, (at_one - at_zero) / 1_000.0


def break_even_rent(scenario: Scenario, result: Result, m: MemberInputs) -> float:
    """Market rent at which project and market-rent path end equally rich."""
    at_zero, slope = _advantage_line(scenario, result, m)
    return -at_zero / slope


def break_even_grid(
    scenario: Scenario,
    result: Result,
    m: MemberInputs,
    market_rents: np.ndarray,
    rate_differences_pp: np.ndarray,
) -> pd.DataFrame:
    """Member's advantage at the end for market rents x return gaps, in money of year 1.

    The return gap is the alternative return minus the member loan rate, in
    percentage points; the project and its required rent stay as in `result`.
    Positive values mean living in the project leaves the member richer.
    Rows are return gaps, columns market rents.
    """
    rows = {}
    for gap in rate_differences_pp:
        variant = replace(m, alt_return=m.member_loan_rate + gap / 100)
        at_zero, slope = _advantage_line(scenario, result, variant)
        rows[gap] = at_zero + slope * np.asarray(market_rents, dtype=float)
    return pd.DataFrame.from_dict(rows, orient="index", columns=list(market_rents))
