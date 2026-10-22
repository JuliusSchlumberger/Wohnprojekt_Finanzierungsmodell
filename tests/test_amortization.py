import numpy as np
import pytest

from model.cashflow import tranche_schedule
from model.types import Tranche

P, R, N = 100_000.0, 0.04, 20


def pmt(principal: float, rate: float, n: float) -> float:
    return principal * rate / (1 - (1 + rate) ** -n)


def test_annuity_payment_matches_pmt_and_repays_principal():
    s = tranche_schedule(Tranche("a", "bank_loan", P, R, "annuity", term_years=N), horizon=30)
    payment = s.interest_paid[1 : N + 1] + s.repayment[1 : N + 1]
    np.testing.assert_allclose(payment, pmt(P, R, N), rtol=1e-9)
    assert s.repayment.sum() == pytest.approx(P)
    assert s.balance[N] == pytest.approx(0, abs=1e-6)
    assert s.cash_out[N + 1 :].sum() == 0


def test_annuity_zero_rate_is_linear():
    s = tranche_schedule(Tranche("a", "bank_loan", P, 0.0, "annuity", term_years=N), horizon=N)
    np.testing.assert_allclose(s.repayment[1:], P / N)


def test_linear_repayment_constant_and_complete():
    s = tranche_schedule(Tranche("l", "bank_loan", P, R, "linear", term_years=N), horizon=30)
    np.testing.assert_allclose(s.repayment[1 : N + 1], P / N)
    assert s.repayment.sum() == pytest.approx(P)
    np.testing.assert_allclose(s.interest[1 : N + 1], R * (P - P / N * np.arange(N)))


def test_grace_years_interest_only_then_annuity_over_remaining_term():
    g = 3
    s = tranche_schedule(
        Tranche("g", "subsidy_loan", P, R, "annuity", term_years=N, grace_years=g), horizon=30
    )
    assert s.repayment[1 : g + 1].sum() == 0
    np.testing.assert_allclose(s.interest_paid[1 : g + 1], P * R)
    np.testing.assert_allclose(s.cash_out[g + 1 : N + 1], pmt(P, R, N - g), rtol=1e-9)
    assert s.balance[N] == pytest.approx(0, abs=1e-6)


def test_bullet_repays_everything_at_term():
    s = tranche_schedule(Tranche("b", "member_loan", P, R, "bullet", term_years=10), horizon=15)
    assert s.repayment[10] == pytest.approx(P)
    assert s.repayment.sum() == pytest.approx(P)


def test_bullet_with_accrued_interest_repays_compounded_amount():
    s = tranche_schedule(
        Tranche("b", "member_loan", P, R, "bullet", term_years=10, interest_mode="accrued"),
        horizon=15,
    )
    assert s.interest_paid.sum() == 0
    assert s.repayment[10] == pytest.approx(P * (1 + R) ** 10)


def test_initial_repayment_rate_sets_first_year_repayment():
    s = tranche_schedule(
        Tranche("i", "bank_loan", P, 0.038, "annuity", initial_repayment_rate=0.02), horizon=50
    )
    assert s.repayment[1] == pytest.approx(0.02 * P)
    assert s.repayment.sum() == pytest.approx(P)
    assert 28 < np.argmax(s.balance[1:] <= 1e-6) + 1 <= 30


def test_rate_reset_keeps_payoff_year():
    base = Tranche("r", "bank_loan", P, R, "annuity", term_years=N)
    reset = Tranche(
        "r", "bank_loan", P, R, "annuity", term_years=N, fixed_rate_years=10, follow_up_rate=0.07
    )
    s0, s1 = tranche_schedule(base, 30), tranche_schedule(reset, 30)
    np.testing.assert_allclose(s1.cash_out[1:11], s0.cash_out[1:11])
    assert s1.cash_out[11] > s0.cash_out[11]
    assert s1.balance[N] == pytest.approx(0, abs=1e-6)


def test_direct_loan_churn_shrinks_balance_geometrically():
    churn, repl = 0.05, 0.6
    s = tranche_schedule(
        Tranche("d", "direct_loan", P, 0.01, churn_rate=churn, replacement_rate=repl), horizon=10
    )
    t = np.arange(11)
    np.testing.assert_allclose(s.balance, P * (1 - churn * (1 - repl)) ** t)
    np.testing.assert_allclose(s.inflow[1:], repl * s.repayment[1:])


def test_later_drawdown_charges_interest_from_drawdown_year():
    s = tranche_schedule(
        Tranche("d", "bank_loan", P, R, "annuity", term_years=N, drawdown_year=2), horizon=30
    )
    assert s.interest[1] == 0 and s.inflow[2] == P
    assert s.interest[2] == pytest.approx(P * R)
    assert s.repayment.sum() == pytest.approx(P)


def test_subsidy_grant_reduces_repaid_principal():
    grant = 10_000.0
    s = tranche_schedule(
        Tranche("s", "subsidy_loan", P, R, "annuity", term_years=N, subsidy_grant=grant),
        horizon=30,
    )
    assert s.repayment.sum() == pytest.approx(P - grant)
