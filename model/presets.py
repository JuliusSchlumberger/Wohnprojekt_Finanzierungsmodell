"""Scenario builders; `ProjectInputs` is the app's input set, `example_scenario` the baseline."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from model.types import MemberType, Operations, Property, Rules, Scenario, Tranche

Tenure = Literal["purchase", "leasehold"]
SurplusUse = Literal["rent_reduction", "payout_15y", "next_project"]
MemberLoanPayoff = Literal["liquidity", "bank", "direct_loans"]
RentMode = Literal["indexed", "fixed"]

BANK_RATE_CHANGE_STEP = 0.01


@dataclass(frozen=True)
class ProjectInputs:
    """User-facing inputs; amounts in EUR, rates as fractions per year.

    Purchase costs (`ancillary_cost_rate`) apply to land and house, the land
    only when bought. Under leasehold the land price is the ground value on
    which the ground rent is charged. Direct loans run 5 or 10 years with
    yearly interest, member loans `member_loan_term_years` with accrued interest; all are
    repaid at term; repayments that would push liquidity below the reserve
    are deferred and paid as soon as possible, within `max_arrears_years`. Maintenance
    costs `maintenance_reserve_rate` of the replacement value each year, put aside
    and spent in the same year. Once no arrears are open, liquidity above reserve plus all
    outstanding direct and member loans goes to the A4 use. The first 3
    operating years carry `initial_vacancy_rate` instead of `vacancy_rate`.
    `member_loan_payoff` decides how member loans are repaid when due: from
    liquidity (with the arrears rule), or by a new bank loan (follow-up rate,
    remaining bank term, at least 10 years) or new 10-year direct loans that
    take up the full amount due at the end of the maturity year.
    At each maturity of 10-year direct loans `direct_loan_rollover_rate` of
    the balance is re-lent for another 10 years; 5-year loans are repaid.
    `bank_rate_change` counts steps of `BANK_RATE_CHANGE_STEP` (the app offers -1, 0, +1)
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
    member_loan_term_years: int = 15
    member_loan_payoff: MemberLoanPayoff = "liquidity"
    direct_loans_5y: float = 50_000.0
    direct_loan_rate_5y: float = 0.03
    direct_loans_10y: float = 150_000.0
    direct_loan_rate_10y: float = 0.04
    direct_loan_rollover_rate: float = 0.5
    subsidy: float = 0.0
    bank_rate: float = 0.06
    bank_repayment: Literal["annuity", "linear"] = "annuity"
    bank_term_years: int = 30
    bank_rate_change: float = 1
    inflation: float = 0.02
    vacancy_rate: float = 0.04
    initial_vacancy_rate: float = 0.10
    maintenance_reserve_rate: float = 0.02
    surplus_use: SurplusUse = "rent_reduction"
    admin_cost_per_year: float = 4_000.0
    insurance_per_year: float = 2_500.0
    min_liquidity_months: float = 6.0
    leasehold_rate: float = 0.04
    subsidy_rate: float = 0.015
    subsidy_term_years: int = 30
    max_arrears_years: int = 3

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
        leasehold_rate=p.leasehold_rate,
    )
    subordinated = [
        Tranche(
            name="member_loans",
            kind="member_loan",
            amount=p.member_loans,
            interest_rate=p.member_loan_rate,
            repayment="bullet",
            term_years=p.member_loan_term_years,
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
            rollover_rate=p.direct_loan_rollover_rate,
        ),
    ]
    senior = [
        Tranche(
            name="subsidy",
            kind="subsidy_loan",
            amount=p.subsidy,
            interest_rate=p.subsidy_rate,
            repayment="annuity",
            term_years=p.subsidy_term_years,
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
    refinancing = _member_loan_refinancing(p)
    return Scenario(
        property=prop,
        member_types=[MemberType(count=p.persons, equity_contribution=p.equity / p.persons)],
        tranches=[tr for tr in subordinated if tr.amount] + senior + refinancing,
        operations=Operations(
            inflation=p.inflation,
            vacancy_rate=p.vacancy_rate,
            initial_vacancy_rate=p.initial_vacancy_rate,
            maintenance_rate=p.maintenance_reserve_rate,
            admin_cost_per_year=p.admin_cost_per_year,
            insurance_per_year=p.insurance_per_year,
            min_liquidity_months=p.min_liquidity_months,
        ),
        rules=Rules(
            surplus_use=p.surplus_use,
            redirect_surplus=True,
            defer_repayments=True,
            max_arrears_years=p.max_arrears_years,
        ),
    )


def _member_loan_refinancing(p: ProjectInputs) -> list[Tranche]:
    """New loan that pays off the member loans when they fall due, if chosen."""
    if p.member_loan_payoff == "liquidity" or not p.member_loans:
        return []
    due = p.member_loans * (1 + p.member_loan_rate) ** p.member_loan_term_years
    timing = {"drawdown_year": p.member_loan_term_years, "year_end_drawdown": True}
    if p.member_loan_payoff == "bank":
        follow_up = max(p.bank_rate + p.bank_rate_change * BANK_RATE_CHANGE_STEP, 0.0)
        return [
            Tranche(
                name="bank_refinance",
                kind="bank_loan",
                amount=due,
                interest_rate=follow_up,
                repayment=p.bank_repayment,
                term_years=max(p.bank_term_years - p.member_loan_term_years, 10),
                **timing,
            )
        ]
    return [
        Tranche(
            name="direct_loans_refinance",
            kind="direct_loan",
            amount=due,
            interest_rate=p.direct_loan_rate_10y,
            repayment="bullet",
            term_years=10,
            rollover_rate=p.direct_loan_rollover_rate,
            **timing,
        )
    ]


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
