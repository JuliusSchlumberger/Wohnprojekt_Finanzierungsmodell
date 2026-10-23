from string import Formatter

import pytest

pytest.importorskip("panel")

from app.i18n import LANGUAGES, Translator, texts  # noqa: E402
from app.widgets import Inputs  # noqa: E402


def _placeholders(text: str) -> set[str]:
    return {field for _, field, _, _ in Formatter().parse(text) if field}


@pytest.mark.parametrize("language", [lang for lang in LANGUAGES if lang != "de"])
def test_every_language_has_every_key_with_the_same_placeholders(language):
    reference, translated = texts("de"), texts(language)
    assert set(translated) == set(reference)
    for key, text in reference.items():
        assert _placeholders(translated[key]) == _placeholders(text), key


@pytest.mark.parametrize("language", list(LANGUAGES))
def test_methodology_page_exists_in_every_language(language):
    assert Translator(language).markdown("methodik").startswith("# ")


def test_number_formats_follow_the_language():
    de, en, nl = Translator("de"), Translator("en"), Translator("nl")
    assert de.eur(1234.5, 2) == "1.234,50 €"
    assert nl.eur(1234.5, 2) == "1.234,50 €"
    assert en.eur(1234.5, 2) == "€1,234.50"
    assert en.eur(-71) == "-€71"
    assert de.pct(0.267) == "26,7 %" and en.pct(0.267) == "26.7%"
    assert de.plotly_separators == ",." and en.plotly_separators == ".,"


def test_switching_language_relabels_inputs_but_keeps_values():
    inputs = Inputs()
    inputs.tenure = "leasehold"
    inputs.language = "en"
    assert inputs.param.land_price.label == "Land (€)"
    assert inputs.param.tenure.names == {"Purchase": "purchase", "Ground lease": "leasehold"}
    assert inputs.tenure == "leasehold"
    inputs.language = "nl"
    assert inputs.param.tenure.names["Erfpacht"] == "leasehold"


def test_pages_render_in_each_language_with_translated_results():
    from app.main import Dashboard

    dashboard = Dashboard()
    for language, label in [
        ("en", "Required rent"),
        ("nl", "Benodigde huur"),
        ("de", "Erforderliche Miete"),
    ]:
        dashboard.inputs.language = language
        dashboard.render()
        assert dashboard.page_names()[1] == Translator(language)("nav.mode1")
        assert dashboard.mode1.kpi_items()[0].label == label
        fig, _ = dashboard.mode1.chart_items()[0]
        assert fig.layout.separators == Translator(language).plotly_separators


def test_header_language_switch_relabels_navigation():
    from app.main import serve

    template = serve()
    (nav,) = template.header
    language = template.main[0].objects[-1]
    language.value = "en"
    assert list(nav.options)[1] == "Mode 1: Rent"
    language.value = "de"
    assert list(nav.options)[1] == "Modus 1: Miete"
