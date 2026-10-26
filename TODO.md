- model/cashflow.py:51: `amortization_years` returns NaN for a zero-principal annuity with `initial_repayment_rate` (bank loan of exactly 0 EUR when own funds cover investment + opening liquidity).
- app/main.py: scenario and legal-form presets (spec 4.5, 4.6) deferred by decision; scenarios/ is empty.
- app/main.py: scenario comparison page and JSON export/import (spec 4.2 page 5, step 6) deferred by decision.
- app/locale/nl.py: Dutch texts are machine-quality translations by the assistant; have a native speaker review terms (erfpacht, directe leningen, inleg).
- app/widgets.py:36: euro input fields (FloatInput, numbro format "0,0") show 540,000 in every language; German/Dutch would expect 540.000.

## Review REVIEW_Finanzierungsmodell.md

- [H2a] model/cashflow.py: interest on liquidity and maintenance reserve (`cash_interest_rate`).
- [H2b] model/types.py:Rules: surplus option `bank_prepayment`, capped per year.
- [M3] model/cashflow.py: reserve release after bank payoff makes a one-year rent dip (year 31 = 7 EUR); smooth or tie reserve to pre-rebate rent.
- [M4] model/types.py: `Rules.exit_repayment` never read; wire into member_view or delete (spec A5).
- [M5] model/member.py:37: member path ignores project arrears and early-exit repayment; derive from result.tranches["member_loans"].
- [M6] model/solve.py: equity-like share counts short direct loans fully; revisit after H3 or warn.
- [N1] model/cashflow.py:291,339: `kinds` omits `member_tranches()`; include or remove MemberType.member_loan_amount.
- [N2] model/cashflow.py:_distribute: payout_15y pot after year 45 lapses at horizon.
- [N3] model/uncertainty.py:_rent_near: step 0 when guess is 0 -> endless loop; use max(step, 1.0).
- [N4] model/uncertainty.py:Ranges: initial vacancy and bank spread not sampled.
- [N5] app/locale/methodik_*.md: note that credited member-loan interest is taxable when credited.
- [N6] model/presets.py:ProjectInputs: defaults (bank 6 %, member loans 5 %, initial vacancy 20 %/3 y, admin+insurance 6.5 k) need sources.
