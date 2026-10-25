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


@pytest.mark.parametrize(
    "change",
    [
        {"admin_cost_per_year": 20_000.0},
        {"insurance_per_year": 20_000.0},
        {"min_liquidity_months": 12.0},
        {"ancillary_cost_rate": 0.15},
        {"max_arrears_years": 0},
        {"subsidy": 300_000.0, "subsidy_rate": 0.05},
        {"tenure": "leasehold", "leasehold_rate": 0.06},
    ],
)
def test_advanced_inputs_that_add_cost_raise_required_rent(change):
    base = {
        "subsidy": 300_000.0,
        "subsidy_rate": 0.0,
        "tenure": "leasehold",
        "leasehold_rate": 0.02,
    }
    base = {k: v for k, v in base.items() if k in change}
    assert required_rent(build_scenario(ProjectInputs(**change))) > required_rent(
        build_scenario(ProjectInputs(**base))
    )


def test_actual_maintenance_is_spent_from_reserve_without_changing_rent():
    cheap = build_scenario(ProjectInputs(maintenance_rate=0.010))
    dear = build_scenario(ProjectInputs(maintenance_rate=0.019))
    assert required_rent(cheap) == required_rent(dear)
    pot = {
        k: simulate(s, required_rent(s)).table.maintenance_reserve.iloc[-1]
        for k, s in (("cheap", cheap), ("dear", dear))
    }
    assert pot["cheap"] > pot["dear"]


def test_binding_year_is_where_a_slightly_lower_rent_fails():
    from model.solve import binding_year

    s = build_scenario(ProjectInputs())
    rent = required_rent(s)
    year, reason = binding_year(s, rent)
    assert (year, reason) == (1, "reserve")
    late = build_scenario(ProjectInputs(member_loan_term_years=10))
    assert binding_year(late, required_rent(late))[1] == "arrears"


def test_member_loan_term_moves_the_lump_repayment():
    for term in (10, 20):
        s = build_scenario(ProjectInputs(member_loan_term_years=term))
        ml = simulate(s, 900.0).tranches["member_loans"]
        assert int(ml["repayment"].idxmax()) == term
        assert ml["repayment"].max() == pytest.approx(400_000 * 1.05**term)


@pytest.mark.parametrize("payoff", ["bank", "direct_loans"])
def test_refinancing_pays_the_full_member_loan_due_at_year_end(payoff):
    p = ProjectInputs(member_loan_payoff=payoff)
    res = simulate(build_scenario(p), 950.0)
    (name,) = [n for n in res.tranches if n.endswith("_refinance")]
    refi, ml = res.tranches[name], res.tranches["member_loans"]
    term = p.member_loan_term_years
    assert refi["inflow"].loc[term] == pytest.approx(ml["repayment"].loc[term])
    assert refi["interest"].loc[term] == 0
    assert refi["interest"].loc[term + 1] > 0


def test_refinancing_is_not_part_of_the_opening_financing():
    from model.cashflow import capital_structure

    plain = capital_structure(build_scenario(ProjectInputs()), 900.0)
    refinanced = capital_structure(build_scenario(ProjectInputs(member_loan_payoff="bank")), 900.0)
    assert refinanced == plain


def test_refinanced_member_loans_release_surplus_instead_of_hoarding_cash():
    p = ProjectInputs()
    hoarded = {}
    for payoff in ("liquidity", "bank"):
        scenario = build_scenario(replace(p, member_loan_payoff=payoff))
        table = simulate(scenario, required_rent(scenario)).table
        hoarded[payoff] = table.loc[1 : p.member_loan_term_years - 1, "liquidity"].max()
    assert hoarded["bank"] < hoarded["liquidity"]
