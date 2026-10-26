"""Static sensitivity report on the required rent, from precomputed `app/data/exploration.json`."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files

import pandas as pd
import panel as pn
import param

from app import charts
from app.i18n import Translator
from app.layout import BOX, Kpi, box, chart_block, kpi_grid
from app.widgets import Inputs

DATA_FILE = "exploration.json"
# Share of the explained spread above which an input counts as acting linearly.
LINEAR_SHARE = 0.9
FINDING_COUNT = 4
# Non-linear part of the spread that earns an input its own finding beyond the top ones.
MIN_NONLINEAR_SHARE = 0.02
DIGITS = {"member_loan_term_years": 0}


@lru_cache(maxsize=1)
def load_exploration() -> dict | None:
    """The page data written by scripts/explore_rent.py, or None if not generated yet."""
    path = files("app.data").joinpath(DATA_FILE)
    if not path.is_file():
        return None
    return json.loads(path.read_text("utf-8"))


def _value(tr: Translator, name: str, value: float) -> str:
    shown = charts.explore_value(name, value)
    return f"{tr.number(shown, DIGITS.get(name, 1))} {tr(f'explore.unit.{name}')}"


def _range(tr: Translator, name: str, low: float, high: float) -> str:
    return f"{_value(tr, name, low)} – {_value(tr, name, high)}"


def _profile(tr: Translator, values: dict[str, float]) -> str:
    return "; ".join(f"{tr(f'explore.short.{n}')} {_value(tr, n, v)}" for n, v in values.items())


def findings(data: dict, tr: Translator) -> list[str]:
    """Bullet points stating the main results in words."""
    importance = pd.DataFrame(data["importance"]).T.sort_values("total", ascending=False)
    top = importance.index[:3]
    explained = importance["total"]
    lines = [
        tr(
            "explore.finding.drivers",
            first=tr(f"explore.short.{top[0]}"),
            first_share=tr.pct(explained[top[0]]),
            second=tr(f"explore.short.{top[1]}"),
            second_share=tr.pct(explained[top[1]]),
            third=tr(f"explore.short.{top[2]}"),
            top3_share=tr.pct(explained[top].sum()),
        )
    ]
    listed = list(importance.index[:FINDING_COUNT])
    nonlinear = (importance["total"] - importance["linear"]).drop(listed)
    if not nonlinear.empty and nonlinear.max() >= MIN_NONLINEAR_SHARE:
        listed.append(nonlinear.idxmax())
    for name in listed:
        row, curve = importance.loc[name], pd.DataFrame(data["per_parameter"][name])
        low, high = data["meta"]["ranges"][name]
        change = curve["p50"].iloc[-1] - curve["p50"].iloc[0]
        values = {
            "name": tr(f"explore.short.{name}"),
            "range": _range(tr, name, low, high),
            "change": tr.eur(abs(change)),
        }
        if row["linear"] >= LINEAR_SHARE * row["total"]:
            key = "explore.finding.linear_up" if change > 0 else "explore.finding.linear_down"
            lines.append(tr(key, **values))
        else:
            best = curve.loc[curve["p50"].idxmin(), "x"]
            lines.append(tr("explore.finding.nonlinear", best=_value(tr, name, best), **values))
    lines.append(tr("explore.finding.interactions", share=tr.pct(max(1.0 - explained.sum(), 0.0))))
    lines.append(
        tr(
            "explore.finding.cheapest",
            threshold=tr.eur(data["rent"]["p05"]),
            profile=_profile(tr, data["cheapest_median"]),
        )
    )
    lines.append(
        tr(
            "explore.finding.best",
            rent=tr.eur(data["rent"]["min"]),
            profile=_profile(tr, data["best"]),
        )
    )
    return lines


def assumptions_table(data: dict, tr: Translator) -> str:
    meta = data["meta"]
    rows = [
        f"| {tr(f'explore.param.{n}')} | {_range(tr, n, *meta['ranges'][n])} | "
        f"{_value(tr, n, meta['default_values'][n])} |"
        for n in meta["ranges"]
    ]
    header = (
        f"| {tr('explore.col.parameter')} | {tr('explore.col.range')} | "
        f"{tr('explore.col.default')} |\n|---|---|---|\n"
    )
    return header + "\n".join(rows)


def _curve_table(data: dict, tr: Translator) -> pd.DataFrame:
    rows = []
    for name, curve in data["per_parameter"].items():
        for i, x in enumerate(curve["x"]):
            rows.append(
                {
                    tr("explore.col.parameter"): tr(f"explore.short.{name}"),
                    tr("explore.col.value"): _value(tr, name, x),
                    tr("chart.explore.effects.min"): tr.eur(curve["min"][i]),
                    tr("chart.explore.effects.p50"): tr.eur(curve["p50"][i]),
                    "P10": tr.eur(curve["p10"][i]),
                    "P90": tr.eur(curve["p90"][i]),
                }
            )
    return pd.DataFrame(rows)


def _importance_table(data: dict, tr: Translator) -> pd.DataFrame:
    importance = pd.DataFrame(data["importance"]).T.sort_values("total", ascending=False)
    return pd.DataFrame(
        {
            tr("explore.col.parameter"): [tr(f"explore.short.{n}") for n in importance.index],
            tr("chart.explore.importance.linear"): [tr.pct(v) for v in importance["linear"]],
            tr("chart.explore.importance.total"): [tr.pct(v) for v in importance["total"]],
        }
    )


def _cheapest_table(data: dict, tr: Translator) -> pd.DataFrame:
    rows = []
    for name, shares in data["cheapest"].items():
        for i, x in enumerate(shares["x"]):
            rows.append(
                {
                    tr("explore.col.parameter"): tr(f"explore.short.{name}"),
                    tr("explore.col.value"): _value(tr, name, x),
                    tr("chart.explore.cheapest.all"): tr.pct(shares["all"][i]),
                    tr("chart.explore.cheapest.cheapest"): tr.pct(shares["cheapest"][i]),
                }
            )
    return pd.DataFrame(rows)


class ExplorationPage(param.Parameterized):
    """Report page; only the language and the chosen heatmap pair change what it shows."""

    inputs = param.ClassSelector(class_=Inputs)
    pair_x = param.Selector(objects=[])
    pair_y = param.Selector(objects=[])

    def __init__(self, **params):
        super().__init__(inputs=params.pop("inputs", None) or Inputs(), **params)
        self.data = load_exploration()
        if self.data is not None:
            order = sorted(
                self.data["importance"], key=lambda n: -self.data["importance"][n]["total"]
            )
            self.param.pair_x.objects = self.param.pair_y.objects = list(
                self.data["meta"]["ranges"]
            )
            self.pair_x, self.pair_y = order[0], order[1]

    @property
    def tr(self) -> Translator:
        return self.inputs.tr

    def kpi_items(self) -> list[Kpi]:
        tr, rent = self.tr, self.data["rent"]
        return [
            Kpi(
                tr("explore.kpi.base.label"),
                tr.eur(self.data["meta"]["base_rent"], 2),
                tr("explore.kpi.base.help"),
                note=tr("kpi.per_person_month"),
            ),
            Kpi(
                tr("explore.kpi.median.label"),
                tr.eur(rent["p50"], 2),
                tr("explore.kpi.median.help"),
                note=tr("kpi.per_person_month"),
            ),
            Kpi(
                tr("explore.kpi.spread.label"),
                f"{tr.eur(rent['p10'])} – {tr.eur(rent['p90'])}",
                tr("explore.kpi.spread.help"),
            ),
            Kpi(
                tr("explore.kpi.best.label"),
                tr.eur(rent["min"], 2),
                tr("explore.kpi.best.help"),
                tone="good",
            ),
        ]

    def pair_key(self) -> tuple[str, bool]:
        key = f"{self.pair_x}|{self.pair_y}"
        if key in self.data["pairs"]:
            return key, False
        return f"{self.pair_y}|{self.pair_x}", True

    @param.depends("pair_x", "pair_y")
    def pair_chart(self) -> pn.viewable.Viewable:
        tr = self.tr
        if self.pair_x == self.pair_y:
            return pn.pane.Alert(tr("explore.pair_same"), alert_type="info")
        key, swapped = self.pair_key()
        pair = dict(self.data["pairs"][key])
        if swapped:
            z = pd.DataFrame(pair["z"]).T.to_numpy().tolist()
            pair = {"x": pair["y"], "y": pair["x"], "z": z}
        fig = charts.pair_heatmap(pair, self.pair_x, self.pair_y, tr)
        return pn.pane.Plotly(fig, sizing_mode="stretch_width", config={"displaylogo": False})

    def pair_block(self) -> pn.viewable.Viewable:
        tr = self.tr
        for name in ("pair_x", "pair_y"):
            self.param[name].label = tr(f"label.explore_{name}")
            self.param[name].names = {
                tr(f"explore.param.{n}"): n for n in self.data["meta"]["ranges"]
            }
        selects = pn.Row(
            pn.widgets.Select.from_param(self.param.pair_x, width=320),
            pn.widgets.Select.from_param(self.param.pair_y, width=320),
        )
        return pn.Column(
            selects,
            self.pair_chart,
            pn.Accordion(
                (tr("ui.how_to_read"), pn.pane.Markdown(tr("help.explore.pair"))),
                active=[],
                sizing_mode="stretch_width",
            ),
            sizing_mode="stretch_width",
            margin=(0, 0, 16, 0),
            styles=BOX,
        )

    def view(self) -> pn.viewable.Viewable:
        tr = self.tr
        if self.data is None:
            return pn.pane.Alert(tr("explore.missing"), alert_type="warning")
        meta = self.data["meta"]
        inflation = tr.pct(meta["defaults"]["inflation"])
        valid = meta["n"] - meta["excluded_bank"] - meta["infeasible"]
        intro = tr(
            "explore.intro",
            n=tr.number(meta["n"], 0),
            excluded=tr.pct(meta["excluded_bank"] / meta["n"]),
            min_share=tr.pct(meta["min_equity_like_share"]),
            valid=tr.number(valid, 0),
        )
        bullets = "\n".join(f"- {line}" for line in findings(self.data, tr))
        importance = pd.DataFrame(self.data["importance"]).T.sort_values("total", ascending=False)
        return pn.Column(
            pn.pane.Markdown(f"# {tr('explore.title')}\n\n{intro}", sizing_mode="stretch_width"),
            box(
                tr("explore.ranges_title"),
                pn.pane.Markdown(assumptions_table(self.data, tr), sizing_mode="stretch_width"),
                pn.pane.Markdown(
                    tr("explore.ranges_note", inflation=inflation), styles={"font-size": "13px"}
                ),
            ),
            kpi_grid(self.kpi_items()),
            box(
                tr("explore.findings_title"),
                pn.pane.Markdown(bullets, sizing_mode="stretch_width"),
            ),
            chart_block(
                charts.importance(importance, tr),
                tr("help.explore.importance"),
                tr,
                table=_importance_table(self.data, tr),
            ),
            chart_block(
                charts.parameter_effects(self.data["per_parameter"], tr),
                tr("help.explore.effects"),
                tr,
                table=_curve_table(self.data, tr),
            ),
            self.pair_block(),
            chart_block(
                charts.cheapest_profile(self.data["cheapest"], tr),
                tr("help.explore.cheapest", share=tr.pct(meta["cheapest_share"])),
                tr,
                table=_cheapest_table(self.data, tr),
            ),
            box(
                tr("explore.limits_title"),
                pn.pane.Markdown(
                    tr("explore.limits", inflation=inflation), sizing_mode="stretch_width"
                ),
            ),
            sizing_mode="stretch_width",
        )
