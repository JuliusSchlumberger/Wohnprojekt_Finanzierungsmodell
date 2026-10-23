import json
import sys
from pathlib import Path

import numpy as np
import pytest

from model import simulate
from model.types import MemberType, Operations, Property, Rules, Scenario, Tranche

REF = Path(__file__).resolve().parents[1] / "reference"
WORKBOOK = REF / "trias_reference_case.xlsx"
TOLERANCE = 0.01

pytestmark = [
    pytest.mark.reference,
    pytest.mark.skipif(not WORKBOOK.exists(), reason="run reference/fill_trias.ps1 first"),
]


def _case() -> dict:
    return json.loads((REF / "trias_case.json").read_text())


def scenario_from_case(c: dict) -> Scenario:
    """Translate the trias inputs; investment is entered as purchase price without extras."""
    area_total = c["private_area_m2"] + c["common_area_m2"]
    replacement_ratio = 0.6
    prop = Property(
        purchase_price=c["investment"],
        renovation_cost=0.0,
        ancillary_cost_rate=0.0,
        total_area_m2=area_total,
        replacement_value_ratio=replacement_ratio,
    )
    ops = Operations(
        maintenance_rate=c["maintenance_per_m2_year"] * area_total / prop.replacement_value,
        admin_cost_per_year=c["admin_cost_per_year"],
        insurance_per_year=c["insurance_per_year"],
        vacancy_rate=c["vacancy_rate"],
        inflation=c["inflation"],
        indexation_start_year=c["indexation_start_year"],
        start_liquidity=c["start_liquidity"],
    )
    persons = c["persons"]
    members = [
        MemberType(
            count=persons,
            equity_contribution=c["equity"] / persons,
        )
    ]
    dl, bank, sub = c["direct_loan"], c["bank_loan"], c["subsidy_loan"]
    tranches = [
        Tranche("direct_loans", "direct_loan", dl["amount"], dl["interest_rate"]),
        Tranche(
            "bank",
            "bank_loan",
            bank["amount"],
            bank["interest_rate"],
            "annuity",
            term_years=bank["term_years"],
        ),
        # The template's year-1 repayment formula for subsidy loans omits the
        # drawdown, so repayment starts in year 2 with the full-term annuity.
        Tranche(
            "subsidy",
            "subsidy_loan",
            sub["amount"],
            sub["interest_rate"],
            "annuity",
            term_years=sub["term_years"] + 1,
            grace_years=1,
        ),
    ]
    return Scenario(
        property=prop,
        tranches=tranches,
        operations=ops,
        member_types=members,
        rules=Rules(surplus_use="next_project"),
        horizon_years=c["horizon_years"],
    )


def _compare():
    sys.path.insert(0, str(REF))
    from read_trias import read_trias

    c = _case()
    years = slice(1, c["compare_years"])
    trias = read_trias(WORKBOOK).loc[years]
    rent_per_person = c["rent_per_m2_month"] * c["private_area_m2"] / c["persons"]
    res = simulate(scenario_from_case(c), rent_per_person)
    tb, tr = res.table.loc[years], {k: v.loc[years] for k, v in res.tranches.items()}
    ours = {
        "rent_gross": tb.gross_rent,
        "maintenance": -tb.maintenance,
        "vacancy": -(tb.gross_rent - tb.rent_income),
        "legal_admin": -(tb.admin + tb.insurance),
        "direct_loan_interest": -tr["direct_loans"].interest,
        "bank_interest": -tr["bank"].interest,
        "subsidy_interest": -tr["subsidy"].interest,
        "liquidity": tb.liquidity,
        "bank_repayment": -tr["bank"].repayment,
        "bank_balance": tr["bank"].balance,
        "subsidy_repayment": -tr["subsidy"].repayment,
        "subsidy_balance": tr["subsidy"].balance,
    }
    return trias, ours


@pytest.fixture(scope="module")
def compared():
    return _compare()


@pytest.mark.parametrize(
    "quantity",
    [
        "rent_gross",
        "maintenance",
        "vacancy",
        "legal_admin",
        "direct_loan_interest",
        "bank_interest",
        "subsidy_interest",
        "bank_repayment",
        "bank_balance",
        "subsidy_repayment",
        "subsidy_balance",
        "liquidity",
    ],
)
def test_matches_trias_within_one_percent(compared, quantity):
    trias, ours = compared
    expected = trias[quantity].to_numpy()
    scale = np.abs(expected).max()
    np.testing.assert_allclose(ours[quantity].to_numpy(), expected, rtol=0, atol=TOLERANCE * scale)
