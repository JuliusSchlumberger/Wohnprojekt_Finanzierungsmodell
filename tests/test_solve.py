import time
from dataclasses import replace

import pytest

from model.cashflow import min_headroom
from model.presets import example_scenario
from model.solve import required_rent


def _acceptance_scenario():
    """Spec section 7: only maintenance as running cost."""
    s = example_scenario()
    return replace(s, operations=replace(s.operations, admin_cost_per_year=0, insurance_per_year=0))


def test_acceptance_rent_per_total_m2_between_10_and_11():
    s = _acceptance_scenario()
    rent_private = required_rent(s)
    rent_total = rent_private * s.private_area_m2_total / s.property.total_area_m2
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
