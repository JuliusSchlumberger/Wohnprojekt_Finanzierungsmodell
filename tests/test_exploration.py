import numpy as np
import pandas as pd
import pytest

from model.exploration import (
    PARAMETERS,
    apply_draw,
    bank_compliant,
    default_values,
    explore,
    latin_hypercube,
    summarize,
)
from model.presets import ProjectInputs

N = 120


@pytest.fixture(scope="module")
def samples():
    return explore(ProjectInputs(), latin_hypercube(N, seed=3))


def test_draws_stay_within_ranges_and_terms_are_whole_years():
    draws = latin_hypercube(2_000, seed=1)
    for name, (low, high) in PARAMETERS.items():
        assert draws[name].between(low, high).all(), name
    terms = draws["member_loan_term_years"]
    assert set(terms) == set(range(15, 31))


def test_default_values_reproduce_the_defaults():
    p = ProjectInputs()
    assert apply_draw(p, pd.Series(default_values(p))) == p


def test_variants_without_subordinated_loans_fail_the_bank_rule():
    p = ProjectInputs()
    draw = pd.Series({**default_values(p), "member_loan_share": 0.0, "direct_loans_10y_share": 0.0})
    assert not bank_compliant(apply_draw(p, draw))
    assert bank_compliant(p)


def test_higher_bank_spread_needs_a_higher_rent():
    p = ProjectInputs()
    base = default_values(p)
    draws = pd.DataFrame([{**base, "bank_spread_pp": 2.0}, {**base, "bank_spread_pp": 6.0}])
    rents = explore(p, draws)["required_rent"]
    assert rents.iloc[1] > rents.iloc[0]


def test_excluded_variants_have_no_rent(samples):
    assert samples.loc[~samples["compliant"], "required_rent"].isna().all()
    assert samples.loc[samples["compliant"], "required_rent"].notna().all()


def test_summary_is_consistent(samples):
    s = summarize(ProjectInputs(), samples, seed=3)
    assert s["meta"]["n"] == N
    r = s["rent"]
    assert r["min"] <= r["p05"] <= r["p10"] <= r["p50"] <= r["p90"] <= r["max"]
    assert len(s["pairs"]) == len(PARAMETERS) * (len(PARAMETERS) - 1) // 2
    for row in s["importance"].values():
        assert 0 <= row["linear"] <= row["total"] <= 1 + 1e-9
    for curve in s["per_parameter"].values():
        valid = ~np.isnan(curve["p50"])
        assert (np.array(curve["min"])[valid] <= np.array(curve["p50"])[valid]).all()
    for shares in s["cheapest"].values():
        assert sum(shares["all"]) == pytest.approx(1.0)
        assert sum(shares["cheapest"]) == pytest.approx(1.0)
