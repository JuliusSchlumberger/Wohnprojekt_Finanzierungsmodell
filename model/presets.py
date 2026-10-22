"""Built-in scenarios; `example_scenario` is the app's start state."""

from __future__ import annotations

from model.types import MemberType, Property, Scenario, Tranche


def example_scenario() -> Scenario:
    """2.4 M EUR, 1000 m2, 20 persons: 6 % equity, 19 % direct loans, 15 % subsidy, rest bank."""
    prop = Property()
    total = prop.total_investment
    persons = 20
    return Scenario(
        property=prop,
        member_types=[
            MemberType(
                count=persons, private_area_m2=20.0, equity_contribution=0.06 * total / persons
            )
        ],
        tranches=[
            Tranche(
                name="direct_loans", kind="direct_loan", amount=0.19 * total, interest_rate=0.01
            ),
            Tranche(
                name="subsidy",
                kind="subsidy_loan",
                amount=0.15 * total,
                interest_rate=0.015,
                repayment="annuity",
                term_years=30,
            ),
            Tranche(
                name="bank",
                kind="bank_loan",
                interest_rate=0.038,
                repayment="annuity",
                initial_repayment_rate=0.02,
                fixed_rate_years=10,
                follow_up_rate=0.038,
                residual=True,
            ),
        ],
    )
