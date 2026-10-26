# Wohnprojekt-Finanzierungsdashboard

Static dashboard (Python → WebAssembly, GitHub Pages) for exploring how a housing
project owned by a common legal entity (eG, GmbH, KG) can be financed: required rent,
member retirement-provision view, and admissible investment for a target rent.
The full specification is in [docs/spec.md](docs/spec.md).

Status: calculation core (`model/`) and a local Panel app (`app/`) with the start page
modes 1 (required rent), 2 (member view), 3 (admissible investment) and an
a static sensitivity report on the required rent (1,000,000 sampled variants).

## Quick start

```bash
conda env create -f environment.yml
conda activate wohnprojekt
pytest
panel serve app/main.py --show   # opens the dashboard in the browser
```

```python
from model import simulate, required_rent
from model.presets import example_scenario

s = example_scenario()
rent = required_rent(s)  # EUR per person per month, start year
table = simulate(s, rent).table  # one row per year
```

## Layout

```
model/        calculation core (no UI): types, cashflow, solve, presets, member,
              exploration
app/          Panel dashboard: main (pages), widgets (inputs), charts (Plotly), layout
              (tiles, boxes), i18n (language and number formats)
app/locale/  UI texts in German, English and Dutch, plus the methodology page per language
app/data/     precomputed sensitivity report (exploration.json)
scripts/      build_site.py (browser version), site_entry.py (its entry point),
              explore_rent.py (regenerates app/data/exploration.json)
.github/      workflow: test, build and publish on GitHub Pages
tests/        unit tests and trias reference test
reference/    trias template, filled reference case and its reader/generator
docs/spec.md  specification
```

## Browser version (GitHub Pages)

The dashboard also runs entirely in the browser (Pyodide), without a server. Every push to
`main` runs lint and tests, builds it and publishes it on GitHub Pages
(`.github/workflows/pages.yml`). One-time setup in the repository on GitHub:
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

Build and try it locally:

```bash
python scripts/build_site.py --out site
python -m http.server 8000 --directory site   # then open http://localhost:8000
```

The first load downloads Pyodide and the Python packages (some tens of MB) and takes a
while; afterwards the browser caches them.

## Reference test

`reference/trias_reference_case.xlsx` is the empty trias template filled with
`reference/trias_case.json` and recalculated by Excel. Regenerate it on Windows with Excel:

```powershell
powershell -ExecutionPolicy Bypass -File reference/fill_trias.ps1
```
