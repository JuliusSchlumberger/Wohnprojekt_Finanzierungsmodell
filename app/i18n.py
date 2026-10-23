"""UI language: texts by key and number formats for German, English and Dutch."""

from __future__ import annotations

import math
from functools import cache
from importlib import import_module
from importlib.resources import files

LANGUAGES = {"de": "Deutsch", "en": "English", "nl": "Nederlands"}
DEFAULT_LANGUAGE = "de"
REFERENCE_LANGUAGE = "de"


@cache
def texts(language: str) -> dict[str, str]:
    return import_module(f"app.locale.{language}").TEXTS


class Translator:
    """Texts and number formats of one language; missing keys fall back to German."""

    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        if language not in LANGUAGES:
            raise ValueError(f"unknown language {language!r}; choose from {list(LANGUAGES)}")
        self.language = language

    def __call__(self, key: str, **values) -> str:
        text = texts(self.language).get(key)
        if text is None:
            text = texts(REFERENCE_LANGUAGE)[key]
        return text.format(**values) if values else text

    def markdown(self, name: str) -> str:
        """A Markdown page shipped with the package, e.g. `methodik_de.md`."""
        return files("app.locale").joinpath(f"{name}_{self.language}.md").read_text("utf-8")

    @property
    def decimal_comma(self) -> bool:
        return self.language in ("de", "nl")

    def number(self, value: float, digits: int = 0) -> str:
        text = f"{value:,.{digits}f}"
        if self.decimal_comma:
            text = text.replace(",", " ").replace(".", ",").replace(" ", ".")
        return text

    def eur(self, value: float, digits: int = 0) -> str:
        if self.decimal_comma:
            return f"{self.number(value, digits)} €"
        sign = "-" if value < 0 else ""
        return f"{sign}€{self.number(abs(value), digits)}"

    def pct(self, fraction: float, digits: int = 1) -> str:
        number = self.number(100 * fraction, digits)
        return f"{number} %" if self.decimal_comma else f"{number}%"

    def ratio(self, value: float) -> str:
        return "∞" if math.isinf(value) else f"{self.number(value, 1)} : 1"

    @property
    def plotly_separators(self) -> str:
        """Decimal and thousands separator for Plotly number formats."""
        return ",." if self.decimal_comma else ".,"

    @property
    def currency_affixes(self) -> tuple[str, str]:
        """Prefix and suffix around euro amounts in chart ticks and hovers."""
        return ("", " €") if self.decimal_comma else ("€", "")

    def eur_hover(self, value: str, digits: int = 0) -> str:
        """Plotly hovertemplate for an euro amount, e.g. `eur_hover('y')`."""
        prefix, suffix = self.currency_affixes
        return f"{prefix}%{{{value}:,.{digits}f}}{suffix}"
