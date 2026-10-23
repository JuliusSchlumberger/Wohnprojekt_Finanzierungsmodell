"""Panel app: start page and modes 1-3 on shared inputs; run `panel serve app/main.py`."""

from __future__ import annotations

import math
from importlib.resources import files

import numpy as np
import panel as pn
import param
import plotly.graph_objects as go

from app import charts
from app.layout import ACCENT, START_BOX_WIDTH, Kpi, box, chart_block, kpi_grid
from app.widgets import ADVANCED_SECTIONS, INFO, SECTIONS, Inputs, eur, with_info
from model import Result, Scenario, max_investment, required_rent, simulate
from model.cashflow import capital_structure
from model.member import member_view
from model.presets import build_scenario
from model.solve import HEADROOM_TOLERANCE_EUR, is_affordable
from model.uncertainty import Ranges, rent_uncertainty

TITLE = "Wohnprojekt-Finanzierungsrechner"

INTRO = """
Mit diesem Rechner kann eine Wohnprojektgruppe durchspielen, wie sich ein gemeinsam
gekauftes oder im Erbbaurecht genutztes Haus finanzieren lässt. Hier stellt ihr alle
Annahmen ein; auf den Modus-Seiten lassen sich die wichtigsten davon direkt ändern.
Jede Änderung gilt sofort auf allen Seiten. Das **?** neben einem Feld oder einer
Kennzahl erklärt, was dahintersteckt.
"""

MODES = [
    ("Modus 1: Miete", "Welche Miete pro Person braucht unser Haus mindestens?"),
    ("Modus 2: Vorsorge", "Lohnt sich das Projekt für ein Mitglied gegenüber Marktmiete?"),
    ("Modus 3: Zielmiete", "Wie viel Haus kann sich unsere Gruppe bei einer Zielmiete leisten?"),
]

DISCLAIMER = (
    "**Haftungshinweis:** Dieser Rechner ist ein Planungswerkzeug und keine Finanz-, Steuer- "
    "oder Rechtsberatung. Alle Ergebnisse hängen von den Annahmen ab."
)

ASSUMPTIONS = [
    (
        "Eigentumsmodell",
        "Ein gemeinsamer Rechtsträger (eG, GmbH, GmbH & Co. KG) kauft das Haus oder nutzt es "
        "im Erbbaurecht. Mitglieder zahlen ein Nutzungsentgelt („Miete“). Kein Einzeleigentum.",
    ),
    (
        "Mieteinheit",
        "Miete pro Person und Monat, für alle gleich. Gemeinschaftsflächen sind darin enthalten.",
    ),
    ("Kapitalbeiträge", "Einzelpersonen bringen unterschiedlich viel ein (Mitgliedertypen)."),
    (
        "Frei werdendes Geld",
        "Nach Tilgung von Bank- und Förderdarlehen und sobald alle Direkt- und "
        "Mitgliederdarlehen gedeckt sind: Mietsenkung, Mietrückzahlung alle 15 Jahre oder "
        "Solidartransfer an ein nächstes Projekt.",
    ),
    (
        "Einlagen",
        "Bei Austritt inflationsindexiert zurückgezahlt; neue Mitglieder kaufen sich zum "
        "selben Wert ein. Der Bestand im Projekt bleibt konstant.",
    ),
    (
        "Zeithorizont und Inflation",
        "50 Jahre. Miete, Betriebskosten und Erbbauzins steigen mit der Inflation; Zins und "
        "Tilgung sind nominal fest.",
    ),
    (
        "Mindestliquidität",
        "Das Konto fällt nie unter die Mindestreserve (Standard 6 Monatsmieten).",
    ),
    ("Steuern", "Nicht modelliert."),
    (
        "Direkt- und Mitgliederdarlehen",
        "Nachrangig und endfällig. Direktkredite laufen 5 oder 10 Jahre, Zinsen jährlich "
        "ausgezahlt; Mitgliederdarlehen 15 Jahre, Zinsen thesauriert. Was am Fälligkeitstag "
        "nicht ohne Unterschreiten der Mindestreserve zurückgezahlt werden kann, wird so "
        "schnell wie möglich nachgezahlt, innerhalb einer Frist (Standard 3 Jahre), und verzinst "
        "sich bis dahin.",
    ),
]

METHOD1_TEXT = """
Das Modell rechnet 50 Jahre in Jahresschritten. Jedes Jahr gilt:
**Konto neu = Konto alt + Mieteinnahmen − Betriebskosten − Zinsen − Tilgung**
(abzüglich Rückzahlung fälliger Direkt- und Mitgliederdarlehen, Mietsenkung aus dem
Überschuss, Mietrückzahlung oder Solidartransfer).

- **Mieteinnahmen**: Miete × Personen × 12, abzüglich Mietausfall (in den ersten
  3 Jahren höher).
- **Betriebskosten**: Zuführung zur Instandhaltungsrücklage (Anteil des
  Wiederherstellungswerts), Verwaltung und Versicherung.
- **Zins und Tilgung**: je Darlehen nach seinen Konditionen, nominal fest.
- **Mindestreserve**: das Konto darf nie unter die Mindestreserve fallen (Standard
  6 Monatsmieten, unter „Erweitert“).
- **Rückstände**: würde eine fällige Rückzahlung das Konto unter die Reserve drücken,
  wird nur der mögliche Teil gezahlt; der Rest wird so schnell wie möglich nachgezahlt
  und muss innerhalb einer Frist beglichen sein (Standard 3 Jahre, unter „Erweitert“). Bis dahin
  fallen Zinsen an.
- **Überschuss (A4)**: erst wenn kein Rückstand offen ist und das Konto über der Reserve
  alle noch offenen Direkt- und Mitgliederdarlehen decken könnte, fließt der Rest in
  Mietsenkung, Mietrückzahlung oder Solidartransfer.

Die **erforderliche Miete** ist die niedrigste Anfangsmiete, bei der diese Bedingungen in
allen 50 Jahren erfüllt sind, auf 1 Cent genau. Das **engste Jahr** ist das Jahr, in dem
das Konto der Reserve am nächsten kommt; es bestimmt die Miete.
"""

