from dataclasses import replace

import numpy as np
import pytest

from model import required_rent, simulate
from model.member import MemberInputs, member_view
from model.presets import ProjectInputs, build_scenario


@pytest.fixture(scope="module")
def project():
    s = build_scenario(ProjectInputs())
    return s, simulate(s, required_rent(s))


def test_alternative_grows_at_real_alternative_return(project):
    s, res = project
    view = member_view(s, res, MemberInputs(alt_return=0.05))
    growth = view["alternative"].iloc[1:].to_numpy() / view["alternative"].iloc[:-1].to_numpy()
    cidx = res.table["cost_index"].loc[view.index].to_numpy()
    np.testing.assert_allclose(growth, 1.05 / (cidx[1:] / cidx[:-1]))


def test_default_path_lacks_only_the_equity_while_member_stays(project):
    s, res = project
    view = member_view(s, res, MemberInputs(equity=10_000, member_loan=0.0))
    held = view["project"] - view["default"]
    np.testing.assert_allclose(held, 10_000 * res.table["cost_index"].loc[1])


def test_member_loan_is_repaid_with_interest_after_15_years(project):
    s, res = project
    base = MemberInputs(
        equity=0.0, member_loan=0.0, member_loan_rate=0.06, alt_return=0.0, exit_year=50
    )
    with_loan = replace(base, member_loan=10_000.0)
    diff = member_view(s, res, with_loan)["project"] - member_view(s, res, base)["project"]
    deflator = res.table["cost_index"] / res.table["cost_index"].loc[1]
    assert diff.loc[14] == pytest.approx(10_000 * 1.06**14 / deflator.loc[14])
    assert diff.loc[15] == pytest.approx(10_000 * 1.06**15 / deflator.loc[15])
    assert diff.loc[30] == pytest.approx(10_000 * 1.06**15 / deflator.loc[30])


def test_exit_returns_equity_indexed_and_ends_series(project):
    s, res = project
    view = member_view(s, res, MemberInputs(equity=10_000, entry_year=5, exit_year=20))
    assert view.index[0] == 5 and view.index[-1] == 21
    assert view["rent_saving_month"].loc[21] == 0


def test_invalid_years_raise(project):
    s, res = project
    with pytest.raises(ValueError):
        member_view(s, res, MemberInputs(entry_year=20, exit_year=10))


def test_personal_member_loan_follows_the_chosen_term(project):
    s, res = project
    base = MemberInputs(equity=0.0, member_loan=0.0, alt_return=0.0, exit_year=50)
    with_loan = replace(base, member_loan=10_000.0, member_loan_rate=0.05, member_loan_term_years=8)
    diff = member_view(s, res, with_loan)["project"] - member_view(s, res, base)["project"]
    deflator = res.table["cost_index"] / res.table["cost_index"].loc[1]
    assert diff.loc[20] == pytest.approx(10_000 * 1.05**8 / deflator.loc[20])


def test_break_even_grid_matches_direct_evaluation(project):
    from model.member import break_even_grid, break_even_rent

    s, res = project
    m = MemberInputs()
    grid = break_even_grid(s, res, m, np.array([500.0, 950.0, 1400.0]), np.array([-1.0, 2.0]))
    direct = member_view(
        s, res, replace(m, market_rent=950.0, alt_return=m.member_loan_rate + 0.02)
    )
    assert grid.loc[2.0, 950.0] == pytest.approx(direct["advantage"].iloc[-1])
    at_break_even = member_view(s, res, replace(m, market_rent=break_even_rent(s, res, m)))
    assert at_break_even["advantage"].iloc[-1] == pytest.approx(0.0, abs=1e-6)
