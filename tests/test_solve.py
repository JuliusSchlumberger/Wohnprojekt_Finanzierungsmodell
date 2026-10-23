import time
from dataclasses import replace

import numpy as np
import pytest

from model.cashflow import min_headroom, simulate
from model.presets import ProjectInputs, build_scenario, example_scenario, scenario_from_shares
from model.solve import max_investment, required_rent


def _acceptance_scenario():
    """Spec section 7: only maintenance as running cost."""
    s = example_scenario()
    return replace(s, operations=replace(s.operations, admin_cost_per_year=0, insurance_per_year=0))


def test_acceptance_rent_per_total_m2_between_10_and_11():
    s = _acceptance_scenario()
    rent_total = required_rent(s) * s.persons / s.property.total_area_m2
    assert 10.0 <= rent_total <= 11.0


def test_required_rent_is_tight():
    s = example_scenario()
    rent = required_rent(s)
    assert min_headroom(s, rent) >= 0
    assert min_headroom(s, rent - 0.02) < 0


def test_required_rent_rises_with_bank_rate():
    s = example_scenario()
    bank = s.tranches[-1]
    dearer = replace(
        s, tranches=[*s.tranches[:-1], replace(bank, interest_rate=0.05, follow_up_rate=0.05)]
    )
    assert required_rent(dearer) > required_rent(s)


def test_required_rent_falls_with_equity_share():
    s = example_scenario()
    m = s.member_types[0]
    richer = replace(s, member_types=[replace(m, equity_contribution=3 * m.equity_contribution)])
    assert required_rent(richer) < required_rent(s)


def test_infeasible_bracket_raises():
    with pytest.raises(ValueError, match="rent above"):
        required_rent(example_scenario(), bracket=(0.0, 5.0))


def test_required_rent_under_half_second():
    t0 = time.perf_counter()
    required_rent(example_scenario())
    assert time.perf_counter() - t0 < 0.5


def test_scenario_from_shares_matches_requested_investment_under_leasehold():
    s = scenario_from_shares(3_000_000, tenure="leasehold")
    assert s.property.total_investment == pytest.approx(3_000_000)
    assert s.property.tenure == "leasehold"


def test_build_scenario_charges_purchase_costs_on_land_only_when_bought():
    bought = ProjectInputs()
    leased = ProjectInputs(tenure="leasehold")
    assert bought.total_investment == pytest.approx((540_000 + 1_260_000) * 1.1 + 420_000)
    assert leased.total_investment == pytest.approx(1_260_000 * 1.1 + 420_000)
    assert leased.ancillary_cost == pytest.approx(126_000)


def test_bank_rate_change_moves_follow_up_rate_by_one_point():
    bank = build_scenario(ProjectInputs(bank_rate_change=1)).tranches[-1]
    assert bank.rate_in_year(11) == pytest.approx(bank.rate_in_year(10) + 0.01)


def _app_defaults():
    s = build_scenario(ProjectInputs())
    return s, simulate(s, required_rent(s)).table


def test_arrears_arise_only_on_due_dates_and_are_cleared_within_three_years():
    _, tb = _app_defaults()
    late = tb.arrears_new > 0
    assert late.any()
    assert (tb.sub_due[late] > 0).all()
    assert tb.arrears_overdue.max() == 0
    assert tb.arrears.iloc[-1] == 0


def test_arrears_are_paid_back_in_full_with_interest():
    _, tb = _app_defaults()
    assert tb.arrears_paid.sum() == pytest.approx(tb.arrears_new.sum())
    assert tb.arrears_interest.sum() > 0


def test_deferring_repayments_lowers_required_rent():
    s, _ = _app_defaults()
    strict = replace(s, rules=replace(s.rules, defer_repayments=False))
    assert required_rent(s) < required_rent(strict)


def test_surplus_only_once_arrears_cleared_and_open_loans_covered():
    s, tb = _app_defaults()
    res = simulate(s, required_rent(s))
    open_loans = sum(
        df["balance"] for n, df in res.tranches.items() if n.startswith(("direct", "member"))
    )
    taken = tb.surplus > 0
    assert taken.any()
    assert (tb.arrears[taken] == 0).all()
    np.testing.assert_allclose(
        tb.liquidity[taken], (tb.reserve_required + open_loans)[taken], rtol=1e-9
    )


def test_member_loan_is_repaid_with_compound_interest_after_15_years():
    s = build_scenario(ProjectInputs(member_loans=100_000, member_loan_rate=0.06))
    ml = simulate(s, 600.0).tranches["member_loans"]
    assert ml["repayment"].loc[15] == pytest.approx(100_000 * 1.06**15)
    assert ml["repayment"].drop(15).sum() == 0


def _by_investment(total_investment):
    return build_scenario(ProjectInputs().scaled_to(total_investment))


def test_max_investment_inverts_required_rent():
    base = ProjectInputs()
    rent = required_rent(build_scenario(base))
    investment = max_investment(_by_investment, rent, base.own_funds)
    assert investment == pytest.approx(base.total_investment, abs=2_000)


def test_max_investment_rises_with_target_rent():
    own = ProjectInputs().own_funds
    assert max_investment(_by_investment, 400.0, own) < max_investment(_by_investment, 600.0, own)


def test_max_investment_rejects_rent_too_low_for_own_funds():
    with pytest.raises(ValueError):
        max_investment(_by_investment, 1.0, ProjectInputs().own_funds)
