"""Sampled sensitivity of the required rent to eight inputs; `explore` and `summarize`."""

from __future__ import annotations

from dataclasses import asdict, replace
from itertools import combinations

import numpy as np
import pandas as pd

from model.presets import BANK_RATE_CHANGE_STEP, ProjectInputs, build_scenario
from model.solve import RENT_BRACKET_EUR_PERSON, is_affordable, required_rent

# Sampled ranges; spreads are percentage points above inflation, shares are of
# land + house + renovation.
PARAMETERS: dict[str, tuple[float, float]] = {
    "bank_spread_pp": (2.0, 6.0),
    "bank_rate_change_pp": (-1.0, 3.0),
    "vacancy_rate": (0.05, 0.15),
    "member_loan_share": (0.0, 0.5),
    "member_loan_spread_pp": (0.0, 4.0),
    "member_loan_term_years": (15, 30),
    "direct_loans_10y_share": (0.0, 0.4),
    "direct_loan_spread_10y_pp": (1.5, 2.0),
}
INTEGER_PARAMETERS = ("member_loan_term_years",)
# Bank requirement on equity plus subordinated loans, as the app default.
MIN_EQUITY_LIKE_SHARE = 0.20
RENT_TOLERANCE_EUR = 0.5
SEARCH_WINDOW = 0.08
BINS = 20
PAIR_BINS = 12
CHEAPEST_SHARE = 0.05


def latin_hypercube(n: int, seed: int) -> pd.DataFrame:
    """Uniform Latin-hypercube draws over PARAMETERS; integers equally likely."""
    rng = np.random.default_rng(seed)
    columns = {}
    for name, (low, high) in PARAMETERS.items():
        u = (rng.permutation(n) + rng.random(n)) / n
        if name in INTEGER_PARAMETERS:
            columns[name] = np.floor(low + u * (high - low + 1)).astype(int)
        else:
            columns[name] = low + u * (high - low)
    return pd.DataFrame(columns)


def main_investment(p: ProjectInputs) -> float:
    return p.land_price + p.building_price + p.renovation_cost


def apply_draw(p: ProjectInputs, draw: pd.Series) -> ProjectInputs:
    """Inputs for one draw; rates are inflation plus spread, never negative."""

    def rate(spread_pp: float) -> float:
        return max(p.inflation + spread_pp / 100, 0.0)

    base = main_investment(p)
    return replace(
        p,
        bank_rate=rate(draw["bank_spread_pp"]),
        bank_rate_change=float(draw["bank_rate_change_pp"]) / (100 * BANK_RATE_CHANGE_STEP),
        vacancy_rate=float(draw["vacancy_rate"]),
        member_loans=float(draw["member_loan_share"]) * base,
        member_loan_rate=rate(draw["member_loan_spread_pp"]),
        member_loan_term_years=int(draw["member_loan_term_years"]),
        direct_loans_10y=float(draw["direct_loans_10y_share"]) * base,
        direct_loan_rate_10y=rate(draw["direct_loan_spread_10y_pp"]),
    )


def default_values(p: ProjectInputs) -> dict[str, float]:
    """The inputs `p` expressed as the sampled parameters (inverse of `apply_draw`)."""
    base = main_investment(p)
    return {
        "bank_spread_pp": 100 * (p.bank_rate - p.inflation),
        "bank_rate_change_pp": 100 * p.bank_rate_change * BANK_RATE_CHANGE_STEP,
        "vacancy_rate": p.vacancy_rate,
        "member_loan_share": p.member_loans / base,
        "member_loan_spread_pp": 100 * (p.member_loan_rate - p.inflation),
        "member_loan_term_years": p.member_loan_term_years,
        "direct_loans_10y_share": p.direct_loans_10y / base,
        "direct_loan_spread_10y_pp": 100 * (p.direct_loan_rate_10y - p.inflation),
    }


def bank_compliant(p: ProjectInputs) -> bool:
    return p.equity_like >= MIN_EQUITY_LIKE_SHARE * p.total_investment


def _rent_near(scenario, guess: float) -> float:
    """Required rent to RENT_TOLERANCE_EUR, searched outwards from `guess`."""
    limit = RENT_BRACKET_EUR_PERSON[1]
    step = max(SEARCH_WINDOW * guess, 1.0)
    lo, hi = max(guess - step, 0.0), min(guess + step, limit)
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
    while hi - lo > RENT_TOLERANCE_EUR:
        mid = 0.5 * (lo + hi)
        if is_affordable(scenario, mid):
            hi = mid
        else:
            lo = mid
    return hi


def explore(p: ProjectInputs, draws: pd.DataFrame) -> pd.DataFrame:
    """Draws with `compliant` and `required_rent` (NaN if excluded or not feasible)."""
    guess = required_rent(build_scenario(p))
    compliant, rents = [], []
    for _, draw in draws.iterrows():
        q = apply_draw(p, draw)
        ok = bank_compliant(q)
        compliant.append(ok)
        rent = np.nan
        if ok:
            try:
                rent = _rent_near(build_scenario(q), guess)
            except ValueError:
                pass
        rents.append(rent)
    return draws.assign(compliant=compliant, required_rent=rents)


def _edges(name: str, bins: int) -> np.ndarray:
    low, high = PARAMETERS[name]
    if name in INTEGER_PARAMETERS:
        return np.arange(low, high + 2) - 0.5
    return np.linspace(low, high, bins + 1)


