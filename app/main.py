"""Panel app: start page and modes 1-3 on shared inputs; run `panel serve app/main.py`."""

from __future__ import annotations

import math

import numpy as np
import panel as pn
import param
import plotly.graph_objects as go

from app import charts
from app.layout import ACCENT, START_BOX_WIDTH, Kpi, box, chart_block, kpi_grid
from app.widgets import INFO, Inputs, eur, with_info
from model import Result, Scenario, max_investment, required_rent, simulate
from model.cashflow import capital_structure
from model.member import member_view
from model.presets import build_scenario
from model.solve import HEADROOM_TOLERANCE_EUR, is_affordable

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
    ("Mindestliquidität", "Das Konto fällt nie unter 6 Monatsmieten."),
    ("Steuern", "Nicht modelliert."),
    (
        "Direkt- und Mitgliederdarlehen",
        "Nachrangig und endfällig. Direktkredite laufen 5 oder 10 Jahre, Zinsen jährlich "
        "ausgezahlt; Mitgliederdarlehen 15 Jahre, Zinsen thesauriert. Was am Fälligkeitstag "
        "nicht ohne Unterschreiten der Mindestreserve zurückgezahlt werden kann, wird so "
        "schnell wie möglich nachgezahlt, spätestens nach 3 Jahren, und verzinst sich bis dahin.",
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
- **Mindestreserve**: das Konto darf nie unter 6 Monatsmieten fallen.
- **Rückstände**: würde eine fällige Rückzahlung das Konto unter die Reserve drücken,
  wird nur der mögliche Teil gezahlt; der Rest wird so schnell wie möglich nachgezahlt
  und muss nach spätestens 3 Jahren beglichen sein. Bis dahin fallen Zinsen an.
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
Kontostand am Jahresende im Vergleich zur Mindestreserve von 6 Monatsmieten (gestrichelt),
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
- **Linie**: wie viel davon am Jahresende noch offen ist. Sie muss nach spätestens 3 Jahren
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
        items = [
            Kpi(
                "Erforderliche Miete",
                eur(m["rent_per_person"], 2),
                "Niedrigste Miete pro Person und Monat, bei der das Konto in allen 50 Jahren "
                "über der Mindestreserve bleibt und jeder Rückstand nach höchstens 3 Jahren "
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
                    "gezahlt werden konnte (nominal). Er wird innerhalb von 3 Jahren "
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


PAGE_NAMES = ["Start", "Modus 1: Miete", "Modus 2: Vorsorge", "Modus 3: Zielmiete"]
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
    nav.jslink(tabs, value="active", bidirectional=True)
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
