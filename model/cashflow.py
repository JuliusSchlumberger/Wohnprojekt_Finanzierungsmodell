"""Annual cash-flow simulation of a scenario at a given starting rent; entry point `simulate`."""

from __future__ import annotations

import math
from dataclasses import astuple, dataclass, field, replace
from functools import lru_cache
from typing import get_args

import numpy as np
import pandas as pd

from model.types import Rules, Scenario, Tranche, TrancheKind

SENIOR_KINDS = ("bank_loan", "subsidy_loan")
SUBORDINATED_KINDS = ("member_loan", "direct_loan")
EQUITY_LIKE_KINDS = ("equity", *SUBORDINATED_KINDS)
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


def _settle(
    rules: Rules,
    net: np.ndarray,
    start_liquidity: float,
    reserve: np.ndarray,
    due: np.ndarray,
    due_rate: np.ndarray,
    outstanding: np.ndarray,
) -> dict[str, np.ndarray]:
    """Year-by-year liquidity with deferred repayments and surplus redirection.

    `net` excludes the subordinated repayments `due`. With
    `rules.defer_repayments`, arrears are paid first (oldest first), then the
    year's due amount, each only as far as liquidity stays above the reserve;
    the rest becomes arrears that bear interest at `due_rate`, paid yearly.
    Arrears still open `max_arrears_years` after falling due are reported as
    overdue. Without deferral the due amount is paid in full.
    With `rules.redirect_surplus`, liquidity above the reserve plus all
    `outstanding` subordinated debt is taken out once no arrears are open.
    """
    n = len(net)
    out = {
        k: np.zeros(n)
        for k in (
            "liquidity",
            "surplus",
            "paid_on_time",
            "arrears_new",
            "arrears_paid",
            "arrears",
            "arrears_interest",
            "arrears_overdue",
        )
    }
    cohorts: list[list[float]] = []  # [year due, open amount, rate]
    liq = out["liquidity"][0] = start_liquidity
    for t in range(1, n):
        liq += net[t]
        out["arrears_interest"][t] = sum(amount * rate for _, amount, rate in cohorts)
        liq -= out["arrears_interest"][t]
        if rules.defer_repayments:
            for cohort in cohorts:
                pay = min(max(liq - reserve[t], 0.0), cohort[1])
                cohort[1] -= pay
                liq -= pay
                out["arrears_paid"][t] += pay
            cohorts = [c for c in cohorts if c[1] > _PAID_OFF_EUR]
            paid = min(max(liq - reserve[t], 0.0), due[t])
            if due[t] - paid > _PAID_OFF_EUR:
                cohorts.append([t, due[t] - paid, due_rate[t]])
                out["arrears_new"][t] = due[t] - paid
        else:
            paid = due[t]
        liq -= paid
        out["paid_on_time"][t] = paid
        out["arrears"][t] = sum(amount for _, amount, _ in cohorts)
        out["arrears_overdue"][t] = sum(
            amount for year, amount, _ in cohorts if t - year >= rules.max_arrears_years
        )
        if rules.redirect_surplus and not cohorts:
            out["surplus"][t] = max(liq - reserve[t] - outstanding[t], 0.0)
            liq -= out["surplus"][t]
        out["liquidity"][t] = liq
    return out


def _distribute(amount: np.ndarray, rules: Rules) -> dict[str, np.ndarray]:
    """Split freed money by the A4 rule into rent reduction, payout and transfer."""
    zeros = np.zeros_like(amount)
    if rules.surplus_use == "rent_reduction":
        return {"rent_reduction": amount, "payout": zeros, "transfer_out": zeros}
    if rules.surplus_use == "next_project":
        return {"rent_reduction": zeros, "payout": zeros, "transfer_out": amount}
    t = np.arange(len(amount))
    pot = np.cumsum(amount)
    payout = np.zeros_like(amount)
    paid_so_far = 0.0
    for year in np.nonzero((t > 0) & (t % rules.payout_interval_years == 0))[0]:
        payout[year] = pot[year] - paid_so_far
        paid_so_far = pot[year]
    return {"rent_reduction": zeros, "payout": payout, "transfer_out": zeros}


