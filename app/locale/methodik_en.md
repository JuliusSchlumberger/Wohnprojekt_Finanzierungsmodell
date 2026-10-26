# Methodology

The calculator models a joint housing project over 50 years in yearly steps. All amounts are
calculated in nominal terms; the charts show them either adjusted for inflation, in
purchasing power of year 1, or nominal. All interest rates are entered as a spread above
inflation in percentage points; the nominal rate is inflation plus spread, at least 0 %.

## Financing at the start

- **Total investment** = house + land (only if bought) + purchase costs on both
  + renovation.
- **Own funds**: member shares (Einlagen) and member loans (Mitgliederdarlehen), each per
  person; direct loans (Direktkredite) with terms of 5 and 10 years; subsidised loans
  (Förderdarlehen, at most as high as the renovation costs).
- **Bank loan** closes the gap to the total investment plus opening liquidity. The opening
  liquidity is the minimum reserve of the first year and is financed as well.
- **Equity check**: member shares, member loans and direct loans together relative to the
  total investment, compared with the minimum share the bank requires.

## Every year

**new balance = old balance + rent income − running costs − interest − repayment**,
plus repayments of direct and member loans falling due and the use of the surplus.

- **Rent income**: rent per person × persons × 12, minus rent loss (a separate, usually
  higher rate in the first three years). The rent rises with inflation.
- **Running costs**: contribution to the maintenance reserve, administration, insurance and,
  under a ground lease (Erbbaurecht), the ground rent (Erbbauzins); all rise with inflation.
  The contribution is a fixed share of the reconstruction value (60 % of house plus
  renovation, without the land) and is spent on maintenance in the same year.
- **Bank**: annuity or linear repayment over the chosen term; after the 10-year fixed-rate
  period the follow-up rate applies.
- **Subsidised loan**: annuity with a fixed rate.
- **Direct loans**: interest every year, repayment at the end of the term (5 or 10 years).
  For the 10-year direct loans the chosen share (default 50 %) is replaced by new direct
  loans at every maturity; only the rest is repaid.
- **Member loans**: interest is added to the loan (compound interest), repayment including
  interest at the end of the term (default 15 years, adjustable under “Advanced”). The
  repayment comes either from the account (with arrears, see below), from a new bank loan
  at the follow-up rate (term: rest of the bank term, at least 10 years) or from new
  10-year direct loans at the 10-year direct loan rate. The new loan covers the full amount
  due including interest and is serviced from the following year.
- **Arrears**: if a repayment falling due would push the account below the minimum reserve,
  only the possible part is paid. The rest is paid as soon as possible, oldest first, bears
  interest until then and must be settled within the chosen deadline. Apart from the chosen
  refinancing of the member loans, no new loans are
  taken up.
- **Surplus**: if no arrears are open and the account above the reserve covers all
  remaining direct and member loans, the rest is taken out: as a rent reduction, as a rent
  refund every 15 years or as a solidarity transfer (Solidartransfer). Once bank and subsidy
  are repaid, the debt service set free is used in the same way.

## What is searched for

- **Mode 1, required rent**: the lowest starting rent at which the account stays above the
  minimum reserve in all 50 years and every arrear is settled in time. Found by bisection to
  the cent.
- **Mode 2, members**: wealth of a member in the project (invested rent saving, repayments,
  share in real terms, loan with compound interest) compared with market rent and invested
  capital, both at the same alternative return and adjusted for inflation.
- **Mode 3, target rent**: the largest total investment a target rent can carry, limited by
  the bank's equity requirement. Land, house and renovation are scaled in proportion to the
  cost estimate.
- **Uncertainty**: a fixed sensitivity analysis. Eight assumptions (bank rate and its change
  after 10 years, rent loss, amount, rate and term of the member loans, amount and rate of the
  10-year direct loans) are drawn evenly in 1,000,000 variants (Latin hypercube); all other
  inputs stay at their defaults. Variants below the equity requirement of the bank are
  excluded. For each variant the required rent is found to 50 cents; the page evaluates
  shares of variance (linear and total), the rent per assumption with the lowest reachable
  rent (Pareto front), pairs of assumptions and the assumptions of the cheapest 5 %.

## Limits of the model

- **Taxes** are not modelled.
- **One member type**: member share and member loan are the same per person for everyone;
  mode 2 looks at a single member who does not affect the project financing.
- **Fixed loan types**: direct loans with 5 and 10 years, member loans with an adjustable
  term, one bank and one subsidised loan. Loans are not cancelled early, and no replacement
  is taken up after maturity, except the optional refinancing of the member loans and the
  re-raising of the 10-year direct loans.
- **Expected values**: apart from the sensitivity analysis, fixed values are used; vacancy,
  interest changes and inflation are assumptions, not forecasts.
- **Legal form** is not distinguished; its effect (e.g. higher administration costs in a
  cooperative) can be represented through the inputs.
- **Assumptions without sources**: the defaults are plausible starting points for an
  example group, not researched market values. Please replace them with your own offers and
  calculations.
- **German context**: terms and defaults (e.g. ground lease, KfW, transfer tax) follow
  German practice.

This calculator is a planning tool, not financial, tax or legal advice.