def _binned(x: pd.Series, edges: np.ndarray) -> pd.Series:
    return pd.Series(np.clip(np.digitize(x, edges) - 1, 0, len(edges) - 2), index=x.index)


def _per_parameter(valid: pd.DataFrame, name: str) -> pd.DataFrame:
    edges = _edges(name, BINS)
    groups = valid["required_rent"].groupby(_binned(valid[name], edges))
    out = pd.DataFrame(
        {
            "min": groups.min(),
            "p10": groups.quantile(0.10),
            "p50": groups.median(),
            "p90": groups.quantile(0.90),
            "count": groups.size(),
        }
    )
    out.insert(0, "x", 0.5 * (edges[:-1] + edges[1:])[out.index])
    return out.reset_index(drop=True)


def _pearson(x: pd.Series, y: pd.Series) -> float:
    # Elementwise numpy only: pandas' corr goes through BLAS, which fails to load in some
    # Windows environments on large arrays.
    dx = x.to_numpy(float) - x.mean()
    dy = y.to_numpy(float) - y.mean()
    return float((dx * dy).mean() / np.sqrt((dx * dx).mean() * (dy * dy).mean()))


def _importance(valid: pd.DataFrame) -> pd.DataFrame:
    """Share of rent variance explained by each input alone, linear and in total.

    Total is the correlation ratio eta^2 over BINS bins (any shape of
    dependence); linear is the squared Pearson correlation. The rest of the
    variance comes from interactions between inputs.
    """
    rent = valid["required_rent"]
    total_var = rent.var(ddof=0)
    rows = {}
    for name in PARAMETERS:
        bins = _binned(valid[name], _edges(name, BINS))
        means = rent.groupby(bins).transform("mean")
        eta2 = means.var(ddof=0) / total_var
        r = _pearson(valid[name], rent)
        rows[name] = {
            "total": eta2,
            "linear": min(r**2, eta2),
            "direction": float(np.sign(r)),
        }
    return pd.DataFrame(rows).T.sort_values("total", ascending=False)


def _pairs(valid: pd.DataFrame) -> dict[str, dict]:
    out = {}
    for a, b in combinations(PARAMETERS, 2):
        ea, eb = _edges(a, PAIR_BINS), _edges(b, PAIR_BINS)
        grid = (
            valid["required_rent"].groupby([_binned(valid[a], ea), _binned(valid[b], eb)]).median()
        )
        z = grid.unstack().reindex(index=range(len(ea) - 1), columns=range(len(eb) - 1))
        out[f"{a}|{b}"] = {
            "x": list(0.5 * (ea[:-1] + ea[1:])),
            "y": list(0.5 * (eb[:-1] + eb[1:])),
            "z": z.to_numpy().tolist(),
        }
    return out


def _cheapest(valid: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Per input: share of all variants and of the cheapest CHEAPEST_SHARE per bin."""
    threshold = valid["required_rent"].quantile(CHEAPEST_SHARE)
    cheap = valid[valid["required_rent"] <= threshold]
    out = {}
    for name in PARAMETERS:
        edges = _edges(name, BINS)
        share_all = _binned(valid[name], edges).value_counts(normalize=True)
        share_cheap = _binned(cheap[name], edges).value_counts(normalize=True)
        index = range(len(edges) - 1)
        out[name] = pd.DataFrame(
            {
                "x": 0.5 * (edges[:-1] + edges[1:]),
                "all": share_all.reindex(index, fill_value=0.0).to_numpy(),
                "cheapest": share_cheap.reindex(index, fill_value=0.0).to_numpy(),
            }
        )
    return out


def summarize(p: ProjectInputs, samples: pd.DataFrame, seed: int) -> dict:
    """Everything the static page shows, as plain JSON-ready data."""
    valid = samples[samples["compliant"] & samples["required_rent"].notna()]
    if valid.empty:
        raise ValueError("no sampled variant is bank-compliant and feasible")
    rent = valid["required_rent"]
    threshold = rent.quantile(CHEAPEST_SHARE)
    cheapest = valid[rent <= threshold]
    best = valid.loc[rent.idxmin()]
    return {
        "meta": {
            "n": len(samples),
            "seed": seed,
            "excluded_bank": int((~samples["compliant"]).sum()),
            "infeasible": int((samples["compliant"] & samples["required_rent"].isna()).sum()),
            "base_rent": required_rent(build_scenario(p)),
            "defaults": asdict(p),
            "default_values": default_values(p),
            "ranges": {k: list(v) for k, v in PARAMETERS.items()},
            "min_equity_like_share": MIN_EQUITY_LIKE_SHARE,
            "cheapest_share": CHEAPEST_SHARE,
            "tolerance_eur": RENT_TOLERANCE_EUR,
        },
        "rent": {
            "min": float(rent.min()),
            "p05": float(threshold),
            "p10": float(rent.quantile(0.10)),
            "p50": float(rent.median()),
            "p90": float(rent.quantile(0.90)),
            "max": float(rent.max()),
        },
        "best": {name: float(best[name]) for name in PARAMETERS},
        "cheapest_median": {name: float(cheapest[name].median()) for name in PARAMETERS},
        "importance": _importance(valid).to_dict(orient="index"),
        "per_parameter": {
            name: _per_parameter(valid, name).to_dict(orient="list") for name in PARAMETERS
        },
        "pairs": _pairs(valid),
        "cheapest": {k: v.to_dict(orient="list") for k, v in _cheapest(valid).items()},
    }
