"""Solvers for the dashboard modes: `required_rent` (mode 1), `max_investment` (mode 3)."""

from __future__ import annotations

from collections.abc import Callable

from model.cashflow import _run, min_headroom
from model.types import Scenario

RENT_BRACKET_EUR_PERSON = (0.0, 5_000.0)
RENT_TOLERANCE_EUR_PERSON = 0.01
INVESTMENT_TOLERANCE_EUR = 1_000.0
INVESTMENT_LIMIT_EUR = 1e9
HEADROOM_TOLERANCE_EUR = 0.01


def is_affordable(scenario: Scenario, rent_per_person: float) -> bool:
    """Liquidity stays at or above the reserve in every year, up to rounding.

    Refinancing tops liquidity up to exactly the reserve, so the headroom in
    those years is zero only up to floating-point error.
    """
    return min_headroom(scenario, rent_per_person) >= -HEADROOM_TOLERANCE_EUR


def required_rent(
    scenario: Scenario,
    bracket: tuple[float, float] = RENT_BRACKET_EUR_PERSON,
    tol: float = RENT_TOLERANCE_EUR_PERSON,
) -> float:
    """Lowest starting rent (EUR per person and month) keeping liquidity >= reserve every year.

    Bisection on the minimum yearly headroom, which increases with rent.
    Raises ValueError if even the upper bracket rent is insufficient.
    """
    lo, hi = bracket
    if not is_affordable(scenario, hi):
        raise ValueError(f"rent above {hi} EUR per person needed; check scenario")
    if is_affordable(scenario, lo):
        return lo
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if is_affordable(scenario, mid):
            hi = mid
        else:
            lo = mid
    return hi


def max_investment(
    scenario_for: Callable[[float], Scenario],
    target_rent: float,
    lower: float,
    tol: float = INVESTMENT_TOLERANCE_EUR,
    upper_limit: float = INVESTMENT_LIMIT_EUR,
) -> float:
    """Largest total investment (EUR) whose required rent does not exceed `target_rent`.

    `scenario_for` builds the scenario for a given investment; the required
    rent must increase with investment, as it does when own funds are fixed
    and the bank loan closes the gap. `lower` is the smallest investment to
    consider, normally the own funds. Raises ValueError if even `lower` needs
    a higher rent.
    """

    def affordable(investment: float) -> bool:
        return is_affordable(scenario_for(investment), target_rent)

    if not affordable(lower):
        raise ValueError(
            f"target rent {target_rent} EUR per person does not carry {lower:,.0f} EUR"
        )
    lo, hi = lower, max(2 * lower, 100_000.0)
    while affordable(hi):
        lo, hi = hi, 2 * hi
        if hi > upper_limit:
            raise ValueError(f"investment above {upper_limit:,.0f} EUR affordable; check scenario")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if affordable(mid):
            lo = mid
        else:
            hi = mid
    return lo


def binding_year(
    scenario: Scenario, rent_per_person: float, step: float = 0.05
) -> tuple[int, str] | None:
    """Year that fixes the required rent and why: first failure at a slightly lower rent.

    Returns (year, "reserve") if liquidity would fall below the reserve, or
    (year, "arrears") if a deferred repayment would stay open too long; None
    if even a rent of zero would do.
    """
    if rent_per_person - step < 0:
        return None
    raw = _run(scenario, rent_per_person - step)
    for t in range(1, scenario.horizon_years + 1):
        if raw["headroom"][t] < -HEADROOM_TOLERANCE_EUR:
            return t, "reserve"
        if raw["arrears_overdue"][t] > 0:
            return t, "arrears"
    return None
