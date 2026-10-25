import numpy as np
import pytest

pytest.importorskip("panel")

from app import charts  # noqa: E402
from app.main import Mode1, Mode2, Mode3, build_app  # noqa: E402
from app.widgets import Inputs  # noqa: E402
from model import required_rent  # noqa: E402
from model.member import MemberInputs  # noqa: E402
from model.presets import ProjectInputs, build_scenario  # noqa: E402


def test_default_inputs_match_project_defaults():
    mode1 = Mode1()
    expected = required_rent(build_scenario(ProjectInputs()))
    assert mode1.result.metrics["rent_per_person"] == pytest.approx(expected)


def test_rent_rises_when_bank_rate_slider_moves_up():
    mode1 = Mode1()
    before = mode1.result.metrics["rent_per_person"]
    mode1.inputs.bank_spread_pp = 5.5
    assert mode1.result.metrics["rent_per_person"] > before


def test_change_on_one_page_updates_the_other():
    inputs = Inputs()
    mode1, mode3 = Mode1(inputs=inputs), Mode3(inputs=inputs)
    rent, investment = mode1.result.metrics["rent_per_person"], mode3.investment
    inputs.param.update(direct_loans_5y=0.0, direct_loans_10y=0.0)
    assert mode1.result.metrics["rent_per_person"] > rent
    assert mode3.investment < investment


def test_subsidy_above_renovation_cost_shows_error():
    mode1 = Mode1()
    mode1.inputs.subsidy = 500_000
    assert mode1.result is None
    assert "Sanierung" in mode1.error


def test_sources_above_investment_show_error_instead_of_raising():
    mode1 = Mode1()
    mode1.inputs.equity_per_person = 200_000
    assert mode1.result is None
    assert "übersteigen" in mode1.error


def test_bank_loan_closes_gap_including_opening_liquidity():
    mode1 = Mode1()
    c = mode1.capital
    own = c["equity"] + c["member_loan"] + c["direct_loan"] + c["subsidy_loan"]
    opening = mode1.result.metrics["opening_liquidity"]
    assert c["bank_loan"] == pytest.approx(ProjectInputs().total_investment + opening - own)


def test_equity_like_share_below_minimum_shows_warning():
    mode1 = Mode1()
    assert mode1.bank_status()[1].alert_type == "success"
    mode1.inputs.param.update(
        member_loan_per_person=0.0, direct_loans_5y=50_000, direct_loans_10y=50_000
    )
    assert mode1.capital["equity_like_share"] < 0.2
    assert mode1.bank_status()[1].alert_type == "warning"


def test_mode3_default_is_limited_by_target_rent():
    mode3 = Mode3()
    assert mode3.investment == mode3.rent_limit < mode3.bank_limit
    assert required_rent(mode3.scenario) <= mode3.inputs.target_rent + 0.01


def test_mode3_bank_equity_rule_binds_when_minimum_share_is_high():
    mode3 = Mode3()
    mode3.inputs.min_equity_like_pct = 60.0
    assert mode3.investment == pytest.approx(ProjectInputs().equity_like / 0.6)
    assert mode3.investment < mode3.rent_limit


def test_mode3_rent_too_low_for_own_funds_shows_error():
    mode3 = Mode3()
    mode3.inputs.target_rent = 100.0
    assert mode3.scenario is None
    assert "Eigenmittel" in mode3.error


def test_app_renders_all_pages():
    build_app().get_root()


def test_rent_line_in_year_1_equals_nominal_rent_income():
    mode1 = Mode1()
    fig = charts.annual_costs(mode1.result, mode1.scenario)
    rent_line = next(t for t in fig.data if t.name == "Mieteinnahmen")
    assert rent_line.y[0] == pytest.approx(mode1.result.table["rent_income"].loc[1])


def test_cost_bars_add_up_to_net_cash_outflow():
    mode1 = Mode1()
    fig = charts.annual_costs(mode1.result, mode1.scenario)
    bars = sum(t.y for t in fig.data if t.type == "bar")
    tab = mode1.result.table.loc[1:]
    outflow = (
        tab.operating
        + tab.debt_service
        - tab.loan_inflow
        + tab.rent_rebate
        + tab.payout
        + tab.transfer_out
    ) / (tab.cost_index / tab.cost_index.loc[1])
    np.testing.assert_allclose(bars, outflow)


def test_late_repayments_show_up_in_kpis_and_charts():
    mode1 = Mode1()
    assert "Nicht pünktlich zurückgezahlt" in [k.label for k in mode1.kpi_items()]
    titles = [fig.layout.title.text for fig, _ in mode1.chart_items()]
    assert any("Nicht pünktlich" in title for title in titles)
    names = [t.name for t in charts.annual_costs(mode1.result, mode1.scenario).data]
    assert "Zinsen Direktkredite" in names
    assert "Zinsen Bank und Förderung" in names
    assert "Nachzahlung Rückstände inkl. Zinsen" in names


def test_on_time_repayment_bar_shows_full_amount_when_paid_on_time():
    mode1 = Mode1()
    mode1.inputs.param.update(direct_loans_5y=10_000.0, direct_loans_10y=0.0)
    fig = charts.annual_costs(mode1.result, mode1.scenario)
    bar = next(t for t in fig.data if t.name.startswith("Rückzahlung Direkt"))
    year5 = list(bar.x).index(mode1.result.table["year"].loc[5])
    deflator = mode1.result.table["cost_index"].loc[5] / mode1.result.table["cost_index"].loc[1]
    assert bar.y[year5] * deflator == pytest.approx(10_000.0)


