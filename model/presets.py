"""Scenario builders; `ProjectInputs` is the app's input set, `example_scenario` the baseline."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from model.types import MemberType, Operations, Property, Rules, Scenario, Tranche

Tenure = Literal["purchase", "leasehold"]
SurplusUse = Literal["rent_reduction", "payout_15y", "next_project"]
RentMode = Literal["indexed", "fixed"]

BANK_RATE_CHANGE_STEP = 0.01
MEMBER_LOAN_TERM_YEARS = 15


@dataclass(frozen=True)
class ProjectInputs:
    """User-facing inputs; amounts in EUR, rates as fractions per year.

    Purchase costs (`ancillary_cost_rate`) apply to land and house, the land
    only when bought. Under leasehold the land price is the ground value on
    which the ground rent is charged. Direct loans run 5 or 10 years with
    yearly interest, member loans 15 years with accrued interest; all are
    repaid at term; repayments that would push liquidity below the reserve
    are deferred and paid as soon as possible, within 3 years. Maintenance is
    paid from a reserve fed with `maintenance_reserve_rate` of the replacement
    value. Once no arrears are open, liquidity above reserve plus all
    outstanding direct and member loans goes to the A4 use. The first 3
    operating years carry `initial_vacancy_rate` instead of `vacancy_rate`.
    `bank_rate_change` is -1, 0 or +1 steps of `BANK_RATE_CHANGE_STEP`
    applied after the 10-year fixed-rate period.
    """

    land_price: float = 540_000.0
    building_price: float = 1_260_000.0
    renovation_cost: float = 420_000.0
    ancillary_cost_rate: float = 0.10
    tenure: Tenure = "purchase"
    persons: int = 20
    equity: float = 40_000.0
    member_loans: float = 400_000.0
    member_loan_rate: float = 0.05
    direct_loans_5y: float = 50_000.0
    direct_loan_rate_5y: float = 0.025
    direct_loans_10y: float = 150_000.0
    direct_loan_rate_10y: float = 0.04
    subsidy: float = 0.0
    bank_rate: float = 0.06
    bank_repayment: Literal["annuity", "linear"] = "annuity"
    bank_term_years: int = 30
    bank_rate_change: Literal[-1, 0, 1] = 1
    inflation: float = 0.02
    vacancy_rate: float = 0.04
    initial_vacancy_rate: float = 0.20
    maintenance_reserve_rate: float = 0.02
    surplus_use: SurplusUse = "rent_reduction"

    @property
    def ancillary_cost(self) -> float:
        bought = self.building_price
        if self.tenure == "purchase":
            bought += self.land_price
        return self.ancillary_cost_rate * bought

    @property
    def total_investment(self) -> float:
        return build_scenario(self).property.total_investment

    @property
    def direct_loans(self) -> float:
        return self.direct_loans_5y + self.direct_loans_10y

    @property
    def own_funds(self) -> float:
        return self.equity_like + self.subsidy

    @property
    def equity_like(self) -> float:
        """Member equity plus subordinated member and direct loans."""
        return self.equity + self.member_loans + self.direct_loans

    def scaled_to(self, total_investment: float) -> ProjectInputs:
        """Same project with land, house and renovation scaled to `total_investment`."""
        k = total_investment / self.total_investment
        return replace(
            self,
            land_price=k * self.land_price,
            building_price=k * self.building_price,
            renovation_cost=k * self.renovation_cost,
        )


def build_scenario(p: ProjectInputs) -> Scenario:
    """Scenario for the app inputs; the bank loan closes the gap incl. opening liquidity."""
    if p.persons < 1:
        raise ValueError("at least one person required")
    purchase_price = p.land_price + p.building_price
    if purchase_price <= 0:
        raise ValueError("land and building price must not both be zero")
    if min(p.equity, p.member_loans, p.direct_loans_5y, p.direct_loans_10y, p.subsidy) < 0:
        raise ValueError("financing amounts must not be negative")
    prop = Property(
        purchase_price=purchase_price,
        renovation_cost=p.renovation_cost,
        ancillary_cost_rate=p.ancillary_cost_rate,
        tenure=p.tenure,
        ground_share=p.land_price / purchase_price,
    )
    subordinated = [
        Tranche(
            name="member_loans",
            kind="member_loan",
            amount=p.member_loans,
            interest_rate=p.member_loan_rate,
            repayment="bullet",
            term_years=MEMBER_LOAN_TERM_YEARS,
            interest_mode="accrued",
        ),
        Tranche(
            name="direct_loans_5y",
            kind="direct_loan",
            amount=p.direct_loans_5y,
            interest_rate=p.direct_loan_rate_5y,
            repayment="bullet",
            term_years=5,
        ),
        Tranche(
            name="direct_loans_10y",
            kind="direct_loan",
            amount=p.direct_loans_10y,
            interest_rate=p.direct_loan_rate_10y,
            repayment="bullet",
            term_years=10,
        ),
    ]
    senior = [
        Tranche(
            name="subsidy",
            kind="subsidy_loan",
            amount=p.subsidy,
            interest_rate=0.015,
            repayment="annuity",
            term_years=30,
        ),
        Tranche(
            name="bank",
            kind="bank_loan",
            interest_rate=p.bank_rate,
            repayment=p.bank_repayment,
            term_years=p.bank_term_years,
            fixed_rate_years=10,
            follow_up_rate=max(p.bank_rate + p.bank_rate_change * BANK_RATE_CHANGE_STEP, 0.0),
            residual=True,
        ),
    ]
    return Scenario(
        property=prop,
        member_types=[MemberType(count=p.persons, equity_contribution=p.equity / p.persons)],
        tranches=[tr for tr in subordinated if tr.amount] + senior,
        operations=Operations(
            inflation=p.inflation,
            maintenance_reserve_rate=p.maintenance_reserve_rate,
            vacancy_rate=p.vacancy_rate,
            initial_vacancy_rate=p.initial_vacancy_rate,
        ),
        rules=Rules(surplus_use=p.surplus_use, redirect_surplus=True, defer_repayments=True),
    )


def property_for_investment(total_investment: float, tenure: Tenure = "purchase") -> Property:
    """Default property scaled so that `total_investment` equals the financed investment.

    Keeps the default ratio of renovation cost to purchase price. Under
    leasehold the land is not bought, so the purchase price is scaled up.
    """
    base = Property(tenure=tenure)
    renovation_ratio = base.renovation_cost / base.purchase_price
    bought = 1 - base.ground_share if tenure == "leasehold" else 1.0
    price = total_investment / (bought * (1 + base.ancillary_cost_rate) + renovation_ratio)
    return Property(purchase_price=price, renovation_cost=renovation_ratio * price, tenure=tenure)


def scenario_from_shares(
    total_investment: float | None = None,
    persons: int = 20,
    equity_share: float = 0.06,
    direct_loan_share: float = 0.19,
    subsidy_share: float = 0.15,
    bank_rate: float = 0.038,
    tenure: Tenure = "purchase",
    surplus_use: SurplusUse = "rent_reduction",
    rent_mode: RentMode = "indexed",
) -> Scenario:
    """Scenario from financing shares (fractions of total investment); bank closes the gap.

    Direct loans are never cancelled; the bank loan is a 2 % initial-repayment
    annuity. `total_investment=None` keeps the default property.
    """
    if equity_share + direct_loan_share + subsidy_share > 1:
        raise ValueError("equity, direct loan and subsidy shares exceed 100 %")
    if persons < 1:
        raise ValueError("at least one person required")
    if total_investment is None:
        prop = Property(tenure=tenure)
    else:
        prop = property_for_investment(total_investment, tenure)
    total = prop.total_investment
    return Scenario(
        property=prop,
        member_types=[
            MemberType(count=persons, equity_contribution=equity_share * total / persons)
        ],
        tranches=[
            Tranche(
                name="direct_loans",
                kind="direct_loan",
                amount=direct_loan_share * total,
                interest_rate=0.01,
            ),
            Tranche(
                name="subsidy",
                kind="subsidy_loan",
                amount=subsidy_share * total,
                interest_rate=0.015,
                repayment="annuity",
                term_years=30,
            ),
            Tranche(
                name="bank",
                kind="bank_loan",
                interest_rate=bank_rate,
                repayment="annuity",
                initial_repayment_rate=0.02,
                fixed_rate_years=10,
                follow_up_rate=bank_rate,
                residual=True,
            ),
        ],
        operations=Operations(rent_mode=rent_mode),
        rules=Rules(surplus_use=surplus_use),
    )


def example_scenario() -> Scenario:
    """2.4 M EUR, 1000 m2, 20 persons: 6 % equity, 19 % direct loans, 15 % subsidy, rest bank."""
    return scenario_from_shares()