def opening_liquidity(scenario: Scenario, rent_per_person: float) -> float:
    ops = scenario.operations
    if ops.start_liquidity is not None:
        return ops.start_liquidity
    first_year_rent = rent_per_person * scenario.persons * 12 * _rent_index(scenario)[1]
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


def capital_structure(scenario: Scenario, rent_per_person: float) -> dict[str, float]:
    """Financed amount per tranche kind and the equity-like share of total investment.

    Equity-like capital is member equity plus subordinated member and direct
    loans, which banks usually count towards the borrower's own funds.
    """
    tranches = financed_tranches(scenario, opening_liquidity(scenario, rent_per_person))
    amounts = dict.fromkeys(get_args(TrancheKind), 0.0)
    for tr in tranches:
        amounts[tr.kind] += float(tr.amount)
    equity_like = sum(amounts[kind] for kind in EQUITY_LIKE_KINDS)
    return {
        **amounts,
        "equity_like": equity_like,
        "equity_like_share": equity_like / scenario.property.total_investment,
    }


def _rent_index(scenario: Scenario) -> np.ndarray:
    if scenario.operations.rent_mode == "indexed":
        return cost_index(scenario)
    return np.ones(scenario.horizon_years + 1)


def debt_schedules(scenario: Scenario, start_liquidity: float) -> dict[str, TrancheSchedule]:
    tranches = financed_tranches(scenario, start_liquidity)
    names = [tr.name for tr in tranches]
    if len(set(names)) != len(names):
        raise ValueError(f"tranche names must be unique: {names}")
    return {tr.name: _cached_schedule(astuple(tr), scenario.horizon_years) for tr in tranches}


@lru_cache(maxsize=1024)
def _cached_schedule(fields: tuple, horizon: int) -> TrancheSchedule:
    # Rent searches re-run the same fixed tranches many times; only the residual
    # bank loan changes. Arrays are frozen because the cache shares them.
    schedule = tranche_schedule(Tranche(*fields), horizon)
    for array in vars(schedule).values():
        array.setflags(write=False)
    return schedule


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


