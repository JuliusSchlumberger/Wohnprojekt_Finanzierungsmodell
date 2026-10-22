from dataclasses import replace

import numpy as np
import pytest

from model import simulate
from model.presets import example_scenario
from model.types import Rules, Scenario

RENT = 28.0


def _with_rules(s: Scenario, **kw) -> Scenario:
    return replace(s, rules=Rules(**kw))


def test_liquidity_identity_holds_every_year():
    tb = simulate(example_scenario(), RENT).table
    flows = (
        tb.rent_income
        - tb.operating
        - tb.debt_service
        + tb.loan_inflow
        - tb.payout
        - tb.transfer_out
    )
    np.testing.assert_allclose(tb.liquidity.diff()[1:], flows[1:], atol=1e-6)


def test_senior_loans_fully_repaid_within_horizon():
    res = simulate(example_scenario(), RENT)
    for name in ("bank", "subsidy"):
        tr = res.tranches[name]
        assert tr.repayment.sum() == pytest.approx(tr.balance.iloc[0])
        assert tr.balance.iloc[-1] == pytest.approx(0, abs=1e-6)


def test_opening_liquidity_is_six_months_rent_financed_by_bank():
    s = example_scenario()
    res = simulate(s, RENT)
    reserve = 0.5 * RENT * s.private_area_m2_total * 12 * (1 + s.operations.inflation)
    assert res.metrics["opening_liquidity"] == pytest.approx(reserve)
    sources = sum(df.balance.iloc[0] for df in res.tranches.values())
    assert sources == pytest.approx(s.property.total_investment + reserve)


def test_financing_gap_without_residual_raises():
    s = example_scenario()
    s.tranches[-1] = replace(s.tranches[-1], residual=False, amount=1.0)
    with pytest.raises(ValueError, match="sources"):
        simulate(s, RENT)


def test_leasehold_lowers_investment_and_adds_ground_rent():
    s = example_scenario()
    lease = replace(s, property=replace(s.property, tenure="leasehold"))
    assert lease.property.total_investment < s.property.total_investment
    tb = simulate(lease, RENT).table
    assert (tb.ground_rent[1:] > 0).all()
    assert simulate(s, RENT).table.ground_rent.sum() == 0


def test_surplus_modes_differ_only_after_senior_payoff():
    s = example_scenario()
    runs = {
        mode: simulate(_with_rules(s, surplus_use=mode), RENT)
        for mode in ("rent_reduction", "payout_15y", "next_project")
    }
    payoff = int(runs["next_project"].metrics["senior_payoff_year"])
    liq = {m: r.table.liquidity for m, r in runs.items()}
    for m in liq:
        np.testing.assert_allclose(liq[m][: payoff + 1], liq["next_project"][: payoff + 1])

    after = runs["rent_reduction"].table.loc[payoff + 1 :]
    assert (after.rent_reduction > 0).all()
    assert (runs["next_project"].table.transfer_out.loc[payoff + 1 :] > 0).all()

    payout = runs["payout_15y"].table.payout
    assert set(payout[payout > 0].index) <= {15, 30, 45}
    transfers = runs["next_project"].table.transfer_out
    assert payout.sum() == pytest.approx(transfers.loc[:45].sum())


def test_fixed_rent_mode_keeps_rent_constant():
    s = example_scenario()
    s = replace(s, operations=replace(s.operations, rent_mode="fixed"))
    tb = simulate(s, RENT).table
    assert tb.gross_rent[1:].nunique() == 1
