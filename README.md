# Wohnprojekt-Finanzierungsdashboard

Static dashboard (Python → WebAssembly, GitHub Pages) for exploring how a housing
project owned by a common legal entity (eG, GmbH, KG) can be financed: required rent,
member retirement-provision view, and admissible investment for a target rent.
The full specification is in [docs/spec.md](docs/spec.md).

Status: calculation core and mode 1 solver (`model/`). The app is not built yet.

## Quick start

```bash
conda env create -f environment.yml
conda activate wohnprojekt
pytest
```

```python
from model import simulate, required_rent
from model.presets import example_scenario

s = example_scenario()
rent = required_rent(s)  # EUR per m2 private area per month, start year
table = simulate(s, rent).table  # one row per year
```

## Layout

```
model/        calculation core (no UI): types, cashflow, solve, presets
tests/        unit tests and trias reference test
reference/    trias template, filled reference case and its reader/generator
docs/spec.md  specification
```

## Reference test

`reference/trias_reference_case.xlsx` is the empty trias template filled with
`reference/trias_case.json` and recalculated by Excel. Regenerate it on Windows with Excel:

```powershell
powershell -ExecutionPolicy Bypass -File reference/fill_trias.ps1
```