def _run(scenario: Scenario, rent_per_person: float) -> dict[str, np.ndarray | float | dict]:
    """Core simulation returning raw arrays; `simulate` wraps it for display."""
    ops, prop, rules = scenario.operations, scenario.property, scenario.rules
    T = scenario.horizon_years
    t = np.arange(T + 1)
    cidx = cost_index(scenario)
    ridx = _rent_index(scenario)

    start_liq = opening_liquidity(scenario, rent_per_person)
    schedules = debt_schedules(scenario, start_liq)

    gross_rent = rent_per_person * scenario.persons * 12 * ridx
    gross_rent[0] = 0.0
    maintenance = ops.maintenance_rate * prop.replacement_value * cidx
    reserve_contribution = (
        maintenance.copy()
        if ops.maintenance_reserve_rate is None
        else ops.maintenance_reserve_rate * prop.replacement_value * cidx
    )
    admin = ops.admin_cost_per_year * cidx
    insurance = ops.insurance_per_year * cidx
    community = ops.community_cost_per_year * cidx
    ground_rent = (
        prop.leasehold_rate * prop.ground_value * cidx
        if prop.tenure == "leasehold"
        else np.zeros(T + 1)
    )
    operating = reserve_contribution + admin + insurance + community + ground_rent
    operating[0] = 0.0
    maintenance_reserve = np.cumsum(np.where(t > 0, reserve_contribution - maintenance, 0.0))

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

    if rules.redirect_surplus and rules.surplus_use != "rent_reduction":
        # freed debt service stays in liquidity and leaves as surplus
        freed[:] = 0.0
    freed_use = _distribute(np.minimum(freed, gross_rent), rules)
    rent_reduction = freed_use["rent_reduction"]
    charged_rent = gross_rent - rent_reduction
    vacancy = np.full(T + 1, ops.vacancy_rate)
    if ops.initial_vacancy_rate is not None:
        vacancy[1 : ops.initial_vacancy_years + 1] = ops.initial_vacancy_rate
    rent_income = charged_rent * (1 - vacancy)
    net = (
        rent_income
        - operating
        - debt_service
        + inflow
        - freed_use["payout"]
        - freed_use["transfer_out"]
    )
    net[0] = 0.0
    reserve_required = ops.min_liquidity_months / 12 * charged_rent
    sub = {n: s for n, s in schedules.items() if kinds.get(n) in SUBORDINATED_KINDS}
    zeros = np.zeros(T + 1)
    due = sum((s.repayment for s in sub.values()), start=zeros)
    if not (rules.defer_repayments or rules.redirect_surplus):
        liquidity = start_liq + np.cumsum(net)
        settled = {"surplus": zeros, "paid_on_time": due, "arrears_new": zeros}
        settled |= {"arrears_paid": zeros, "arrears": zeros, "arrears_interest": zeros}
        settled["arrears_overdue"] = zeros
    else:
        rates = {tr.name: tr.interest_rate for tr in scenario.tranches}
        weighted = sum((s.repayment * rates[n] for n, s in sub.items()), start=zeros)
        due_rate = np.divide(weighted, due, out=np.zeros(T + 1), where=due > 0)
        outstanding = sum((s.balance for s in sub.values()), start=zeros)
        settled = _settle(rules, net + due, start_liq, reserve_required, due, due_rate, outstanding)
        liquidity = settled.pop("liquidity")
        repayment = repayment - due + settled["paid_on_time"] + settled["arrears_paid"]
        interest_paid = interest_paid + settled["arrears_interest"]
        interest = interest + settled["arrears_interest"]
        debt_service = interest_paid + repayment
    surplus = settled.pop("surplus")
    surplus_use = _distribute(surplus, rules)
    payout = freed_use["payout"] + surplus_use["payout"]
    transfer_out = freed_use["transfer_out"] + surplus_use["transfer_out"]
    rent_rebate = surplus_use["rent_reduction"]
    headroom = liquidity - reserve_required
    worst = min(headroom[1:].min(), -settled["arrears_overdue"].max())

    return {
        "t": t,
        "cost_index": cidx,
        "gross_rent": gross_rent,
        "rent_reduction": rent_reduction,
        "charged_rent": charged_rent,
        "vacancy_rate": vacancy,
        "rent_income": rent_income,
        "maintenance": maintenance,
        "reserve_contribution": reserve_contribution,
        "maintenance_reserve": maintenance_reserve,
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
        "sub_due": due,
        "sub_paid_on_time": settled["paid_on_time"],
        "arrears_new": settled["arrears_new"],
        "arrears_paid": settled["arrears_paid"],
        "arrears": settled["arrears"],
        "arrears_interest": settled["arrears_interest"],
        "arrears_overdue": settled["arrears_overdue"],
        "surplus": surplus,
        "rent_rebate": rent_rebate,
        "payout": payout,
        "transfer_out": transfer_out,
        "liquidity": liquidity,
        "reserve_required": reserve_required,
        "headroom": headroom,
        "min_headroom": float(worst),
        "payoff_year": payoff,
        "schedules": schedules,
    }


def min_headroom(scenario: Scenario, rent_per_person: float) -> float:
    """Smallest liquidity minus required reserve over operating years."""
    return _run(scenario, rent_per_person)["min_headroom"]


def simulate(scenario: Scenario, rent_per_person: float) -> Result:
    """Simulate a scenario for a starting rent in EUR per person per month."""
    raw = _run(scenario, rent_per_person)
    schedules = raw.pop("schedules")
    payoff = raw.pop("payoff_year")
    min_head = raw.pop("min_headroom")
    table = pd.DataFrame(raw).set_index("t")
    table.insert(0, "year", scenario.property.start_year + table.index)
    table["rent_per_person"] = np.where(
        table.index > 0,
        (table["charged_rent"] - table["rent_rebate"]) / (12 * scenario.persons),
        np.nan,
    )
    tranches = {name: pd.DataFrame(vars(s), index=table.index) for name, s in schedules.items()}
    metrics: dict[str, float] = {
        "rent_per_person": rent_per_person,
        "rent_per_year": float(table["gross_rent"].iloc[1]),
        "min_headroom": min_head,
        "senior_payoff_year": float("nan") if payoff is None else float(payoff),
        "total_interest": float(table["interest"].sum()),
        "opening_liquidity": float(table["liquidity"].iloc[0]),
    }
    return Result(table=table, tranches=tranches, metrics=metrics)