METHOD2_TEXT = """
Grundlage ist die erforderliche Miete aus Modus 1 mit allen Annahmen der Startseite.
Verglichen werden zwei Wege für ein Mitglied, beide inflationsbereinigt:

- **Im Projekt**: Das Mitglied zahlt Einlage und ggf. Mitgliederdarlehen ein und zahlt die
  Projektmiete. Alles, was es gegenüber der Marktmiete spart, sowie Mietrückzahlungen und
  zurückgezahlte Einlage und Darlehen legt es zur Alternativrendite an. Einlage (real) und
  Darlehen (mit Zinseszins) zählen zum Vermögen, solange sie im Projekt stecken.
- **Marktmiete + Geld angelegt**: Einlage und Darlehensbetrag werden stattdessen zur
  Alternativrendite angelegt, und das Mitglied zahlt Marktmiete.
- **Einlage und Darlehen verloren** (gestrichelt): wie „Im Projekt“, aber Einlage und
  Darlehen fallen aus, z. B. bei Insolvenz. Nachrangiges Kapital trägt dieses Risiko.

Mietsenkungen aus dem Überschuss (A4) senken die Projektmiete und erhöhen damit die
Ersparnis. Das einzelne Mitglied wirkt nicht auf die Projektfinanzierung zurück.
"""

METHOD3_TEXT = """
Eure Eigenmittel (Einlagen, Mitgliederdarlehen, Direktkredite, Förderdarlehen) sind fest;
das Bankdarlehen wächst mit dem Haus. Grundstück, Haus und Sanierung werden dabei im
Verhältnis eurer Kostenschätzung hoch- oder heruntergerechnet. Zwei Grenzen bestimmen,
wie teuer das Haus sein darf:

- **Zielmiete**: Je teurer das Haus, desto größer das Bankdarlehen und desto höher die
  erforderliche Miete (Modus 1). Gesucht wird die größte Investition, bei der die
  erforderliche Miete die Zielmiete nicht übersteigt, auf 1.000 € genau.
- **Eigenkapitalanforderung der Bank**: Einlagen, Mitgliederdarlehen und Direktkredite
  müssen mindestens den Mindestanteil der Investition decken, also
  Investition ≤ (Einlagen + Mitgliederdarlehen + Direktkredite) / Mindestanteil.

Die zulässige Investition ist die kleinere der beiden Grenzen.
"""

CHART_HELP = {
    "annual_costs": """
Jeder Balken zeigt, wofür das Projekt in einem Jahr Geld ausgibt; die schwarze Linie sind
die Mieteinnahmen nach Mietausfall.

- **Balken über der Linie**: das Projekt zahlt in diesem Jahr aus seinem Konto drauf.
- **Balken unter der Linie**: das Konto wächst.
- Alle Werte sind **inflationsbereinigt** (Kaufkraft von Jahr 1). Eine waagerechte Linie
  heißt also: die Miete steigt genau mit der Inflation. Zins und Tilgung der Bank sind
  nominal fest und werden deshalb real von Jahr zu Jahr kleiner.
- Die hohen Balken in einzelnen Jahren sind **Fälligkeiten** von Direkt- und
  Mitgliederdarlehen. Was dort nicht sofort geht, erscheint in den Folgejahren als
  Nachzahlung.
- Ab dem Jahr, in dem der **Überschuss** fließt, füllt Mietsenkung, Mietrückzahlung oder
  Solidartransfer die Lücke bis zur Linie.

Mit der Maus über einem Jahr seht ihr alle Beträge.
""",
    "debt_balances": """
Wie viel das Projekt am Ende jedes Jahres noch schuldet, je Darlehen und als Summe
(gestrichelt), inflationsbereinigt.

- **Bank und Förderung** sinken stetig durch die Tilgung.
- **Direktkredite** bleiben bis zu ihrer Fälligkeit (5 bzw. 10 Jahre) stehen und fallen dann
  auf null. **Mitgliederdarlehen** wachsen bis zur Fälligkeit nach 15 Jahren durch den
  Zinseszins.
- **Rückstände** zeigen, was nach der Fälligkeit noch nachgezahlt werden muss.
""",
    "liquidity": """
Kontostand am Jahresende im Vergleich zur Mindestreserve (gestrichelt, Standard 6 Monatsmieten),
inflationsbereinigt.

- Die Miete ist so gewählt, dass das Konto die Reserve **nie unterschreitet**. Wo die
  Linien sich berühren, liegt das engste Jahr.
- Vor Fälligkeiten von Darlehen spart das Konto an, danach fällt es.
- Sobald kein Rückstand offen ist und alle Direkt- und Mitgliederdarlehen gedeckt wären,
  wird der **Überschuss** abgeschöpft; deshalb wächst das Konto dann nicht weiter.
- Gepunktet: die **Instandhaltungsrücklage**, ein eigener Topf, der nicht zur Liquidität
  zählt.
""",
    "arrears": """
- **Balken**: wie viel von fälligen Direkt- und Mitgliederdarlehen am Fälligkeitstag nicht
  gezahlt werden konnte, ohne die Mindestreserve zu unterschreiten.
- **Linie**: wie viel davon am Jahresende noch offen ist. Sie muss innerhalb der Frist
  wieder auf null sein; bis dahin zahlt das Projekt Zinsen auf den Rückstand.

Für Darlehensgeber*innen heißt ein Balken: Sie bekommen ihr Geld später als vereinbart.
""",
    "investment_curve": """
Wie viel Haus (Gesamtinvestition) bei einer bestimmten Zielmiete pro Person finanzierbar
ist, in heutigen Preisen.

- Die **Linie** steigt, weil eine höhere Miete ein größeres Bankdarlehen trägt.
- **Gestrichelt**: die Obergrenze durch die Eigenkapitalanforderung der Bank; sie hängt
  nicht von der Miete ab.
- Zulässig ist jeweils die **niedrigere** der beiden Linien. Der Punkt markiert eure
  Zielmiete.
""",
    "liquidity_mode3": """
Kontostand des Hauses, das bei eurer Zielmiete gerade noch finanzierbar ist, im Vergleich
zur Mindestreserve (gestrichelt), inflationsbereinigt. Berührt die Linie die Reserve, ist
das Haus an der Grenze dessen, was die Zielmiete trägt.
""",
    "member_wealth": """
Vermögen des Mitglieds über die Zeit, inflationsbereinigt.

- **Im Projekt** über **Marktmiete + Geld angelegt**: das Projekt lohnt sich finanziell.
  Der Abstand ist der Vorsorgevorteil.
- Am Anfang liegt der Vergleich oft vorn, weil Geld am Markt mehr Rendite bringt als
  Einlage und Darlehen. Die Mietersparnis holt das über die Jahre auf.
- **Gestrichelt**: falls Einlage und Darlehen verloren gingen, z. B. bei einer Insolvenz.
  Liegt auch diese Linie über dem Vergleich, lohnt sich das Projekt selbst dann.
""",
}

