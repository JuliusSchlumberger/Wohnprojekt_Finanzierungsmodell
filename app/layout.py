"""Visual building blocks shared by all pages: KPI tiles, chart blocks and boxes."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import panel as pn
import plotly.graph_objects as go

from app.charts import INK, INK_SECONDARY, SERIES, SURFACE, figure_table

ACCENT = SERIES[0]
BORDER = "#e3e2de"
BOX = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "border-radius": "10px",
    "padding": "12px 16px",
}
TONES = {"good": "#0ca30c", "warning": "#fab219", "critical": "#d03b3b"}
START_BOX_HEIGHT = 400
START_BOX_WIDTH = 300


@dataclass(frozen=True)
class Kpi:
    """One headline number; `help` is shown on demand, `note` under the value."""

    label: str
    value: str
    help: str
    note: str = ""
    tone: str = ""


def kpi_tile(kpi: Kpi, width: int = 230) -> pn.viewable.Viewable:
    note = f"<div style='font-size:12px;color:{INK_SECONDARY};margin-top:2px'>{kpi.note}</div>"
    return pn.Column(
        pn.Row(
            pn.pane.HTML(
                f"<div style='font-size:13px;color:{INK_SECONDARY}'>{kpi.label}</div>",
                margin=(0, 0),
                sizing_mode="stretch_width",
            ),
            pn.widgets.TooltipIcon(value=kpi.help, margin=(0, 0)),
            sizing_mode="stretch_width",
        ),
        pn.pane.HTML(
            f"<div style='font-size:22px;font-weight:600;color:{INK}'>{kpi.value}</div>"
            + (note if kpi.note else ""),
            margin=(4, 0, 0, 0),
        ),
        width=width,
        min_height=96,
        margin=(0, 12, 12, 0),
        styles={**BOX, "border-left": f"4px solid {TONES.get(kpi.tone, ACCENT)}"},
    )


def kpi_grid(kpis: list[Kpi]) -> pn.viewable.Viewable:
    return pn.FlexBox(*(kpi_tile(k) for k in kpis), sizing_mode="stretch_width")


def _table_pane(table: pd.DataFrame) -> pn.viewable.Viewable:
    formatted = table.map(lambda v: "" if pd.isna(v) else f"{v:,.0f} €".replace(",", "."))
    formatted.index.name = "Jahr" if table.index.dtype.kind in "iu" else ""
    return pn.pane.DataFrame(formatted, max_height=320, sizing_mode="stretch_width")


def chart_block(fig: go.Figure, help_text: str) -> pn.viewable.Viewable:
    """A chart with its reading guide and its values as a table, both on demand."""
    return pn.Column(
        pn.pane.Plotly(fig, sizing_mode="stretch_width", config={"displaylogo": False}),
        pn.Accordion(
            (
                "Wie lese ich diese Grafik?",
                pn.pane.Markdown(help_text, sizing_mode="stretch_width"),
            ),
            ("Werte als Tabelle", _table_pane(figure_table(fig))),
            active=[],
            sizing_mode="stretch_width",
        ),
        sizing_mode="stretch_width",
        margin=(0, 0, 16, 0),
        styles=BOX,
    )


def box(title: str, *objects, height: int | None = None, width: int | None = None):
    """A titled box with the common look; fixed `height` keeps rows of boxes even."""
    sizing = {"height": height} if height else {}
    if width:
        sizing["width"] = width
    else:
        sizing["sizing_mode"] = "stretch_width"
    return pn.Column(
        pn.pane.HTML(
            f"<div style='font-size:15px;font-weight:600;color:{INK}'>{title}</div>",
            margin=(0, 0, 6, 0),
        ),
        *objects,
        margin=(0, 12, 12, 0),
        styles=BOX,
        **sizing,
    )
