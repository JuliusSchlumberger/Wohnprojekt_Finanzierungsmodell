# Repo facts

- Spec: docs/spec.md (German). UI texts live in `app/locale/{de,en,nl}.py` (keys, German is the
  reference) and `app/locale/methodik_*.md`; code, names, docstrings English. A new UI text needs
  a key in all three files (`tests/test_i18n.py` checks keys and placeholders).
- Env: `conda env create -f environment.yml` → env `wohnprojekt` (Python 3.12).
- Entry points: `model.simulate(scenario, rent_per_person)`, `model.required_rent(scenario)`,
  `model.max_investment(...)`, `model.member.member_view(...)`,
  `model.exploration.explore(...)` / `summarize(...)` (sensitivity report data),
  `model.presets.example_scenario()`, `model.presets.build_scenario(ProjectInputs())` (app inputs).
- Commands (from repo root, env active): `pytest` (all, ~2 s), `pytest -m "not reference"`,
  `ruff check . && ruff format --check .`, `python scripts/build_site.py --out site`
  (browser build; CI does the same and publishes to GitHub Pages),
  `python scripts/explore_rent.py` (regenerates `app/data/exploration.json`, ~10-15 min on
  14 cores; needed after any change to defaults or model; a test checks the defaults).
- Protected: `reference/Finanzplan_Wohnprojekte_Stiftung_trias.xlsx` (original template),
  `reference/trias_reference_case.xlsx` (regenerate only via `reference/fill_trias.ps1`).

## Conventions

- Year index t: 0 = opening state (investment financed, opening liquidity), 1..T operating years.
- Amounts entered for year 1 (rent, running costs) are paid in year 1 (index 1.00), indexed
  from year 2.
- Opening liquidity defaults to `min_liquidity_months` of year-1 rent, financed by the
  residual tranche (normally the bank loan).
- Bank and subsidy loans are "senior"; the A4 surplus rule applies after they are repaid.
- App rate inputs are spreads above inflation in pp (`*_spread_pp`); the model takes nominal
  rates = max(inflation + spread, 0). Charts default to real values (year-1 purchasing power).

## Baselines

- `required_rent(example_scenario())` = 546.31 EUR per person.
- `required_rent(build_scenario(ProjectInputs()))` = 843.47 EUR per person (app defaults;
  deciding year 1, reserve).
- Mode 2 defaults: break-even market rent 848.80 EUR per person at 0 pp return gap.
- trias reference case: all 12 series equal to machine precision, years 1-30.