MODE1_LEVERS = [
    "land_price",
    "tenure",
    "building_price",
    "renovation_cost",
    "equity_per_person",
    "member_loan_per_person",
    "direct_loans_5y",
    "direct_loans_10y",
    "subsidy",
    "bank_rate_pct",
    "inflation_pct",
]
MODE2_LEVERS = [
    "member_type",
    "member_equity",
    "member_loan_personal",
    "member_loan_rate_pct",
    "entry_year",
    "exit_year",
    "market_rent",
    "alt_return_pct",
    "inflation_pct",
    "surplus_use",
]
MODE3_LEVERS = [
    "target_rent",
    "equity_per_person",
    "member_loan_per_person",
    "direct_loans_5y",
    "direct_loans_10y",
    "subsidy",
    "bank_rate_pct",
    "inflation_pct",
    "min_equity_like_pct",
]
CURVE_RENTS_EUR_PERSON = np.arange(200.0, 1_200.01, 50.0)
MIN_INVESTMENT_EUR = 50_000.0
LEVER_WIDTH = 360


def assumptions_table() -> str:
    rows = "\n".join(f"| A{i} | {k} | {v} |" for i, (k, v) in enumerate(ASSUMPTIONS, start=1))
    return "| Nr. | Annahme | Festlegung |\n|---|---|---|\n" + rows


def _bank_line(capital: dict[str, float]) -> pn.viewable.Viewable:
    return with_info(
        pn.pane.Markdown(f"**Bankdarlehen (automatisch): {eur(capital['bank_loan'])}**"),
        INFO["bank_loan"],
    )


def _pct(fraction: float) -> str:
    return f"{100 * fraction:.1f} %".replace(".", ",")


def _ratio(value: float) -> str:
    return "∞" if math.isinf(value) else f"{value:.1f} : 1".replace(".", ",")


def _on_demand(title: str, text: str) -> pn.viewable.Viewable:
    return pn.Accordion(
        (title, pn.pane.Markdown(text, sizing_mode="stretch_width")),
        active=[],
        sizing_mode="stretch_width",
        margin=(0, 0, 12, 0),
    )


