# Repo facts

- Spec: docs/spec.md (German). UI texts live in `app/locale/{de,en,nl}.py` (keys, German is the
  reference) and `app/locale/methodik_*.md`; code, names, docstrings English. A new UI text needs
  a key in all three files (`tests/test_i18n.py` checks keys and placeholders).
- Env: `conda env create -f environment.yml` → env `wohnprojekt` (Python 3.12).
- Entry points: `model.simulate(scenario, rent_per_person)`, `model.required_rent(scenario)`,
  `model.max_investment(...)`, `model.member.member_view(...)`,
  `model.uncertainty.rent_uncertainty(ProjectInputs(), Ranges(), n)`,
  `model.presets.example_scenario()`, `model.presets.build_scenario(ProjectInputs())` (app inputs).
- Commands (from repo root, env active): `pytest` (all, ~2 s), `pytest -m "not reference"`,
  `ruff check . && ruff format --check .`, `python scripts/build_site.py --out site`
  (browser build; CI does the same and publishes to GitHub Pages).
- Protected: `reference/Finanzplan_Wohnprojekte_Stiftung_trias.xlsx` (original template),
  `reference/trias_reference_case.xlsx` (regenerate only via `reference/fill_trias.ps1`).

## Conventions

- Year index t: 0 = opening state (investment financed, opening liquidity), 1..T operating years.
- Rent input is EUR per person per month in year 1, inflation-indexed afterwards.
- Opening liquidity defaults to `min_liquidity_months` of year-1 rent, financed by the
  residual tranche (normally the bank loan).
- Bank and subsidy loans are "senior"; the A4 surplus rule applies after they are repaid.

## Baselines

- `required_rent(example_scenario())` = 558.76 EUR per person (11.18 per total m2).
- `required_rent(build_scenario(ProjectInputs()))` = 903.55 EUR per person (app defaults).
- trias reference case: all 12 series equal to machine precision, years 1-30.
