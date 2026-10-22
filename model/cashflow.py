"""Annual cash-flow simulation of a scenario at a given starting rent; entry point `simulate`."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd

from model.types import Scenario, Tranche

SENIOR_KINDS = ("bank_loan", "subsidy_loan")
_PAID_OFF_EUR = 0.5


@dataclass
class TrancheSchedule:
    """Per-year arrays of length horizon + 1; index 0 is the opening state."""

    interest: np.ndarray
    interest_paid: np.ndarray
    repayment: np.ndarray
    inflow: np.ndarray
    balance: np.ndarray

    @property
    def cash_out(self) -> np.ndarray:
        return self.interest_paid + self.repayment


@dataclass
class Result:
    table: pd.DataFrame
    tranches: dict[str, pd.DataFrame]
    metrics: dict[str, float] = field(default_factory=dict)


def cost_index(scenario: Scenario) -> np.ndarray:
    """Inflation index for years 0..T, 1 until indexation starts."""
    ops = scenario.operations
    t = np.arange(scenario.horizon_years + 1)
    k = np.clip(t - ops.indexation_start_year + 1, 0, None)
    k[0] = 0
    return (1 + ops.inflation) ** k


def amortization_years(tr: Tranche, principal: float) -> float:
    """Years of repayment after the grace period, possibly fractional."""
    if tr.initial_repayment_rate is None:
        return tr.term_years - tr.grace_years
    r, i0 = tr.interest_rate, tr.initial_repayment_rate
    if r == 0:
        return 1 / i0
    payment = principal * (r + i0)
    return math.log(payment / (payment - r * principal)) / math.log(1 + r)


def tranche_schedule(tr: Tranche, horizon: int) -> TrancheSchedule:
    """Interest, repayment and balance of one tranche.

    Interest is charged on the balance at the start of the year including that
    year's drawdown; service starts in the drawdown year (year 1 if drawn up
    front) and a repayment grant is credited then. Annuities are recomputed
    each year on the remaining balance and term, so a rate reset or repayment
    grant keeps the payoff date.
    Direct-loan cancellations count as repayment; replacements as inflow.
    """
    if tr.interest_mode == "accrued" and tr.repayment in ("annuity", "linear"):
        raise ValueError(f"{tr.name}: accrued interest needs repayment 'bullet' or 'none'")
    n = horizon + 1
    s = TrancheSchedule(*(np.zeros(n) for _ in range(5)))
    d = tr.drawdown_year
    if d == 0:
        s.balance[0] = tr.amount
    principal = tr.amount - tr.subsidy_grant
    n_amort = amortization_years(tr, principal) if tr.repayment in ("annuity", "linear") else 0.0

    first = max(d, 1)
    for t in range(first, n):
        b = s.balance[t - 1]
        if t == d:
            b += tr.amount
            s.inflow[t] += tr.amount
        if t == first and tr.subsidy_grant:
            b -= min(tr.subsidy_grant, b)
        years_in = t - first + 1
        r = tr.rate_in_year(years_in)
        interest = b * r
        s.interest[t] = interest
        if tr.interest_mode == "accrued":
            b += interest
        else:
            s.interest_paid[t] = interest

        repay = 0.0
        amort_year = years_in - tr.grace_years
        if amort_year >= 1 and b > 0:
            if tr.repayment == "annuity":
                n_rem = n_amort - amort_year + 1
                if n_rem <= 1:
                    repay = b
                else:
                    pay = b / n_rem if r == 0 else b * r / (1 - (1 + r) ** -n_rem)
                    repay = min(pay - interest, b)
            elif tr.repayment == "linear":
                repay = min(principal / n_amort, b)
            elif tr.repayment == "bullet" and years_in >= tr.term_years:
                repay = b
        b -= repay

        if tr.kind == "direct_loan" and tr.churn_rate:
            cancelled = tr.churn_rate * b
            replaced = tr.replacement_rate * cancelled
            b += replaced - cancelled
            repay += cancelled
            s.inflow[t] += replaced
        s.repayment[t] = repay
        s.balance[t] = b
    return s


def opening_liquidity(scenario: Scenario, rent_per_m2: float) -> float:
    ops = scenario.operations
    if ops.start_liquidity is not None:
        return ops.start_liquidity
    first_year_rent = rent_per_m2 * scenario.private_area_m2_total * 12 * _rent_index(scenario)[1]
    return ops.min_liquidity_months / 12 * first_year_rent


def financed_tranches(scenario: Scenario, start_liquidity: float) -> list[Tranche]:
    """All tranches incl. member capital, residual sized to close the gap.

    Sources must equal total investment plus opening liquidity.
    """
    tranches = scenario.tranches + scenario.member_tranches()
    need = scenario.property.total_investment + start_liquidity
    residual = [tr for tr in tranches if tr.residual]
    fixed = sum(tr.amount for tr in tranches if not tr.residual)
    if len(residual) > 1:
        raise ValueError("at most one residual tranche allowed")
    if residual:
        gap = need - fixed
        if gap < 0:
            raise ValueError(f"sources exceed need by {-gap:,.0f} EUR; residual would be negative")
        return [replace(tr, amount=gap) if tr.residual else tr for tr in tranches]
    if abs(fixed - need) > 1.0:
        raise ValueError(
            f"sources {fixed:,.0f} EUR != investment + opening liquidity {need:,.0f} EUR; "
            "adjust amounts or mark one tranche residual"
        )
    return tranches


def _rent_index(scenario: Scenario) -> np.ndarray:
    if scenario.operations.rent_mode == "indexed":
        return cost_index(scenario)
    return np.ones(scenario.horizon_years + 1)


def debt_schedules(scenario: Scenario, start_liquidity: float) -> dict[str, TrancheSchedule]:
    tranches = financed_tranches(scenario, start_liquidity)
    names = [tr.name for tr in tranches]
    if len(set(names)) != len(names):
        raise ValueError(f"tranche names must be unique: {names}")
    return {tr.name: tranche_schedule(tr, scenario.horizon_years) for tr in tranches}


def senior_payoff_year(scenario: Scenario, schedules: dict[str, TrancheSchedule]) -> int | None:
    """First operating year after which all bank and subsidy loans are repaid."""
    kinds = {tr.name: tr.kind for tr in scenario.tranches}
    senior = [s for name, s in schedules.items() if kinds.get(name) in SENIOR_KINDS]
    if not senior:
        return None
    outstanding = np.sum([s.balance for s in senior], axis=0)
    drawn = np.sum([np.cumsum(s.inflow) + s.balance[0] for s in senior], axis=0) > 0
    done = np.nonzero((outstanding <= _PAID_OFF_EUR) & drawn)[0]
    done = done[done >= 1]
    return int(done[0]) if done.size else None


def _run(scenario: Scenario, rent_per_m2: float) -> dict[str, np.ndarray | float | dict]:
    """Core simulation returning raw arrays; `simulate` wraps it for display."""
    ops, prop, rules = scenario.operations, scenario.property, scenario.rules
    T = scenario.horizon_years
    t = np.arange(T + 1)
    cidx = cost_index(scenario)
    ridx = _rent_index(scenario)

    start_liq = opening_liquidity(scenario, rent_per_m2)
    schedules = debt_schedules(scenario, start_liq)

    gross_rent = rent_per_m2 * scenario.private_area_m2_total * 12 * ridx
    gross_rent[0] = 0.0
    maintenance = ops.maintenance_rate * prop.replacement_value * cidx
    admin = ops.admin_cost_per_year * cidx
    insurance = ops.insurance_per_year * cidx
    community = ops.community_cost_per_year * cidx
    ground_rent = (
        prop.leasehold_rate * prop.ground_value * cidx
        if prop.tenure == "leasehold"
        else np.zeros(T + 1)
    )
    operating = maintenance + admin + insurance + community + ground_rent
    operating[0] = 0.0

    interest = np.sum([s.interest for s in schedules.values()], axis=0)
    interest_paid = np.sum([s.interest_paid for s in schedules.values()], axis=0)
    repayment = np.sum([s.repayment for s in schedules.values()], axis=0)
    inflow = np.sum([s.inflow for s in schedules.values()], axis=0)
    debt_service = interest_paid + repayment

    kinds = {tr.name: tr.kind for tr in scenario.tranches}
    senior = [s.cash_out for n, s in schedules.items() if kinds.get(n) in SENIOR_KINDS]
    senior_service = np.sum(senior, axis=0) if senior else np.zeros(T + 1)
    payoff = senior_payoff_year(scenario, schedules)
    freed = np.zeros(T + 1)
    if payoff is not None:
        freed[t > payoff] = senior_service.max()

    rent_reduction = np.zeros(T + 1)
    payout = np.zeros(T + 1)
    transfer_out = np.zeros(T + 1)
    if rules.surplus_use == "rent_reduction":
        rent_reduction = np.minimum(freed, gross_rent)
    elif rules.surplus_use == "next_project":
        transfer_out = freed
    else:
        pot = np.cumsum(freed)
        due = (t > 0) & (t % rules.payout_interval_years == 0)
        paid_so_far = 0.0
        for year in np.nonzero(due)[0]:
            payout[year] = pot[year] - paid_so_far
            paid_so_far = pot[year]

    charged_rent = gross_rent - rent_reduction
    rent_income = charged_rent * (1 - ops.vacancy_rate)
    net = rent_income - operating - debt_service + inflow - payout - transfer_out
    net[0] = 0.0
    liquidity = start_liq + np.cumsum(net)
    reserve_required = ops.min_liquidity_months / 12 * charged_rent
    headroom = liquidity - reserve_required

    return {
        "t": t,
        "cost_index": cidx,
        "gross_rent": gross_rent,
        "rent_reduction": rent_reduction,
        "charged_rent": charged_rent,
        "rent_income": rent_income,
        "maintenance": maintenance,
        "admin": admin,
        "insurance": insurance,
        "community": community,
        "ground_rent": ground_rent,
        "operating": operating,
        "interest": interest,
        "interest_paid": interest_paid,
        "repayment": repayment,
        "loan_inflow": inflow,
        "debt_service": debt_service,
        "payout": payout,
        "transfer_out": transfer_out,
        "liquidity": liquidity,
        "reserve_required": reserve_required,
        "headroom": headroom,
        "min_headroom": float(headroom[1:].min()),
        "payoff_year": payoff,
        "schedules": schedules,
    }


def min_headroom(scenario: Scenario, rent_per_m2: float) -> float:
    """Smallest liquidity minus required reserve over operating years."""
    return _run(scenario, rent_per_m2)["min_headroom"]


def simulate(scenario: Scenario, rent_per_m2: float) -> Result:
    """Simulate a scenario for a starting rent in EUR per m2 private area per month."""
    raw = _run(scenario, rent_per_m2)
    schedules = raw.pop("schedules")
    payoff = raw.pop("payoff_year")
    min_head = raw.pop("min_headroom")
    table = pd.DataFrame(raw).set_index("t")
    table.insert(0, "year", scenario.property.start_year + table.index)
    area = scenario.private_area_m2_total
    table["rent_per_m2"] = np.where(table.index > 0, table["charged_rent"] / (12 * area), np.nan)
    tranches = {name: pd.DataFrame(vars(s), index=table.index) for name, s in schedules.items()}
    metrics: dict[str, float] = {
        "rent_per_m2": rent_per_m2,
        "rent_per_year": float(table["gross_rent"].iloc[1]),
        "min_headroom": min_head,
        "senior_payoff_year": float("nan") if payoff is None else float(payoff),
        "total_interest": float(table["interest"].sum()),
        "opening_liquidity": float(table["liquidity"].iloc[0]),
    }
    for m in scenario.member_types:
        metrics[f"rent_per_person_month:{m.name}"] = rent_per_m2 * m.private_area_m2
    return Result(table=table, tranches=tranches, metrics=metrics)