class _Page(param.Parameterized):
    """A mode page: recomputes from the shared inputs whenever any of them changes."""

    inputs = param.ClassSelector(class_=Inputs)
    scenario = param.ClassSelector(class_=Scenario, allow_None=True)
    result = param.ClassSelector(class_=Result, allow_None=True)
    capital = param.Dict(default={})
    error = param.String(default="")

    levers: list[str] = []
    method: str = ""

    def __init__(self, **params):
        super().__init__(inputs=params.pop("inputs", None) or Inputs(), **params)
        self.inputs.param.watch(self._update, self.inputs.input_names())
        self._update()

    def _update(self, *_events) -> None:
        raise NotImplementedError

    def kpi_items(self) -> list[Kpi]:
        raise NotImplementedError

    def alerts(self) -> list[pn.viewable.Viewable]:
        return []

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        raise NotImplementedError

    def bank_status(self) -> pn.viewable.Viewable:
        return pn.Spacer(height=0)

    def _input_error(self) -> str:
        inp = self.inputs
        if inp.subsidy > inp.renovation_cost:
            return (
                f"Förderdarlehen ({eur(inp.subsidy)}) sind nur für Sanierung nutzbar und "
                f"übersteigen die Sanierungskosten ({eur(inp.renovation_cost)})."
            )
        if inp.land_price + inp.building_price <= 0:
            return "Grundstück und Haus dürfen nicht beide 0 € kosten."
        return ""

    def _fail(self, message: str) -> None:
        self.param.update(scenario=None, result=None, capital={}, error=message)

    @param.depends("result", "error")
    def kpis(self) -> pn.viewable.Viewable:
        if self.error:
            return pn.pane.Alert(f"Keine Lösung: {self.error}", alert_type="danger")
        return pn.Column(kpi_grid(self.kpi_items()), *self.alerts(), sizing_mode="stretch_width")

    @param.depends("result")
    def figures(self) -> pn.viewable.Viewable:
        if self.result is None:
            return pn.Spacer(height=0)
        blocks = [chart_block(fig, help_text) for fig, help_text in self.chart_items()]
        return pn.Column(*blocks, sizing_mode="stretch_width")

    def view(self) -> pn.viewable.Viewable:
        levers = box(
            "Stellschrauben",
            *self.inputs.widgets(self.levers),
            self.bank_status,
            pn.pane.Markdown(
                "*Alle weiteren Annahmen auf der Startseite.*", styles={"font-size": "13px"}
            ),
            width=LEVER_WIDTH,
        )
        return pn.Row(
            levers,
            pn.Column(
                self.kpis,
                _on_demand("So wird gerechnet", self.method),
                self.figures,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )


class Mode1(_Page):
    """Required rent per person for the shared inputs."""

    levers = MODE1_LEVERS
    method = METHOD1_TEXT

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        p = self.inputs.to_project()
        if p.own_funds > p.total_investment:
            self._fail(
                f"Eigenmittel und Förderdarlehen ({eur(p.own_funds)}) übersteigen die "
                f"Gesamtinvestition ({eur(p.total_investment)}). Bitte Beträge reduzieren."
            )
            return
        try:
            scenario = build_scenario(p)
            rent = required_rent(scenario)
        except ValueError as exc:
            self._fail(str(exc))
            return
        self.param.update(
            scenario=scenario,
            result=simulate(scenario, rent),
            capital=capital_structure(scenario, rent),
            error="",
        )

    @param.depends("capital")
    def bank_status(self) -> pn.viewable.Viewable:
        if not self.capital:
            return pn.Spacer(height=0)
        c = self.capital
        min_share = self.inputs.min_equity_like_pct / 100
        share = c["equity_like_share"]
        ratio = c["bank_loan"] / c["equity_like"] if c["equity_like"] else math.inf
        text = (
            f"Eigenkapital + Nachrang: {eur(c['equity_like'])} = {_pct(share)} der "
            f"Gesamtinvestition (Mindestanteil {_pct(min_share)}). "
            f"Bankdarlehen : Eigenkapital + Nachrang = {_ratio(ratio)}."
        )
        if share >= min_share:
            check = pn.pane.Alert(text, alert_type="success")
        else:
            gap = (min_share - share) * self.scenario.property.total_investment
            check = pn.pane.Alert(
                f"{text} Es fehlen {eur(gap)} Einlagen, Mitgliederdarlehen oder "
                "Direktkredite; so finanziert eine Bank vermutlich nicht.",
                alert_type="warning",
            )
        return pn.Column(_bank_line(c), check, sizing_mode="stretch_width")

    def kpi_items(self) -> list[Kpi]:
        m, tab = self.result.metrics, self.result.table
        start = self.scenario.property.start_year
        payoff = m["senior_payoff_year"]
        headroom = tab["headroom"].loc[1:]
        tightest = int(headroom.index[headroom <= headroom.min() + HEADROOM_TOLERANCE_EUR][0])
        years = self.inputs.max_arrears_years
        items = [
            Kpi(
                "Erforderliche Miete",
                eur(m["rent_per_person"], 2),
                "Niedrigste Miete pro Person und Monat, bei der das Konto in allen 50 Jahren "
                f"über der Mindestreserve bleibt und jeder Rückstand nach höchstens {years} Jahren "
                "beglichen ist. Danach steigt sie mit der Inflation.",
                note="pro Person und Monat",
            ),
            Kpi(
                "Mieteinnahmen Jahr 1",
                eur(m["rent_per_year"]),
                "Miete aller Personen im ersten Jahr, vor Mietausfall.",
                note="pro Jahr, alle Personen",
            ),
            Kpi(
                "Gesamtinvestition",
                eur(self.scenario.property.total_investment),
                "Grundstück (bei Kauf), Haus, Sanierung und Kaufnebenkosten.",
            ),
            Kpi(
                "Engstes Jahr",
                str(start + tightest),
                "Jahr, in dem das Konto der Mindestreserve am nächsten kommt. Dieses Jahr "
                "bestimmt die erforderliche Miete.",
                note=f"Jahr {tightest}",
            ),
            Kpi(
                "Bank und Förderung getilgt",
                "–" if math.isnan(payoff) else str(int(start + payoff)),
                "Ab dem Folgejahr wird der bisherige Kapitaldienst frei und nach der "
                "gewählten Überschussverwendung genutzt.",
            ),
        ]
        first_surplus = tab["year"][tab["surplus"] > 0.5]
        if not first_surplus.empty:
            items.append(
                Kpi(
                    "Überschuss fließt ab",
                    str(int(first_surplus.iloc[0])),
                    "Ab diesem Jahr ist kein Rückstand offen und das Konto deckt Reserve plus "
                    "alle offenen Direkt- und Mitgliederdarlehen. Der Rest geht in Mietsenkung, "
                    "Mietrückzahlung oder Solidartransfer.",
                )
            )
        late = tab["arrears_new"][tab["arrears_new"] > 0.5]
        if not late.empty:
            items.append(
                Kpi(
                    "Nicht pünktlich zurückgezahlt",
                    eur(late.sum()),
                    "Teil fälliger Direkt- und Mitgliederdarlehen, der am Fälligkeitstag nicht "
                    f"gezahlt werden konnte (nominal). Er wird innerhalb von {years} Jahren "
                    "nachgezahlt; Details in der Grafik unten.",
                    note=", ".join(str(int(tab["year"][t])) for t in late.index),
                    tone="warning",
                )
            )
        return items

    def alerts(self) -> list[pn.viewable.Viewable]:
        sub = charts.subordinated_debt_real(self.result, self.scenario)
        if not sub.any() or sub.iloc[-1] <= sub.iloc[0]:
            return []
        return [
            pn.pane.Alert(
                f"Direkt- und Mitgliederdarlehen sind nach {len(sub) - 1} Jahren real höher als "
                "am Anfang, weil Zinsen auf Mitgliederdarlehen schneller auflaufen, als "
                "zurückgezahlt wird. Diese Schuld geht nicht in die erforderliche Miete ein.",
                alert_type="warning",
            )
        ]

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        items = [
            (charts.annual_costs(self.result, self.scenario), CHART_HELP["annual_costs"]),
            (charts.liquidity(self.result), CHART_HELP["liquidity"]),
            (charts.debt_balances(self.result, self.scenario), CHART_HELP["debt_balances"]),
        ]
        if self.result.table["arrears_new"].any():
            items.append((charts.arrears(self.result), CHART_HELP["arrears"]))
        return items


class Mode2(_Page):
    """One member's wealth in the project versus market rent and investing elsewhere."""

    view_table = param.DataFrame(default=None, allow_None=True)

    levers = MODE2_LEVERS
    method = METHOD2_TEXT

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        if self.inputs.entry_year >= self.inputs.exit_year:
            self._fail("Der Auszug muss nach dem Einzug liegen.")
            return
        try:
            scenario = build_scenario(self.inputs.to_project())
            result = simulate(scenario, required_rent(scenario))
        except ValueError as exc:
            self._fail(str(exc))
            return
        self.param.update(
            scenario=scenario,
            result=result,
            view_table=member_view(scenario, result, self.inputs.to_member()),
            error="",
        )

    def _fail(self, message: str) -> None:
        super()._fail(message)
        self.view_table = None

    def kpi_items(self) -> list[Kpi]:
        v = self.view_table
        first, last = v.iloc[1], v.iloc[-1]
        end = int(last["year"])
        advantage = last["advantage"]
        return [
            Kpi(
                "Projektmiete",
                eur(self.result.metrics["rent_per_person"], 2),
                "Erforderliche Miete aus Modus 1, pro Person und Monat im ersten Jahr.",
                note="aus Modus 1",
            ),
            Kpi(
                "Ersparnis gegenüber Marktmiete",
                eur(first["rent_saving_month"]),
                "Marktmiete minus Projektmiete im ersten Jahr nach dem Einzug. Später wächst "
                "die Ersparnis, sobald der Überschuss die Miete senkt.",
                note="pro Monat, erstes Jahr",
            ),
            Kpi(
                "Vorsorgevorteil",
                eur(advantage),
                "Vermögen im Projekt minus Vermögen mit Marktmiete und angelegtem Geld, am "
                "Ende, inflationsbereinigt.",
                note=f"bis {end}",
                tone="good" if advantage >= 0 else "warning",
            ),
            Kpi(
                "Vermögen im Projekt",
                eur(last["project"]),
                "Angelegte Ersparnisse und Rückzahlungen plus Einlage und Darlehen, solange "
                "sie im Projekt stecken; inflationsbereinigt.",
                note=f"{end}",
            ),
            Kpi(
                "Vermögen mit Marktmiete",
                eur(last["alternative"]),
                "Einlage und Darlehensbetrag zur Alternativrendite angelegt, Marktmiete "
                "gezahlt; inflationsbereinigt.",
                note=f"{end}",
            ),
            Kpi(
                "Bei Ausfall von Einlage und Darlehen",
                eur(last["default"] - last["alternative"]),
                "Vorsorgevorteil, falls Einlage und Darlehen komplett verloren gingen, z. B. "
                "bei einer Insolvenz des Projekts.",
                note="Vorteil gegenüber Marktmiete",
            ),
        ]

    @param.depends("view_table", "error")
    def kpis(self) -> pn.viewable.Viewable:
        return super().kpis()

    @param.depends("view_table")
    def figures(self) -> pn.viewable.Viewable:
        return super().figures()

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        if self.view_table is None:
            return []
        return [(charts.member_wealth(self.view_table), CHART_HELP["member_wealth"])]


class Mode3(_Page):
    """Admissible investment for a target rent, limited by rent and by the bank's equity rule."""

    rent_limit = param.Number(default=math.nan)
    bank_limit = param.Number(default=math.inf)
    investment = param.Number(default=math.nan)
    curve = param.Array(default=None, allow_None=True)

    levers = MODE3_LEVERS
    method = METHOD3_TEXT

    def _update(self, *_events) -> None:
        if message := self._input_error():
            self._fail(message)
            return
        p = self.inputs.to_project()
        lower = max(p.own_funds, MIN_INVESTMENT_EUR)

        def scenario_for(total: float) -> Scenario:
            return build_scenario(p.scaled_to(total))

        def rent_limit_at(rent: float) -> float:
            try:
                return max_investment(scenario_for, rent, lower)
            except ValueError:
                return math.nan

        target = self.inputs.target_rent
        if not is_affordable(scenario_for(lower), target):
            self._fail(
                f"Schon ein Haus in Höhe eurer Eigenmittel ({eur(lower)}) braucht mehr als "
                f"{eur(target)} Miete pro Person. Zielmiete erhöhen oder Eigenmittel ändern."
            )
            return
        rent_limit = rent_limit_at(target)
        if math.isnan(rent_limit):
            self._fail("Keine obere Grenze für die Investition gefunden; Eingaben prüfen.")
            return
        min_share = self.inputs.min_equity_like_pct / 100
        bank_limit = p.equity_like / min_share if min_share > 0 else math.inf
        investment = min(rent_limit, bank_limit)
        if investment < lower:
            self._fail(
                "Die Eigenkapitalanforderung der Bank lässt kein Haus zu, das eure Eigenmittel "
                "aufnimmt: Einlagen, Mitgliederdarlehen und Direktkredite sind im Verhältnis zu "
                "den Förderdarlehen zu klein."
            )
            return
        scenario = scenario_for(investment)
        self.param.update(
            rent_limit=rent_limit,
            bank_limit=bank_limit,
            investment=investment,
            scenario=scenario,
            result=simulate(scenario, target),
            capital=capital_structure(scenario, target),
            curve=np.array([rent_limit_at(r) for r in CURVE_RENTS_EUR_PERSON]),
            error="",
        )

    def _fail(self, message: str) -> None:
        super()._fail(message)
        self.param.update(investment=math.nan, curve=None)

    @param.depends("capital")
    def bank_status(self) -> pn.viewable.Viewable:
        return _bank_line(self.capital) if self.capital else pn.Spacer(height=0)

    def kpi_items(self) -> list[Kpi]:
        estimate = self.inputs.to_project().total_investment
        rent_binds = self.rent_limit <= self.bank_limit
        share = self.investment / estimate
        return [
            Kpi(
                "Zulässige Investition",
                eur(self.investment),
                "Die kleinere der beiden Grenzen: was die Zielmiete trägt und was die "
                "Eigenkapitalanforderung der Bank zulässt.",
                note="begrenzt durch " + ("Zielmiete" if rent_binds else "Eigenkapital"),
                tone="good" if share >= 1 else "warning",
            ),
            Kpi(
                "Anteil eurer Kostenschätzung",
                _pct(share),
                "Zulässige Investition geteilt durch eure Kostenschätzung (Grundstück, Haus, "
                "Sanierung und Nebenkosten von der Startseite). Ab 100 % ist das Haus "
                "finanzierbar.",
                note=f"Schätzung {eur(estimate)}",
            ),
            Kpi(
                "Grenze durch Zielmiete",
                eur(self.rent_limit),
                "Größte Investition, bei der die erforderliche Miete die Zielmiete nicht "
                "übersteigt.",
            ),
            Kpi(
                "Grenze durch Eigenkapital",
                "keine" if math.isinf(self.bank_limit) else eur(self.bank_limit),
                "(Einlagen + Mitgliederdarlehen + Direktkredite) / Mindestanteil, den die "
                "Bank verlangt.",
            ),
        ]

    @param.depends("investment", "error")
    def kpis(self) -> pn.viewable.Viewable:
        return super().kpis()

    def chart_items(self) -> list[tuple[go.Figure, str]]:
        curve = charts.investment_curve(
            CURVE_RENTS_EUR_PERSON,
            self.curve,
            self.bank_limit,
            self.inputs.target_rent,
            self.investment,
        )
        return [
            (curve, CHART_HELP["investment_curve"]),
            (charts.liquidity(self.result), CHART_HELP["liquidity_mode3"]),
        ]


UNCERTAINTY_TEXT = """
Viele Annahmen kennt ihr heute nicht genau. Hier gebt ihr für die fünf wichtigsten eine
Spanne an. Der Rechner zieht daraus viele Varianten (Latin-Hypercube-Stichprobe) und sucht
für jede die erforderliche Miete wie in Modus 1, auf 50 Cent genau.

- Innerhalb jeder Spanne ist der Wert von der Startseite am **wahrscheinlichsten**;
  Werte zu den Rändern hin werden seltener (Dreiecksverteilung).
- Die **sichere Miete** ist die Miete, die in 90 % der Varianten reicht.
- Alle übrigen Annahmen kommen unverändert von der Startseite.
- Gleiche Eingaben liefern immer dasselbe Ergebnis (fester Zufallsstartwert).
"""

UNCERTAINTY_HELP = {
    "rent_distribution": """
Jeder Balken zählt, wie viele Varianten eine erforderliche Miete in diesem Bereich haben.

- **Gepunktet**: die Miete aus Modus 1, mit den Werten der Startseite.
- **Durchgezogen**: der Median; die Hälfte der Varianten braucht weniger, die Hälfte mehr.
- **Gestrichelt**: die sichere Miete. Nur 10 % der Varianten brauchen mehr.

Je breiter die Verteilung, desto mehr hängt die Miete von Annahmen ab, die ihr heute nicht
kennt. Ein Abstand zwischen Modus-1-Miete und sicherer Miete ist ein Puffer, den ihr
einplanen könnt.
""",
    "headroom_band": """
Wie viel Geld über der Mindestreserve auf dem Konto liegt, wenn ihr die sichere Miete
ansetzt, inflationsbereinigt.

- **Linie**: Median über alle Varianten.
- **Band**: 80 % der Varianten liegen darin (zwischen dem 10. und 90. Perzentil).
- Der Puffer ist in jedem Jahr höchstens so hoch, bis der Überschuss abgeschöpft wird;
  danach liegt er nahe null.

Liegt das untere Bandende unter null, unterschreiten in diesem Jahr einige Varianten die
Reserve. Das sind die 10 %, für die die sichere Miete nicht reicht.
""",
    "sensitivity": """
Wie stark jede unsichere Annahme mit der erforderlichen Miete zusammenhängt
(Rangkorrelation, −1 bis +1).

- **Positiv** (blau): ist die Annahme höher, steigt die Miete, z. B. höhere Sanierungskosten.
- **Negativ** (rot): ist die Annahme höher, sinkt die Miete. Bei der Inflation liegt das
  daran, dass die Miete mit der Inflation wächst, Zins und Tilgung aber nicht.
- Je länger der Balken, desto mehr lohnt es sich, diese Annahme genauer zu klären.
""",
}

RANGE_INFO = {
    "inflation_range": "Spanne der jährlichen Inflation. Wahrscheinlichster Wert: Startseite.",
    "bank_change_range": (
        "Änderung des Bankzinses nach Ende der Zinsbindung (10 Jahre), in Prozentpunkten. "
        "Wahrscheinlichster Wert: die Wahl auf der Startseite (sinkt −1, bleibt 0, steigt +1)."
    ),
    "vacancy_range": (
        "Spanne des Mietausfalls ab dem 4. Jahr. Wahrscheinlichster Wert: Startseite."
    ),
    "renovation_range": (
        "Sanierungskosten in % eurer Schätzung. 130 % heißt: die Sanierung wird 30 % teurer. "
        "Wahrscheinlichster Wert: 100 %."
    ),
    "running_range": (
        "Verwaltung und Versicherung in % eurer Schätzung. Wahrscheinlichster Wert: 100 %."
    ),
    "n_samples": (
        "Mehr Varianten machen das Ergebnis stabiler, dauern aber länger (etwa 1 Sekunde "
        "pro 100 Varianten)."
    ),
}


class UncertaintyPage(param.Parameterized):
    """Spread of the required rent for ranges of the most uncertain inputs."""

    inputs = param.ClassSelector(class_=Inputs)
    inflation_range = param.Range((1.0, 4.0), bounds=(0.0, 8.0), label="Inflation (%)")
    bank_change_range = param.Range(
        (-1.0, 3.0), bounds=(-3.0, 5.0), label="Bankzins nach 10 J. (± Pp.)"
    )
    vacancy_range = param.Range((2.0, 8.0), bounds=(0.0, 20.0), label="Mietausfall (%)")
    renovation_range = param.Range(
        (90.0, 130.0), bounds=(50.0, 200.0), label="Sanierung (% der Schätzung)"
    )
    running_range = param.Range(
        (80.0, 150.0), bounds=(50.0, 250.0), label="Verwaltung, Versicherung (%)"
    )
    n_samples = param.Integer(200, bounds=(50, 300), label="Anzahl Varianten")
    result = param.Parameter(default=None)
    error = param.String(default="")
    stale = param.Boolean(default=True)

    def __init__(self, **params):
        super().__init__(inputs=params.pop("inputs", None) or Inputs(), **params)
        self.inputs.param.watch(self._mark_stale, self.inputs.input_names())
        ranges = [p for p in self.param if p.endswith("_range")] + ["n_samples"]
        self.param.watch(self._mark_stale, ranges)

    def _mark_stale(self, *_events) -> None:
        self.stale = True

    def ranges(self) -> Ranges:
        def frac(r):
            return (r[0] / 100, r[1] / 100)

        return Ranges(
            inflation=frac(self.inflation_range),
            bank_rate_change_pp=tuple(self.bank_change_range),
            vacancy_rate=frac(self.vacancy_range),
            renovation_factor=frac(self.renovation_range),
            running_cost_factor=frac(self.running_range),
        )

    def compute(self, *_events) -> None:
        try:
            result = rent_uncertainty(self.inputs.to_project(), self.ranges(), self.n_samples)
        except ValueError as exc:
            self.param.update(result=None, error=str(exc), stale=False)
            return
        self.param.update(result=result, error="", stale=False)

    def kpi_items(self) -> list[Kpi]:
        r = self.result
        p10, p50, p90 = (r.rent_percentiles[q] for q in (10, 50, 90))
        items = [
            Kpi(
                "Miete ohne Unsicherheit",
                eur(r.base_rent, 2),
                "Erforderliche Miete aus Modus 1, mit den Werten der Startseite.",
                note="aus Modus 1",
            ),
            Kpi(
                "Median",
                eur(p50, 2),
                "Die Hälfte der Varianten braucht weniger, die Hälfte mehr.",
                note="pro Person und Monat",
            ),
            Kpi(
                "Spanne 10–90 %",
                f"{eur(p10)} – {eur(p90)}",
                "80 % der Varianten brauchen eine Miete in diesem Bereich.",
            ),
            Kpi(
                "Sichere Miete",
                eur(p90, 2),
                "Reicht in 90 % der Varianten. Der Abstand zur Miete ohne Unsicherheit ist "
                "ein Puffer für ungünstige Entwicklungen.",
                note=f"{eur(p90 - r.base_rent)} über Modus 1",
                tone="warning" if p90 > r.base_rent else "good",
            ),
        ]
        if r.failed:
            items.append(
                Kpi(
                    "Varianten ohne Lösung",
                    str(r.failed),
                    "In diesen Varianten reicht keine Miete bis 5.000 € pro Person; sie fehlen "
                    "in der Auswertung.",
                    tone="critical",
                )
            )
        return items

    def chart_items(self) -> list[tuple[go.Figure, str, str]]:
        r = self.result
        return [
            (
                charts.rent_distribution(
                    r.samples["required_rent"], r.base_rent, r.rent_percentiles[50], r.safe_rent
                ),
                UNCERTAINTY_HELP["rent_distribution"],
                "count",
            ),
            (charts.headroom_band(r.headroom_band), UNCERTAINTY_HELP["headroom_band"], "eur"),
            (charts.sensitivity(r.sensitivity), UNCERTAINTY_HELP["sensitivity"], "ratio"),
        ]

    @param.depends("result", "error", "stale")
    def results(self) -> pn.viewable.Viewable:
        if self.error:
            return pn.pane.Alert(f"Keine Lösung: {self.error}", alert_type="danger")
        if self.result is None:
            return pn.pane.Alert(
                "Spannen einstellen und auf „Berechnen“ klicken.", alert_type="info"
            )
        blocks = [chart_block(fig, text, fmt) for fig, text, fmt in self.chart_items()]
        notice = (
            [
                pn.pane.Alert(
                    "Annahmen wurden geändert. Die Ergebnisse unten sind veraltet; bitte neu "
                    "berechnen.",
                    alert_type="warning",
                )
            ]
            if self.stale
            else []
        )
        return pn.Column(*notice, kpi_grid(self.kpi_items()), *blocks, sizing_mode="stretch_width")

    def view(self) -> pn.viewable.Viewable:
        sliders = [
            with_info(
                pn.widgets.RangeSlider.from_param(
                    self.param[name], step=0.5 if "change" not in name else 0.25
                ),
                RANGE_INFO[name],
            )
            for name in RANGE_INFO
            if name != "n_samples"
        ]
        button = pn.widgets.Button(label="Berechnen", color="primary", sizing_mode="stretch_width")
        button.on_click(self.compute)
        levers = box(
            "Spannen",
            *sliders,
            with_info(
                pn.widgets.IntSlider.from_param(self.param.n_samples, step=50),
                RANGE_INFO["n_samples"],
            ),
            button,
            pn.pane.Markdown(
                "*Wahrscheinlichster Wert jeweils von der Startseite.*",
                styles={"font-size": "13px"},
            ),
            width=LEVER_WIDTH,
        )
        return pn.Row(
            levers,
            pn.Column(
                _on_demand("So wird gerechnet", UNCERTAINTY_TEXT),
                self.results,
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
        )


def _default_text(inputs: Inputs, name: str) -> str:
    parameter = inputs.param[name]
    value = parameter.default
    if isinstance(parameter, param.Selector):
        names = getattr(parameter, "names", None) or {}
        return next((k for k, v in names.items() if v == value), str(value))
    if isinstance(value, float) and "(€" in parameter.label:
        return eur(value)
    if isinstance(value, float):
        return f"{value:g}".replace(".", ",")
    return str(value)


def parameter_table(inputs: Inputs) -> str:
    """Markdown table of every input with its default and explanation."""
    rows = []
    for section, names in {**SECTIONS, **ADVANCED_SECTIONS}.items():
        for name in names:
            label = inputs.param[name].label
            info = INFO[name].replace("|", "/")
            rows.append(f"| {section} | {label} | {_default_text(inputs, name)} | {info} |")
    header = "| Bereich | Eingabe | Standard | Bedeutung |\n|---|---|---|---|\n"
    return header + "\n".join(rows)


def methodik_page(inputs: Inputs) -> pn.viewable.Viewable:
    text = files("app").joinpath("methodik.md").read_text(encoding="utf-8")
    return pn.Column(
        pn.pane.Markdown(text, max_width=1000),
        pn.pane.Markdown("## Eingaben und Standardwerte", max_width=1000),
        pn.pane.Markdown(parameter_table(inputs), sizing_mode="stretch_width"),
        _on_demand("Annahmen des Modells (A1–A9)", assumptions_table()),
        sizing_mode="stretch_width",
    )


def start_page(inputs: Inputs) -> pn.viewable.Viewable:
    mode_tiles = [
        box(title, pn.pane.Markdown(question, margin=(0, 0)), width=START_BOX_WIDTH)
        for title, question in MODES
    ]
    return pn.Column(
        pn.pane.Markdown(INTRO, max_width=1000, styles={"font-size": "15px"}),
        pn.FlexBox(*mode_tiles, sizing_mode="stretch_width"),
        pn.pane.HTML(
            "<h3 style='margin:8px 0 4px 0'>Annahmen einstellen</h3>", sizing_mode="stretch_width"
        ),
        inputs.all_inputs(),
        _on_demand("Annahmen des Modells (A1–A9)", assumptions_table()),
        pn.pane.Markdown(DISCLAIMER, max_width=1000, styles={"font-size": "13px"}),
        sizing_mode="stretch_width",
    )


PAGE_NAMES = [
    "Start",
    "Modus 1: Miete",
    "Modus 2: Vorsorge",
    "Modus 3: Zielmiete",
    "Unsicherheit",
    "Methodik",
]
# The template header carries the page navigation, so the tab bar itself is hidden.
HIDDEN_TAB_BAR_CSS = ":host > .bk-header { display: none; }"


def build_app() -> pn.viewable.Viewable:
    pn.extension("plotly")
    inputs = Inputs()
    pages = [
        start_page(inputs),
        Mode1(inputs=inputs).view(),
        Mode2(inputs=inputs).view(),
        Mode3(inputs=inputs).view(),
        UncertaintyPage(inputs=inputs).view(),
        methodik_page(inputs),
    ]
    return pn.Tabs(*zip(PAGE_NAMES, pages, strict=True), sizing_mode="stretch_width", dynamic=True)


def serve() -> pn.template.BaseTemplate:
    """App in a template whose fixed header holds the page navigation."""
    tabs = build_app()
    tabs.stylesheets = [HIDDEN_TAB_BAR_CSS]
    nav = pn.widgets.RadioButtonGroup(
        options={name: i for i, name in enumerate(PAGE_NAMES)},
        value=0,
        color="light",
        variant="outline",
        margin=(8, 20),
    )
    nav.link(tabs, value="active", bidirectional=True)
    return pn.template.FastListTemplate(
        title=TITLE,
        header=[nav],
        main=[tabs],
        accent=ACCENT,
        header_background=ACCENT,
        theme_toggle=False,
        main_max_width="1500px",
    )


if pn.state.served:
    serve().servable()
