"""Scenario dataclasses; all monetary amounts in nominal euros, rates as fractions per year."""

from __future__ import annotations

import builtins
from dataclasses import dataclass, field
from typing import Literal

TrancheKind = Literal["equity", "member_loan", "direct_loan", "subsidy_loan", "bank_loan"]
Repayment = Literal["annuity", "linear", "bullet", "none"]
InterestMode = Literal["paid", "accrued"]


@dataclass
class Property:
    """House and land; under leasehold the land share is rented, not bought.

    `ancillary_cost_rate` applies to the purchased part of the price.
    `replacement_value_ratio` scales purchase price plus renovation to the
    rebuild value on which maintenance is charged.
    """

    purchase_price: float = 1_800_000.0
    renovation_cost: float = 420_000.0
    ancillary_cost_rate: float = 0.10
    tenure: Literal["purchase", "leasehold"] = "purchase"
    ground_share: float = 0.3
    leasehold_rate: float = 0.04
    total_area_m2: float = 1000.0
    replacement_value_ratio: float = 0.6
    start_year: int = 2026

    @property
    def ground_value(self) -> float:
        return self.purchase_price * self.ground_share

    @property
    def purchased_price(self) -> float:
        if self.tenure == "leasehold":
            return self.purchase_price - self.ground_value
        return self.purchase_price

    @property
    def total_investment(self) -> float:
        price = self.purchased_price
        return price * (1 + self.ancillary_cost_rate) + self.renovation_cost

    @property
    def replacement_value(self) -> float:
        return self.replacement_value_ratio * (self.purchase_price + self.renovation_cost)


@dataclass
class Tranche:
    """One financing source.

    `drawdown_year` 0 means paid in before the first operating year; with
    `year_end_drawdown` the amount comes in at the end of `drawdown_year` and
    service starts the following year. Later drawdowns are not part of the
    opening financing. A loan
    with `residual=True` takes whatever amount closes the financing gap
    (investment plus initial reserve minus all other sources); its `amount`
    is ignored. With `initial_repayment_rate` set, an annuity loan's term is
    implied by rate plus initial repayment ("3.8 % / 2 % Tilgung") and
    `term_years` is ignored.
    """

    name: str
    kind: TrancheKind
    amount: float = 0.0
    interest_rate: float = 0.0
    repayment: Repayment = "none"
    term_years: float = 30.0
    grace_years: int = 0
    initial_repayment_rate: float | None = None
    fixed_rate_years: int | None = None
    follow_up_rate: float | None = None
    drawdown_year: int = 0
    year_end_drawdown: bool = False
    interest_mode: InterestMode = "paid"
    churn_rate: float = 0.0
    replacement_rate: float = 1.0
    subsidy_grant: float = 0.0
    residual: bool = False

    def rate_in_year(self, service_year: int) -> float:
        """Interest rate in the n-th year of service (1-based)."""
        if self.fixed_rate_years is not None and service_year > self.fixed_rate_years:
            return self.follow_up_rate if self.follow_up_rate is not None else self.interest_rate
        return self.interest_rate


@dataclass
class Operations:
    """Running costs, inflation and liquidity rules.

    Costs are inflation-indexed. The index is 1 before
    `indexation_start_year` and (1 + inflation)^k in the k-th indexed year.
    `start_liquidity=None` sets the opening balance to `min_liquidity_months`
    of first-year gross rent, financed through the residual tranche.
    `initial_vacancy_rate`, if set, replaces `vacancy_rate` in the first
    `initial_vacancy_years` operating years.
    With `maintenance_reserve_rate` set, that share of the replacement value
    is paid each year into a separate maintenance reserve, from which the
    actual maintenance (`maintenance_rate`) is spent; the reserve is not part
    of liquidity. None charges `maintenance_rate` directly.
    """

    maintenance_rate: float = 0.015
    maintenance_reserve_rate: float | None = None
    admin_cost_per_year: float = 4_000.0
    insurance_per_year: float = 2_500.0
    vacancy_rate: float = 0.02
    initial_vacancy_rate: float | None = None
    initial_vacancy_years: int = 3
    community_cost_per_year: float = 0.0
    inflation: float = 0.02
    indexation_start_year: int = 1
    rent_mode: Literal["indexed", "fixed"] = "indexed"
    min_liquidity_months: float = 6.0
    start_liquidity: float | None = None


@dataclass
class MemberType:
    name: str = "Standard"
    count: int = 20
    equity_contribution: float = 7_200.0
    member_loan_amount: float = 0.0
    member_loan_rate: float = 0.0
    member_loan_interest_mode: InterestMode = "paid"


@dataclass
class Rules:
    """How freed money is used (A4) and how members are repaid (A5).

    `surplus_use` applies to the senior debt service freed after payoff and,
    with `redirect_surplus`, to liquidity above the reserve plus all
    outstanding direct and member loans, once no arrears are open.
    With `defer_repayments`, direct and member loan repayments that would push
    liquidity below the reserve are deferred and paid as soon as possible;
    arrears open longer than `max_arrears_years` make a scenario infeasible.
    """

    surplus_use: Literal["rent_reduction", "payout_15y", "next_project"] = "rent_reduction"
    exit_repayment: Literal["nominal", "real"] = "real"
    payout_interval_years: int = 15
    redirect_surplus: bool = False
    defer_repayments: bool = False
    max_arrears_years: int = 3


@dataclass
class Scenario:
    """Project, financing and rules."""

    property: Property = field(default_factory=Property)
    tranches: list[Tranche] = field(default_factory=list)
    operations: Operations = field(default_factory=Operations)
    member_types: list[MemberType] = field(default_factory=lambda: [MemberType()])
    rules: Rules = field(default_factory=Rules)
    horizon_years: int = 50

    @builtins.property
    def persons(self) -> int:
        return sum(m.count for m in self.member_types)

    def member_tranches(self) -> list[Tranche]:
        """Member equity and member loans as tranches, one per member type."""
        out = []
        for m in self.member_types:
            if m.equity_contribution:
                out.append(
                    Tranche(
                        name=f"equity_{m.name}",
                        kind="equity",
                        amount=m.count * m.equity_contribution,
                    )
                )
            if m.member_loan_amount:
                out.append(
                    Tranche(
                        name=f"member_loan_{m.name}",
                        kind="member_loan",
                        amount=m.count * m.member_loan_amount,
                        interest_rate=m.member_loan_rate,
                        interest_mode=m.member_loan_interest_mode,
                    )
                )
        return out
