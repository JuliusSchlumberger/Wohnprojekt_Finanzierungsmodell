import numpy as np
import pytest

from model import required_rent
from model.presets import ProjectInputs, build_scenario
from model.uncertainty import (
    SAMPLE_RENT_TOLERANCE_EUR,
    Ranges,
    _triangular,
    latin_hypercube,
    rent_uncertainty,
)

N = 60


@pytest.fixture(scope="module")
def result():
    return rent_uncertainty(ProjectInputs(), Ranges(), n=N)


def test_latin_hypercube_puts_one_draw_in_each_probability_stratum():
    draws = latin_hypercube(ProjectInputs(), Ranges(), n=N)
    low, high = Ranges().vacancy_rate
    mode = ProjectInputs().vacancy_rate
    split = (mode - low) / (high - low)
    u = np.where(
        draws["vacancy_rate"] < mode,
        (draws["vacancy_rate"] - low) ** 2 / ((high - low) * (mode - low)),
        1 - (high - draws["vacancy_rate"]) ** 2 / ((high - low) * (high - mode)),
    )
    assert 0 < split < 1
    assert sorted(np.floor(u * N).astype(int)) == list(range(N))


def test_triangular_draws_match_closed_form_mean_and_median():
    values = _triangular(np.random.default_rng(0).random(200_000), 1.0, 2.0, 5.0)
    assert values.min() >= 1.0 and values.max() <= 5.0
    assert values.mean() == pytest.approx((1 + 2 + 5) / 3, abs=0.01)
    assert np.median(values) == pytest.approx(5 - np.sqrt(0.5 * 4 * 3), abs=0.01)


def test_same_seed_gives_same_result(result):
    again = rent_uncertainty(ProjectInputs(), Ranges(), n=N)
    assert again.rent_percentiles == result.rent_percentiles


def test_percentiles_are_ordered_and_safe_rent_is_the_90th(result):
    p = result.rent_percentiles
    assert p[10] <= p[50] <= p[90] == result.safe_rent
    assert result.base_rent == pytest.approx(required_rent(build_scenario(ProjectInputs())))


def test_ranges_collapsed_onto_current_inputs_reproduce_base_rent():
    p = ProjectInputs()
    fixed = Ranges(
        inflation=(p.inflation, p.inflation),
        bank_rate_change_pp=(1.0, 1.0),
        vacancy_rate=(p.vacancy_rate, p.vacancy_rate),
        renovation_factor=(1.0, 1.0),
        running_cost_factor=(1.0, 1.0),
    )
    res = rent_uncertainty(p, fixed, n=10)
    np.testing.assert_allclose(
        res.samples["required_rent"], res.base_rent, atol=SAMPLE_RENT_TOLERANCE_EUR + 0.01
    )


def test_costlier_renovation_raises_rent_and_ranks_as_positive_driver(result):
    assert result.sensitivity["renovation_factor"] > 0.3


def test_band_has_one_row_per_operating_year(result):
    assert len(result.headroom_band) == 50
    assert (result.headroom_band["p10"] <= result.headroom_band["p90"] + 1e-6).all()