def test_mode2_default_member_is_compared_against_market_rent():
    mode2 = Mode2()
    last = mode2.view_table.iloc[-1]
    assert last["advantage"] == pytest.approx(last["project"] - last["alternative"])
    assert "Vorsorgevorteil" in [k.label for k in mode2.kpi_items()]


def test_mode2_member_preset_sets_capital_and_changes_result():
    mode2 = Mode2()
    before = mode2.view_table["alternative"].iloc[0]
    mode2.inputs.member_type = "high"
    assert mode2.inputs.member_loan_personal == 40_000
    assert mode2.view_table["alternative"].iloc[0] > before


def test_mode2_exit_before_entry_shows_error():
    mode2 = Mode2()
    mode2.inputs.param.update(entry_year=30, exit_year=20)
    assert mode2.view_table is None
    assert "Auszug" in mode2.error


def test_every_chart_has_reading_help_and_a_value_table():
    for page in (Mode1(), Mode2(), Mode3()):
        for fig, help_text in page.chart_items():
            assert len(help_text.strip()) > 50
            table = charts.figure_table(fig)
            assert not table.empty


def test_start_page_boxes_have_equal_height_and_place_every_input_once():
    from app.layout import START_BOX_HEIGHT
    from app.widgets import ADVANCED_SECTIONS, SECTIONS

    inputs = Inputs()
    boxes = inputs.all_inputs().objects[0].objects
    assert len(boxes) == len(SECTIONS)
    assert {b.height for b in boxes} == {START_BOX_HEIGHT}
    sections = {**SECTIONS, **ADVANCED_SECTIONS}
    placed = [n for names in sections.values() for n in names]
    assert sorted(placed) == sorted(inputs.input_names())


def test_header_navigation_switches_between_all_pages():
    from app.main import PAGE_KEYS, serve

    template = serve()
    nav = template.header[0]
    assert len(nav.options) == len(PAGE_KEYS)
    assert list(nav.options)[1] == "Modus 1: Miete"
    assert list(nav.options.values()) == list(range(len(PAGE_KEYS)))


def test_equity_and_member_loans_scale_with_persons():
    inputs = Inputs()
    inputs.persons = 10
    project = inputs.to_project()
    assert project.equity == 10 * inputs.equity_per_person
    assert project.member_loans == 10 * inputs.member_loan_per_person


def test_header_navigation_switches_the_visible_page_and_back():
    from app.main import serve

    template = serve()
    nav, tabs = template.header[0], template.main[-1]
    for page in (2, 3, 0, 1):
        nav.value = page
        assert tabs.active == page
    tabs.active = 3
    assert nav.value == 3


def test_uncertainty_page_computes_on_demand_and_flags_stale_results():
    from app.main import UncertaintyPage

    page = UncertaintyPage()
    assert page.result is None
    page.n_samples = 50
    page.compute()
    assert not page.stale
    assert "Sichere Miete" in [k.label for k in page.kpi_items()]
    for fig, help_text, _fmt in page.chart_items():
        assert len(help_text.strip()) > 50
        assert not charts.figure_table(fig).empty
    page.inputs.inflation_pct = 3.0
    assert page.stale


def test_methodology_page_lists_every_input_with_its_default():
    from app.main import methodik_page, parameter_table

    inputs = Inputs()
    table = parameter_table(inputs)
    labels = [inputs.param[n].label for n in inputs.input_names()]
    assert all(label in table for label in labels)
    assert methodik_page(inputs).objects[0].object.startswith("# Methodik")


def test_rates_follow_inflation_at_fixed_spreads():
    inputs = Inputs()
    before = inputs.to_project()
    inputs.inflation_pct += 1.0
    after = inputs.to_project()
    for rate in ("bank_rate", "subsidy_rate", "member_loan_rate", "direct_loan_rate_10y"):
        assert getattr(after, rate) == pytest.approx(getattr(before, rate) + 0.01)
    assert inputs.to_member().alt_return == pytest.approx(MemberInputs().alt_return + 0.01)


def test_negative_real_rate_is_floored_at_zero_nominal():
    inputs = Inputs()
    inputs.param.update(inflation_pct=1.0, subsidy_spread_pp=-3.0)
    assert inputs.to_project().subsidy_rate == 0.0


def test_display_toggle_changes_charts_but_not_results():
    mode1 = Mode1()
    rent = mode1.result.metrics["rent_per_person"]
    real = charts.figure_table(mode1.chart_items()[1][0])
    mode1.inputs.display = "nominal"
    assert mode1.result.metrics["rent_per_person"] == rent
    nominal = charts.figure_table(mode1.chart_items()[1][0])
    assert nominal.iloc[0, 1] == pytest.approx(real.iloc[0, 1])
    assert nominal.iloc[-1, 1] > real.iloc[-1, 1]
    assert mode1.chart_items()[1][1].startswith("*")


def test_refinancing_member_loans_shows_inflow_bar_and_keeps_repayment_positive():
    mode1 = Mode1()
    mode1.inputs.member_loan_payoff = "bank"
    fig = mode1.chart_items()[0][0]
    bars = {trace.name: np.asarray(trace.y) for trace in fig.data if trace.type == "bar"}
    assert bars[charts.GERMAN("chart.costs.refinancing")].min() < 0
    assert bars[charts.GERMAN("chart.costs.senior_repayment")].min() >= -1e-6
