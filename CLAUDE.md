# Repo facts

- Spec: docs/spec.md (German). UI text German; code, names, docstrings English.
- Env: `conda env create -f environment.yml` → env `wohnprojekt` (Python 3.12).
- Entry points: `model.simulate(scenario, rent_per_m2)`, `model.required_rent(scenario)`,
  `model.presets.example_scenario()`.
- Commands (from repo root, env active): `pytest` (all, ~2 s), `pytest -m "not reference"`,
  `ruff check . && ruff format --check .`.
- Protected: `reference/Finanzplan_Wohnprojekte_Stiftung_trias.xlsx` (original template),
  `reference/trias_reference_case.xlsx` (regenerate only via `reference/fill_trias.ps1`).

## Conventions

- Year index t: 0 = opening state (investment financed, opening liquidity), 1..T operating years.
- Rent input is EUR per m2 private area per month in year 1; common areas are not rented.
- Opening liquidity defaults to `min_liquidity_months` of year-1 rent, financed by the
  residual tranche (normally the bank loan).
- Bank and subsidy loans are "senior"; the A4 surplus rule applies after they are repaid.

## Baselines

- `required_rent(example_scenario())` = 27.94 EUR/m2 private (11.18 per total m2).
- trias reference case: all 12 series equal to machine precision, years 1-30.
