# Methodology

The calculator models a joint housing project over 50 years in yearly steps. All amounts are
calculated in nominal terms; the charts show them adjusted for inflation, in purchasing power
of year 1.

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
  Actual maintenance is paid from the reserve, a separate pot outside the account.
- **Bank**: annuity or linear repayment over the chosen term; after the 10-year fixed-rate
  period the follow-up rate applies.
- **Subsidised loan**: annuity with a fixed rate.
- **Direct loans**: interest every year, repayment at the end of the term (5 or 10 years).
- **Member loans**: interest is added to the loan (compound interest), repayment including
  interest at the end of the term (default 15 years, adjustable under “Advanced”).
- **Arrears**: if a repayment falling due would push the account below the minimum reserve,
  only the possible part is paid. The rest is paid as soon as possible, oldest first, bears
  interest until then and must be settled within the chosen deadline. No new loans are
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
- **Uncertainty**: for five inputs with a range, variants are drawn (Latin hypercube,
  triangular distribution with the current value as the most likely) and the required rent
  is found for each, to 50 cents.

## Limits of the model

- **Taxes** are not modelled.
- **One member type**: member share and member loan are the same per person for everyone;
  mode 2 looks at a single member who does not affect the project financing.
- **Fixed loan types**: direct loans with 5 and 10 years, member loans with an adjustable
  term, one bank and one subsidised loan. Loans are not cancelled early, and no replacement
  is taken up after maturity.
- **Expected values**: apart from the uncertainty page, fixed values are used; vacancy,
  interest changes and inflation are assumptions, not forecasts.
- **Legal form** is not distinguished; its effect (e.g. higher administration costs in a
  cooperative) can be represented through the inputs.
- **Assumptions without sources**: the defaults are plausible starting points for an
  example group, not researched market values. Please replace them with your own offers and
  calculations.
- **German context**: terms and defaults (e.g. ground lease, KfW, transfer tax) follow
  German practice.

This calculator is a planning tool, not financial, tax or legal advice.
