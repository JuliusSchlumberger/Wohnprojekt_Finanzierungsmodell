"""Spread of the required rent under uncertain inputs; entry point `rent_uncertainty`."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from model.cashflow import _run
from model.presets import BANK_RATE_CHANGE_STEP, ProjectInputs, build_scenario
from model.solve import RENT_BRACKET_EUR_PERSON, is_affordable, required_rent

SAMPLE_RENT_TOLERANCE_EUR = 0.5
SAMPLE_WINDOW = 0.08
PERCENTILES = (10, 50, 90)


@dataclass(frozen=True)
class Ranges:
    """Low and high value per uncertain input; the current input is the most likely value.

    Rates are fractions per year, `bank_rate_change_pp` is the change of the
    bank rate after the fixed-rate period in percentage points, the member
    loan term is in years (drawn values are rounded to whole years), and the
    factors scale renovation cost, running costs (admin plus insurance) and
    the amounts of member loans and 10-year direct loans.
    """

    inflation: tuple[float, float] = (0.01, 0.04)
    bank_rate_change_pp: tuple[float, float] = (-1.0, 3.0)
    vacancy_rate: tuple[float, float] = (0.02, 0.08)
    renovation_factor: tuple[float, float] = (0.9, 1.3)
    running_cost_factor: tuple[float, float] = (0.8, 1.5)
    member_loan_term_years: tuple[float, float] = (10.0, 20.0)
    member_loan_factor: tuple[float, float] = (0.6, 1.1)
    direct_loans_10y_factor: tuple[float, float] = (0.5, 1.1)


@dataclass
class UncertaintyResult:
    samples: pd.DataFrame
    rent_percentiles: dict[int, float]
    base_rent: float
    safe_rent: float
    headroom_band: pd.DataFrame
    headroom_band_nominal: pd.DataFrame
    sensitivity: pd.Series
    failed: int = 0


def _modes(p: ProjectInputs) -> dict[str, float]:
    return {
        "inflation": p.inflation,
        "bank_rate_change_pp": p.bank_rate_change * BANK_RATE_CHANGE_STEP * 100,
        "vacancy_rate": p.vacancy_rate,
        "renovation_factor": 1.0,
        "running_cost_factor": 1.0,
        "member_loan_term_years": float(p.member_loan_term_years),
        "member_loan_factor": 1.0,
        "direct_loans_10y_factor": 1.0,
    }


def _triangular(u: np.ndarray, low: float, mode: float, high: float) -> np.ndarray:
    """Inverse CDF of the triangular distribution; the mode is clipped into [low, high]."""
    if high <= low:
        return np.full_like(u, low)
    mode = min(max(mode, low), high)
    split = (mode - low) / (high - low)
    left = low + np.sqrt(u * (high - low) * (mode - low))
    right = high - np.sqrt((1 - u) * (high - low) * (high - mode))
    return np.where(u < split, left, right)


def latin_hypercube(p: ProjectInputs, ranges: Ranges, n: int, seed: int = 42) -> pd.DataFrame:
    """`n` Latin-hypercube draws of the uncertain inputs, one column per input."""
    rng = np.random.default_rng(seed)
    modes = _modes(p)
    columns = {}
    for name, (low, high) in vars(ranges).items():
        u = (rng.permutation(n) + rng.random(n)) / n
        columns[name] = _triangular(u, low, modes[name], high)
    return pd.DataFrame(columns)


def _apply(p: ProjectInputs, draw: pd.Series) -> ProjectInputs:
    """Variant for one draw; interest rates keep their spread above inflation."""
    shift = float(draw["inflation"]) - p.inflation

    def shifted(rate: float) -> float:
        return max(rate + shift, 0.0)

    return replace(
        p,
        inflation=float(draw["inflation"]),
        bank_rate=shifted(p.bank_rate),
        subsidy_rate=shifted(p.subsidy_rate),
        direct_loan_rate_5y=shifted(p.direct_loan_rate_5y),
        direct_loan_rate_10y=shifted(p.direct_loan_rate_10y),
        member_loan_rate=shifted(p.member_loan_rate),
        bank_rate_change=float(draw["bank_rate_change_pp"]) / (100 * BANK_RATE_CHANGE_STEP),
        vacancy_rate=float(draw["vacancy_rate"]),
        renovation_cost=p.renovation_cost * float(draw["renovation_factor"]),
        admin_cost_per_year=p.admin_cost_per_year * float(draw["running_cost_factor"]),
        insurance_per_year=p.insurance_per_year * float(draw["running_cost_factor"]),
        member_loan_term_years=round(float(draw["member_loan_term_years"])),
        member_loans=p.member_loans * float(draw["member_loan_factor"]),
        direct_loans_10y=p.direct_loans_10y * float(draw["direct_loans_10y_factor"]),
    )


def _rent_near(scenario, guess: float) -> float:
    """Required rent searched around `guess`, to SAMPLE_RENT_TOLERANCE_EUR.

    Starts with a window of +-SAMPLE_WINDOW around the guess and doubles the
    step outwards until the window brackets the required rent, then bisects.
    """
    limit = RENT_BRACKET_EUR_PERSON[1]
    step = SAMPLE_WINDOW * guess
    lo, hi = guess - step, guess + step
    while not is_affordable(scenario, hi):
        if hi >= limit:
            raise ValueError(f"rent above {limit} EUR per person needed")
        step *= 2
        lo, hi = hi, min(hi + step, limit)
    while lo > 0 and is_affordable(scenario, lo):
        step *= 2
        lo, hi = max(lo - step, 0.0), lo
    if lo == 0 and is_affordable(scenario, lo):
        return 0.0
    while hi - lo > SAMPLE_RENT_TOLERANCE_EUR:
        mid = 0.5 * (lo + hi)
        if is_affordable(scenario, mid):
            hi = mid
        else:
            lo = mid
    return hi


def _band(paths: pd.DataFrame, start_year: int) -> pd.DataFrame:
    band = pd.DataFrame({f"p{q}": paths.quantile(q / 100, axis=1) for q in PERCENTILES})
    band.insert(0, "year", start_year + band.index)
    return band


def rent_uncertainty(
    p: ProjectInputs, ranges: Ranges, n: int = 300, seed: int = 42
) -> UncertaintyResult:
    """Required rent for `n` sampled variants and the reserve headroom at the safe rent.

    The safe rent is the 90th percentile of the sampled required rents: it is
    enough in 90 % of the variants. Every variant is simulated at that rent;
    the band is liquidity minus required reserve, in purchasing power of
    year 1 (`headroom_band`) and in nominal euros (`headroom_band_nominal`),
    so values below zero mean the reserve is undercut. Interest rates move
    with the sampled inflation, keeping their spread. Sensitivity is
    the Spearman rank correlation of each input with the required rent.
    """
    base_scenario = build_scenario(p)
    base_rent = required_rent(base_scenario)
    draws = latin_hypercube(p, ranges, n, seed)
    scenarios = [build_scenario(_apply(p, draw)) for _, draw in draws.iterrows()]
    rents = []
    for scenario in scenarios:
        try:
            rents.append(_rent_near(scenario, base_rent))
        except ValueError:
            rents.append(np.nan)
    draws["required_rent"] = rents
    valid = draws.dropna(subset=["required_rent"])
    if valid.empty:
        raise ValueError("no sampled variant has a feasible rent")
    percentiles = {q: float(np.percentile(valid["required_rent"], q)) for q in PERCENTILES}
    safe_rent = percentiles[90]

    real, nominal = {}, {}
    for i in valid.index:
        raw = _run(scenarios[i], safe_rent)
        nominal[i] = raw["headroom"]
        real[i] = raw["headroom"] / (raw["cost_index"] / raw["cost_index"][1])
    years = base_scenario.property.start_year
    band, band_nominal = (_band(pd.DataFrame(paths).loc[1:], years) for paths in (real, nominal))

    ranks = valid.rank()
    sensitivity = (
        ranks.drop(columns="required_rent")
        .corrwith(ranks["required_rent"])
        .fillna(0.0)
        .sort_values(key=np.abs, ascending=False)
    )
    return UncertaintyResult(
        samples=draws,
        rent_percentiles=percentiles,
        base_rent=base_rent,
        safe_rent=safe_rent,
        headroom_band=band,
        headroom_band_nominal=band_nominal,
        sensitivity=sensitivity,
        failed=int(draws["required_rent"].isna().sum()),
    )
