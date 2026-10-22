"""Solvers for the dashboard modes; mode 1 is `required_rent`."""

from __future__ import annotations

from model.cashflow import min_headroom
from model.types import Scenario

RENT_BRACKET_EUR_M2 = (0.0, 50.0)
RENT_TOLERANCE_EUR_M2 = 0.01


def required_rent(
    scenario: Scenario,
    bracket: tuple[float, float] = RENT_BRACKET_EUR_M2,
    tol: float = RENT_TOLERANCE_EUR_M2,
) -> float:
    """Lowest starting rent (EUR/m2 private area/month) keeping liquidity >= reserve every year.

    Bisection on the minimum yearly headroom, which increases with rent.
    Raises ValueError if even the upper bracket rent is insufficient.
    """
    lo, hi = bracket
    if min_headroom(scenario, hi) < 0:
        raise ValueError(f"rent above {hi} EUR/m2 needed; check scenario")
    if min_headroom(scenario, lo) >= 0:
        return lo
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if min_headroom(scenario, mid) >= 0:
            hi = mid
        else:
            lo = mid
    return hi
