"""English UI texts; German legal and financing terms are given in brackets on first use."""

TEXTS = {
    # App frame and navigation
    "app.title": "Housing project calculator",
    "app.language": "Language",
    "nav.start": "Start",
    "nav.mode1": "Mode 1: Rent",
    "nav.mode2": "Mode 2: Members",
    "nav.mode3": "Mode 3: Target rent",
    "nav.uncertainty": "Uncertainty",
    "nav.methodik": "Methodology",
    # Start page
    "start.intro": """
With this calculator a housing project group can work out how a house bought together, or
held on a ground lease (Erbbaurecht), can be financed. Set all assumptions here; the most
important ones can also be changed directly on the mode pages. Every change applies to all
pages at once. The **?** next to a field or a key figure explains what is behind it.
""",
    "start.mode1.question": "What rent per person does our house need at least?",
    "start.mode2.question": "Does the project pay off for a member compared with market rent?",
    "start.mode3.question": "How much house can our group afford at a target rent?",
    "start.heading": "Set assumptions",
    "start.disclaimer": (
        "**Disclaimer:** This calculator is a planning tool, not financial, tax or legal "
        "advice. All results depend on the assumptions."
    ),
    "start.advanced": "Advanced: operations, reserve, purchase costs, subsidy terms",
    # Assumptions A1-A9
    "assumptions.title": "Model assumptions (A1–A9)",
    "assumptions.header": "| No. | Assumption | Definition |",
    "assumption.1.title": "Ownership model",
    "assumption.1.text": (
        "A joint legal entity (cooperative/eG, GmbH, GmbH & Co. KG) buys the house or holds it "
        "on a ground lease (Erbbaurecht). Members pay a usage fee (“rent”). No individual "
        "ownership."
    ),
    "assumption.2.title": "Rent unit",
    "assumption.2.text": (
        "Rent per person and month, the same for everyone. Shared spaces are included."
    ),
    "assumption.3.title": "Capital contributions",
    "assumption.3.text": "Individuals contribute different amounts (member types).",
    "assumption.4.title": "Money set free",
    "assumption.4.text": (
        "Once bank and subsidised loans are repaid and all direct and member loans are "
        "covered: rent reduction, rent refund every 15 years or a solidarity transfer to a "
        "next project."
    ),
    "assumption.5.title": "Member shares",
    "assumption.5.text": (
        "Repaid inflation-indexed on leaving; new members buy in at the same value. The amount "
        "in the project stays constant."
    ),
    "assumption.6.title": "Horizon and inflation",
    "assumption.6.text": (
        "50 years. Rent, running costs and ground rent rise with inflation; interest and "
        "repayment are fixed in nominal terms."
    ),
    "assumption.7.title": "Minimum liquidity",
    "assumption.7.text": (
        "The account never falls below the minimum reserve (default 6 months' rent)."
    ),
    "assumption.8.title": "Taxes",
    "assumption.8.text": "Not modelled.",
    "assumption.9.title": "Direct and member loans",
    "assumption.9.text": (
        "Subordinated and repaid at maturity. Direct loans (Direktkredite) run 5 or 10 years "
        "with yearly interest; member loans (Mitgliederdarlehen) have an adjustable term "
        "(default 15 years) with accrued interest. What cannot be repaid on the due date "
        "without falling below the minimum reserve is paid as soon as possible, within a "
        "deadline (default 3 years), and bears interest until then."
    ),
    # Input sections
    "section.house": "House and costs",
    "section.group": "Group and operations",
    "section.own_funds": "Own funds",
    "section.direct_loans": "Direct loans",
    "section.bank": "Bank and subsidy",
    "section.surplus": "Surplus and target rent",
    "section.member_capital": "Member: capital (mode 2)",
    "section.member_compare": "Member: comparison (mode 2)",
    "section.adv_operations": "Operations",
    "section.adv_liquidity": "Liquidity and arrears",
    "section.adv_purchase": "Purchase and ground lease",
    "section.adv_subsidy": "Subsidised loans",
    "section.adv_member_loans": "Member loans",
    # Input labels
    "label.land_price": "Land (€)",
    "label.building_price": "House (€)",
    "label.renovation_cost": "Renovation (€)",
    "label.tenure": "Land",
    "label.persons": "Number of persons",
    "label.equity_per_person": "Member share per person (€)",
    "label.member_loan_per_person": "Member loan per person (€)",
    "label.direct_loans_5y": "Direct loans 5 years (€)",
    "label.direct_loans_10y": "Direct loans 10 years (€)",
    "label.subsidy": "Subsidised loan (€)",
    "label.bank_repayment": "Bank repayment type",
    "label.bank_term_years": "Bank term (years)",
    "label.bank_rate_change": "Bank interest after 10 years",
    "label.inflation_pct": "Inflation (%)",
    "label.surplus_use": "After bank and subsidised loans are repaid",
    "label.min_equity_like_pct": "Minimum equity + subordinated (%)",
    "label.target_rent": "Target rent per person (€/month)",
    "label.maintenance_reserve_pct": "Maintenance reserve (%)",
    "label.vacancy_pct": "Rent loss (%)",
    "label.initial_vacancy_pct": "Rent loss first 3 years (%)",
    "label.maintenance_rate_pct": "Maintenance (%)",
    "label.admin_cost_per_year": "Administration per year (€)",
    "label.insurance_per_year": "Insurance per year (€)",
    "label.min_liquidity_months": "Minimum reserve (months' rent)",
    "label.max_arrears_years": "Arrears at most (years)",
    "label.ancillary_cost_pct": "Purchase costs (%)",
    "label.leasehold_rate_pct": "Ground rent (%)",
    "label.subsidy_term_years": "Term subsidised loans (years)",
    "label.member_loan_term_years": "Term member loans (years)",
    "label.member_type": "Member type",
    "label.member_equity": "Member share (€)",
    "label.member_loan_personal": "Member loan (€)",
    "label.entry_year": "Moving in (year)",
    "label.exit_year": "Moving out (year)",
    "label.market_rent": "Market rent per person (€/month)",
    "label.inflation_range": "Inflation (%)",
    "label.bank_change_range": "Bank interest after 10 y. (± pp)",
    "label.vacancy_range": "Rent loss (%)",
    "label.renovation_range": "Renovation (% of estimate)",
    "label.running_range": "Administration, insurance (%)",
    "label.n_samples": "Number of variants",
    # Options of choice inputs
    "option.tenure.purchase": "Purchase",
    "option.tenure.leasehold": "Ground lease",
    "option.bank_repayment.annuity": "Annuity",
    "option.bank_repayment.linear": "Linear",
    "option.bank_rate_change.down": "falls",
    "option.bank_rate_change.same": "stays",
    "option.bank_rate_change.up": "rises",
    "option.surplus_use.rent_reduction": "Rent reduction",
    "option.surplus_use.payout_15y": "Rent refund every 15 years",
    "option.surplus_use.next_project": "Solidarity transfer",
    "option.member_type.custom": "Own values",
    "option.member_type.low": "Little capital",
    "option.member_type.mid": "Medium",
    "option.member_type.high": "Much",
    # Input explanations
    "info.land_price": (
        "Purchase price of the land. Under a ground lease (Erbbaurecht) it is not bought; the "
        "amount then counts as the land value on which the ground rent (rate under "
        "“Advanced”) is charged."
    ),
    "info.building_price": "Purchase price of the house without the land.",
    "info.renovation_cost": (
        "Costs of renovation and conversion. Subsidised loans can only be used for these."
    ),
    "info.tenure": (
        "Purchase: the land is financed as well, including the purchase costs on it. Ground "
        "lease (Erbbaurecht): the land is not bought; instead a yearly ground rent "
        "(Erbbauzins) is charged on the land value (default 4 %, under “Advanced”), rising "
        "with inflation."
    ),
    "info.persons": "Number of people who live in the project and pay rent.",
    "info.equity_per_person": (
        "Member share per person (cooperative share or contribution to the legal entity, "
        "Einlage). Shares cost no interest and are not repaid on a schedule. Whoever moves "
        "out gets the share back inflation-indexed; new members buy in at the same value. The "
        "amount in the project therefore stays constant."
    ),
    "info.member_loan_per_person": (
        "Member loan (Mitgliederdarlehen) per person. Interest is not paid out but added to "
        "the loan every year (accrued). At the end of the term (default 15 years, under "
        "“Advanced”) everything is repaid at once, including compound interest."
    ),
    "info.direct_loans_5y": (
        "Subordinated private loans from supporters (Direktkredite) over 5 years. Interest is "
        "paid yearly, the amount is repaid at once after 5 years. Because they are "
        "subordinated, banks usually count direct loans as quasi-equity."
    ),
    "info.direct_loans_10y": (
        "As above, but over 10 years. Longer terms usually carry a higher interest rate."
    ),
    "info.subsidy": (
        "Subsidised loan (Förderdarlehen, e.g. KfW or a regional development bank) repaid as "
        "an annuity; rate and term under “Advanced” (default 1.5 % over 30 years). Only "
        "usable for renovation costs, so at most as high as these. Does not count as "
        "quasi-equity."
    ),
    "info.bank_repayment": (
        "Annuity: constant instalment of interest and repayment, a lot of interest at first. "
        "Linear: constant repayment; the instalment is higher at first and then falls."
    ),
    "info.bank_term_years": "Term after which the bank loan is fully repaid.",
    "info.bank_rate_change": (
        "After 10 years the fixed-rate period ends. For the follow-up financing the rate is "
        "lowered by 1 percentage point, kept or raised."
    ),
    "info.surplus_use": (
        "Applies from the year in which bank and subsidised loans are repaid (A4). Rent "
        "reduction: the rent falls by the debt service set free. Rent refund: the amount is "
        "saved up and paid back to all members every 15 years. Solidarity transfer "
        "(Solidartransfer): the money goes to a next project. The required starting rent "
        "usually does not change, only the course afterwards."
    ),
    "info.min_equity_like_pct": (
        "Banks usually require equity and subordinated funds (member shares, member loans, "
        "direct loans) to cover a minimum share of the total investment, often 20 to 30 %. "
        "Enter your bank's requirement here."
    ),
    "info.vacancy_pct": (
        "Share of the rent that is lost on average, e.g. through vacancy when people move or "
        "unpaid rent. Applies from year 4."
    ),
    "info.initial_vacancy_pct": (
        "Rent loss in the first 3 years, while the house is still being moved into and renovated."
    ),
    "info.maintenance_rate_pct": (
        "What ongoing maintenance actually costs, in % of the reconstruction value per year. "
        "Paid from the maintenance reserve."
    ),
    "info.admin_cost_per_year": (
        "Administration, bookkeeping, audit (for a cooperative the auditing association), "
        "bank fees. Rises with inflation."
    ),
    "info.insurance_per_year": "Building and liability insurance. Rises with inflation.",
    "info.min_liquidity_months": (
        "The account must always hold at least this many months' rent. It is financed by the "
        "bank loan at the start. More reserve means more safety, but also a higher rent."
    ),
    "info.max_arrears_years": (
        "How long a due repayment of direct or member loans may be deferred at most. 0 means: "
        "everything must be paid on time."
    ),
    "info.ancillary_cost_pct": (
        "Real estate transfer tax, notary, land register and possibly an agent, in % of the "
        "purchase price of the house and (if bought) the land. The transfer tax "
        "(Grunderwerbsteuer) is 3.5 to 6.5 % depending on the German state."
    ),
    "info.leasehold_rate_pct": (
        "Yearly ground rent (Erbbauzins) in % of the land value. Rises with inflation. Only "
        "applies to a ground lease."
    ),
    "info.member_loan_term_years": (
        "After this many years member loans are repaid at once, including accrued interest. "
        "Longer terms push the large repayment back but let more compound interest accrue."
    ),
    "info.subsidy_term_years": "Term of the subsidised loans; they are repaid as an annuity.",
    "info.maintenance_reserve_pct": (
        "This share of the reconstruction value goes into the maintenance reserve every year, "
        "rising with inflation. Ongoing maintenance (default 1.5 %, under “Advanced”) is paid "
        "from it; the rest is saved for larger works. The reserve is a separate pot and does "
        "not count as liquidity."
    ),
    "info.member_type": (
        "Presets for this member's share and member loan. “Own values” lets you set them freely."
    ),
    "info.member_equity": (
        "This member's share in today's money. It is paid in inflation-indexed on moving in "
        "and repaid inflation-indexed on moving out."
    ),
    "info.member_loan_personal": (
        "This member's member loan. It accrues interest at the member loan rate and is repaid "
        "with compound interest at the end of the term or in the year after moving out."
    ),
    "info.entry_year": "Year of moving in, counted from the project start (0 = from the start).",
    "info.exit_year": ("Year of moving out. Share and loan come back in the year after."),
    "info.market_rent": (
        "What a comparable flat or room costs on the market per person and month, in the same "
        "unit as the project rent. Rises with inflation."
    ),
    "info.target_rent": (
        "The rent one person wants or is able to pay per month in the first year. It rises "
        "with inflation afterwards."
    ),
    "info.bank_loan": (
        "The bank loan closes the gap: total investment + opening liquidity (minimum reserve) "
        "− member shares − member loans − direct loans − subsidised loans. Because the opening "
        "liquidity depends on the rent, it is calculated together with the rent."
    ),
    "info.inflation_range": "Range of yearly inflation. Most likely value: start page.",
    "info.bank_change_range": (
        "Change of the bank rate after the fixed-rate period (10 years), in percentage points. "
        "Most likely value: the choice on the start page (falls −1, stays 0, rises +1)."
    ),
    "info.vacancy_range": "Range of rent loss from year 4. Most likely value: start page.",
    "info.renovation_range": (
        "Renovation costs in % of your estimate. 130 % means: renovation is 30 % more "
        "expensive. Most likely value: 100 %."
    ),
    "info.running_range": (
        "Administration and insurance in % of your estimate. Most likely value: 100 %."
    ),
    "info.n_samples": (
        "More variants make the result more stable but take longer (in the browser about "
        "2.5 seconds per 100 variants)."
    ),
    # Summaries under input boxes
    "summary.costs": "Purchase costs ({rate}): **{ancillary}**  \nTotal investment: **{total}**",
    "summary.costs_unknown": "Total investment: –",
    "summary.capital": (
        "Member shares total: **{equity}**  \nMember loans total: **{member_loans}**"
    ),
    # Shared page elements
    "ui.levers": "Key inputs",
    "ui.more_on_start": "*All other assumptions are on the start page.*",
    "ui.how_computed": "How it is calculated",
    "ui.no_solution": "No solution: {error}",
    "ui.how_to_read": "How to read this chart",
    "ui.values_table": "Values as a table",
    "ui.year": "Year",
    # Errors
    "error.subsidy_above_renovation": (
        "Subsidised loans ({subsidy}) can only be used for renovation and exceed the "
        "renovation costs ({renovation})."
    ),
    "error.zero_price": "Land and house cannot both cost €0.",
    "error.own_funds_above_investment": (
        "Own funds and subsidised loans ({own}) exceed the total investment ({total}). Please "
        "reduce the amounts."
    ),
    "error.exit_before_entry": "Moving out must come after moving in.",
    "error.rent_too_low_for_own_funds": (
        "Even a house worth your own funds ({lower}) needs more than {target} rent per "
        "person. Raise the target rent or change your own funds."
    ),
    "error.no_upper_bound": "No upper limit for the investment found; please check the inputs.",
    "error.bank_rule_no_house": (
        "The bank's equity requirement allows no house that can take up your own funds: "
        "member shares, member loans and direct loans are too small relative to the "
        "subsidised loans."
    ),
    # Bank loan and equity check
    "bank.line": "**Bank loan (automatic): {amount}**",
    "bank.check": (
        "Equity + subordinated: {equity_like} = {share} of the total investment (minimum "
        "{min_share}). Bank loan : equity + subordinated = {ratio}."
    ),
    "bank.missing": (
        "{check} {gap} of member shares, member loans or direct loans are missing; a bank "
        "would probably not finance this."
    ),
    # Methods
    "method.mode1": """
The model calculates 50 years in yearly steps. Each year:
**new balance = old balance + rent income − running costs − interest − repayment**
(minus repayments of direct and member loans that fall due, rent reduction from the surplus,
rent refund or solidarity transfer).

- **Rent income**: rent × persons × 12, minus rent loss (higher in the first 3 years).
- **Running costs**: contribution to the maintenance reserve (share of the reconstruction
  value), administration and insurance.
- **Interest and repayment**: per loan according to its terms, fixed in nominal terms.
- **Minimum reserve**: the account must never fall below the minimum reserve (default
  6 months' rent, under “Advanced”).
- **Arrears**: if a repayment falling due would push the account below the reserve, only
  the possible part is paid; the rest is paid as soon as possible and must be settled
  within a deadline (default 3 years, under “Advanced”). Interest is due until then.
- **Surplus (A4)**: only when no arrears are open and the account above the reserve could
  cover all remaining direct and member loans does the rest go to rent reduction, rent
  refund or solidarity transfer.

The **required rent** is the lowest starting rent that meets these conditions in all
50 years, to the cent. The **deciding year** is the year in which the calculation would
fail with slightly less rent: there the account would fall below the reserve or arrears
would stay open too long. Years in which the account sits exactly on the reserve because
a repayment is deferred do not decide the rent.
""",
    "method.mode2": """
The basis is the required rent from mode 1 with all assumptions of the start page. Two
paths for a member are compared, both adjusted for inflation:

- **In the project**: the member pays in a share and possibly a member loan and pays the
  project rent. Everything saved compared with market rent, plus rent refunds and the
  repaid share and loan, is invested at the alternative return. The share (real) and the
  loan (with compound interest) count as wealth while they are in the project.
- **Market rent + money invested**: share and loan amount are invested at the alternative
  return instead, and the member pays market rent.
- **Share and loan lost** (dashed): like “In the project”, but share and loan are lost,
  e.g. in an insolvency. Subordinated capital carries this risk.

Rent reductions from the surplus (A4) lower the project rent and so raise the saving. The
individual member does not affect the project financing.
""",
    "method.mode3": """
Your own funds (member shares, member loans, direct loans, subsidised loans) are fixed; the
bank loan grows with the house. Land, house and renovation are scaled up or down in
proportion to your cost estimate. Two limits decide how expensive the house may be:

- **Target rent**: the more expensive the house, the larger the bank loan and the higher
  the required rent (mode 1). The search finds the largest investment whose required rent
  does not exceed the target rent, to the nearest €1,000.
- **Bank's equity requirement**: member shares, member loans and direct loans must cover
  at least the minimum share of the investment, so
  investment ≤ (member shares + member loans + direct loans) / minimum share.

The admissible investment is the smaller of the two limits.
""",
    "method.uncertainty": """
You do not know many assumptions exactly today. Here you give a range for the five most
important ones. The calculator draws many variants from them (Latin hypercube sample) and
finds the required rent for each as in mode 1, to 50 cents.

- Within each range the value from the start page is the **most likely**; values towards
  the edges become rarer (triangular distribution).
- The **safe rent** is the rent that is enough in 90 % of the variants.
- All other assumptions come unchanged from the start page.
- The same inputs always give the same result (fixed random seed).
""",
    # Chart reading guides
    "help.annual_costs": """
Each bar shows what the project spends money on in a year; the black line is rent income
after rent loss.

- **Bars above the line**: the project pays the difference from its account that year.
- **Bars below the line**: the account grows.
- All values are **adjusted for inflation** (purchasing power of year 1). A horizontal line
  therefore means: the rent rises exactly with inflation. Bank interest and repayment are
  fixed in nominal terms and so become smaller in real terms year by year.
- The tall bars in single years are **due dates** of direct and member loans. What cannot
  be paid there at once appears as later payment of arrears in the following years.
- From the year in which the **surplus** flows, rent reduction, rent refund or solidarity
  transfer fills the gap up to the line.

Hover over a year to see all amounts.
""",
    "help.debt_balances": """
How much the project still owes at the end of each year, per loan and in total (dashed),
adjusted for inflation.

- **Bank and subsidy** fall steadily through repayment.
- **Direct loans** stay until they fall due (5 or 10 years) and then drop to zero.
  **Member loans** grow through compound interest until they fall due (default 15 years).
- **Arrears** show what still has to be paid after the due date.
""",
    "help.liquidity": """
Account balance at year end compared with the minimum reserve (dashed, default 6 months'
rent), adjusted for inflation.

- The rent is chosen so that the account **never falls below** the reserve. Where the
  lines touch, either a repayment is being deferred (account exactly on the reserve) or it
  is the deciding year.
- Before loans fall due the account saves up; afterwards it drops.
- As soon as no arrears are open and all direct and member loans would be covered, the
  **surplus** is taken out; that is why the account stops growing then.
- Dotted: the **maintenance reserve**, a separate pot that does not count as liquidity.
""",
    "help.arrears": """
- **Bars**: how much of the direct and member loans falling due could not be paid on the
  due date without falling below the minimum reserve.
- **Line**: how much of it is still open at year end. It must be back to zero within the
  deadline; until then the project pays interest on the arrears.

For lenders a bar means: they get their money later than agreed.
""",
    "help.investment_curve": """
How much house (total investment) can be financed at a given target rent per person, in
today's prices.

- The **line** rises because a higher rent can carry a larger bank loan.
- **Dashed**: the upper limit set by the bank's equity requirement; it does not depend on
  the rent.
- What is admissible is always the **lower** of the two lines. The point marks your target
  rent.
""",
    "help.liquidity_mode3": """
Account balance of the house that can just be financed at your target rent, compared with
the minimum reserve (dashed), adjusted for inflation. Where the line touches the reserve,
the house is at the limit of what the target rent can carry.
""",
    "help.member_wealth": """
The member's wealth over time, adjusted for inflation.

- **In the project** above **Market rent + money invested**: the project pays off
  financially. The gap is the advantage.
- At first the comparison is often ahead, because money on the market earns more than the
  share and loan. The rent saving catches up over the years.
- **Dashed**: if the share and loan were lost, e.g. in an insolvency. If this line is also
  above the comparison, the project pays off even then.
""",
    "help.rent_distribution": """
Each bar counts how many variants have a required rent in that range.

- **Dotted**: the rent from mode 1, with the values of the start page.
- **Solid**: the median; half of the variants need less, half need more.
- **Dashed**: the safe rent. Only 10 % of the variants need more.

The wider the distribution, the more the rent depends on assumptions you do not know
today. A gap between the mode 1 rent and the safe rent is a buffer you can plan for.
""",
    "help.headroom_band": """
How much money lies on the account above the minimum reserve if you charge the safe rent,
adjusted for inflation.

- **Line**: median over all variants.
- **Band**: 80 % of the variants lie inside it (between the 10th and 90th percentile).
- The buffer is at most this high in each year until the surplus is taken out; after that
  it is close to zero.

If the lower edge of the band is below zero, some variants fall below the reserve in that
year. Those are the 10 % for which the safe rent is not enough.
""",
    "help.sensitivity": """
How strongly each uncertain assumption is related to the required rent (rank correlation,
−1 to +1).

- **Positive** (blue): if the assumption is higher, the rent rises, e.g. higher renovation
  costs.
- **Negative** (red): if the assumption is higher, the rent falls. For inflation that is
  because the rent grows with inflation while interest and repayment do not.
- The longer the bar, the more it pays to pin down this assumption.
""",
    # Mode 1 KPIs
    "kpi.required_rent.label": "Required rent",
    "kpi.required_rent.help": (
        "Lowest rent per person and month at which the account stays above the minimum "
        "reserve in all 50 years and every arrear is settled within {years} years. It rises "
        "with inflation afterwards."
    ),
    "kpi.per_person_month": "per person and month",
    "kpi.rent_income.label": "Rent income year 1",
    "kpi.rent_income.help": "Rent of all persons in the first year, before rent loss.",
    "kpi.rent_income.note": "per year, all persons",
    "kpi.investment.label": "Total investment",
    "kpi.investment.help": "Land (if bought), house, renovation and purchase costs.",
    "kpi.binding.label": "Deciding year",
    "kpi.binding.help": (
        "The year that fixes the required rent: with slightly less rent, the minimum reserve "
        "would be undercut in this year or arrears would stay open too long. Later burdens "
        "only change the rent once they take over from this year."
    ),
    "kpi.binding.note_reserve": "year {year}, reserve",
    "kpi.binding.note_arrears": "year {year}, arrears open too long",
    "kpi.payoff.label": "Bank and subsidy repaid",
    "kpi.payoff.help": (
        "From the following year the previous debt service is set free and used as chosen "
        "for the surplus."
    ),
    "kpi.surplus_start.label": "Surplus flows from",
    "kpi.surplus_start.help": (
        "From this year no arrears are open and the account covers the reserve plus all open "
        "direct and member loans. The rest goes to rent reduction, rent refund or solidarity "
        "transfer."
    ),
    "kpi.late.label": "Not repaid on time",
    "kpi.late.help": (
        "Part of the direct and member loans falling due that could not be paid on the due "
        "date (nominal). It is paid within {years} years; details in the chart below."
    ),
    "alert.sub_debt_grew": (
        "After {years} years direct and member loans are higher in real terms than at the "
        "start, because interest on member loans accrues faster than it is repaid. This debt "
        "is not reflected in the required rent."
    ),
    # Mode 2 KPIs
    "kpi.project_rent.label": "Project rent",
    "kpi.project_rent.help": "Required rent from mode 1, per person and month in the first year.",
    "kpi.from_mode1": "from mode 1",
    "kpi.saving.label": "Saving compared with market rent",
    "kpi.saving.help": (
        "Market rent minus project rent in the first year after moving in. Later the saving "
        "grows once the surplus lowers the rent."
    ),
    "kpi.saving.note": "per month, first year",
    "kpi.advantage.label": "Advantage",
    "kpi.advantage.help": (
        "Wealth in the project minus wealth with market rent and money invested, at the end, "
        "adjusted for inflation."
    ),
    "kpi.advantage.note": "until {end}",
    "kpi.wealth_project.label": "Wealth in the project",
    "kpi.wealth_project.help": (
        "Invested savings and repayments plus share and loan while they are in the project; "
        "adjusted for inflation."
    ),
    "kpi.wealth_market.label": "Wealth with market rent",
    "kpi.wealth_market.help": (
        "Share and loan amount invested at the alternative return, market rent paid; "
        "adjusted for inflation."
    ),
    "kpi.default.label": "If share and loan are lost",
    "kpi.default.help": (
        "Advantage if the share and loan were lost completely, e.g. in an insolvency of the "
        "project."
    ),
    "kpi.default.note": "advantage over market rent",
    # Mode 3 KPIs
    "kpi.admissible.label": "Admissible investment",
    "kpi.admissible.help": (
        "The smaller of the two limits: what the target rent can carry and what the bank's "
        "equity requirement allows."
    ),
    "kpi.admissible.by_rent": "limited by target rent",
    "kpi.admissible.by_equity": "limited by equity",
    "kpi.share.label": "Share of your cost estimate",
    "kpi.share.help": (
        "Admissible investment divided by your cost estimate (land, house, renovation and "
        "purchase costs from the start page). From 100 % the house can be financed."
    ),
    "kpi.share.note": "estimate {estimate}",
    "kpi.rent_limit.label": "Limit from target rent",
    "kpi.rent_limit.help": (
        "Largest investment whose required rent does not exceed the target rent."
    ),
    "kpi.bank_limit.label": "Limit from equity",
    "kpi.bank_limit.help": (
        "(Member shares + member loans + direct loans) / minimum share required by the bank."
    ),
    "kpi.bank_limit.none": "none",
    # Uncertainty page
    "unc.ranges": "Ranges",
    "unc.compute": "Calculate",
    "unc.hint": "*Most likely value is always taken from the start page.*",
    "unc.prompt": "Set the ranges and click “Calculate”.",
    "unc.stale": "Assumptions have changed. The results below are out of date; please recalculate.",
    "kpi.base.label": "Rent without uncertainty",
    "kpi.base.help": "Required rent from mode 1, with the values of the start page.",
    "kpi.median.label": "Median",
    "kpi.median.help": "Half of the variants need less, half need more.",
    "kpi.spread.label": "Range 10–90 %",
    "kpi.spread.help": "80 % of the variants need a rent in this range.",
    "kpi.safe.label": "Safe rent",
    "kpi.safe.help": (
        "Enough in 90 % of the variants. The gap to the rent without uncertainty is a buffer "
        "for unfavourable developments."
    ),
    "kpi.safe.note": "{amount} above mode 1",
    "kpi.failed.label": "Variants without a solution",
    "kpi.failed.help": (
        "In these variants no rent up to €5,000 per person is enough; they are left out of the "
        "evaluation."
    ),
    # Methodology page
    "methodik.inputs_heading": "## Inputs and defaults",
    "methodik.table_header": "| Section | Input | Default | Meaning |",
    # Charts
    "chart.real_subtitle": "adjusted for inflation, in purchasing power of {year} (year 1)",
    "chart.tranche.equity": "Member shares",
    "chart.tranche.member_loan": "Member loans",
    "chart.tranche.direct_loan": "Direct loans",
    "chart.tranche.subsidy_loan": "Subsidised loan",
    "chart.tranche.bank_loan": "Bank loan",
    "chart.tranche.direct_loans_5y": "Direct loans 5 years",
    "chart.tranche.direct_loans_10y": "Direct loans 10 years",
    "chart.costs.title": "Yearly spending and rent income",
    "chart.costs.y": "per year",
    "chart.costs.operating": "Operations incl. maintenance reserve",
    "chart.costs.senior_interest": "Interest bank and subsidy",
    "chart.costs.senior_repayment": "Repayment bank and subsidy",
    "chart.costs.direct_interest": "Interest direct loans",
    "chart.costs.member_interest": "Interest member loans (on repayment)",
    "chart.costs.sub_repayment": "Repayment direct and member loans (on time)",
    "chart.costs.arrears": "Payment of arrears incl. interest",
    "chart.costs.rebate": "Rent reduction from surplus",
    "chart.costs.payout": "Rent refund",
    "chart.costs.transfer": "Solidarity transfer",
    "chart.costs.rent_income": "Rent income",
    "chart.arrears.title": "Direct and member loans not repaid on time",
    "chart.arrears.new": "Not repaid on the due date",
    "chart.arrears.open": "Open arrears at year end",
    "chart.debt.title": "Outstanding debt at year end",
    "chart.debt.arrears": "Arrears",
    "chart.debt.total": "Total",
    "chart.liquidity.title": "Liquidity and reserve",
    "chart.liquidity.liquidity": "Liquidity",
    "chart.liquidity.reserve": "Minimum reserve",
    "chart.liquidity.maintenance": "Maintenance reserve (separate pot)",
    "chart.member.title": "Member's wealth",
    "chart.member.project": "In the project",
    "chart.member.market": "Market rent + money invested",
    "chart.member.default": "In the project, share and loan lost",
    "chart.curve.title": "Admissible investment by target rent",
    "chart.curve.subtitle": "today's prices",
    "chart.curve.rent_limit": "Limit from target rent",
    "chart.curve.bank_limit": "Limit from equity requirement",
    "chart.curve.point": "Admissible at target rent",
    "chart.curve.x": "Target rent (€ per person/month)",
    "chart.curve.hover_rent": "Target rent",
    "chart.curve.hover_investment": "Investment",
    "chart.uncertain.inflation": "Inflation",
    "chart.uncertain.bank_rate_change_pp": "Bank interest after 10 years",
    "chart.uncertain.vacancy_rate": "Rent loss",
    "chart.uncertain.renovation_factor": "Renovation costs",
    "chart.uncertain.running_cost_factor": "Administration and insurance",
    "chart.dist.title": "Required rent across all variants",
    "chart.dist.count": "Number of variants",
    "chart.dist.base": "Without uncertainty",
    "chart.dist.median": "Median",
    "chart.dist.safe": "Safe rent (enough in 90 %)",
    "chart.dist.x": "Required rent (€ per person/month)",
    "chart.dist.hover_variants": "variants",
    "chart.band.title": "Buffer above the minimum reserve at the safe rent",
    "chart.band.p90": "90th percentile",
    "chart.band.band": "10–90 % band",
    "chart.band.median": "Median",
    "chart.band.reserve": "Minimum reserve",
    "chart.sens.title": "What drives the uncertainty?",
    "chart.sens.y": "Rank correlation with rent",
    "chart.sens.name": "Correlation",
    # Additional uncertain inputs
    "label.member_loan_term_range": "Term member loans (years)",
    "label.member_loan_range": "Member loans (% of plan)",
    "label.direct_loans_10y_range": "Direct loans 10 y. (% of plan)",
    "info.member_loan_term_range": (
        "Range of the member loan term in whole years. Most likely value: start page (under "
        "“Advanced”)."
    ),
    "info.member_loan_range": (
        "How much member loans actually come together, in % of the planned amount. If money "
        "is missing, the bank loan steps in. Most likely value: 100 %."
    ),
    "info.direct_loans_10y_range": (
        "How much 10-year direct loans are actually raised, in % of the planned amount. If "
        "money is missing, the bank loan steps in. Most likely value: 100 %."
    ),
    "chart.uncertain.member_loan_term_years": "Term member loans",
    "chart.uncertain.member_loan_factor": "Amount of member loans",
    "chart.uncertain.direct_loans_10y_factor": "Amount of 10-year direct loans",
    # Rates relative to inflation, member loan payoff, nominal display
    "label.member_loan_spread_pp": "Interest member loans (pp above inflation)",
    "label.direct_loan_spread_5y_pp": "Interest 5 years (pp above inflation)",
    "label.direct_loan_spread_10y_pp": "Interest 10 years (pp above inflation)",
    "label.bank_spread_pp": "Bank interest (pp above inflation)",
    "label.subsidy_spread_pp": "Interest subsidised loans (pp above inflation)",
    "label.alt_return_spread_pp": "Alternative return (pp above inflation)",
    "info.member_loan_spread_pp": (
        "Interest on member loans in percentage points above inflation; it is added to "
        "the loan. Example: 3 at 2 % inflation gives 5 % interest."
    ),
    "info.direct_loan_spread_5y_pp": (
        "Interest on 5-year direct loans in percentage points above inflation, paid "
        "yearly. Negative values mean: interest below inflation."
    ),
    "info.direct_loan_spread_10y_pp": (
        "Interest on 10-year direct loans in percentage points above inflation, paid yearly."
    ),
    "info.bank_spread_pp": (
        "Interest rate of the bank loan for the first 10 years, in percentage points "
        "above inflation. It depends on market rates, not directly on inflation: it was "
        "often 1 to 3 percentage points above, but from 2015 to 2021 close to or below "
        "inflation. The rate is fixed when the loan is taken out and does not follow "
        "inflation afterwards."
    ),
    "info.subsidy_spread_pp": (
        "Interest of the subsidised loans in percentage points above inflation, fixed "
        "over the whole term. Subsidised rates are often below inflation (negative "
        "value)."
    ),
    "info.alt_return_spread_pp": (
        "Return per year in percentage points above inflation if the money were invested "
        "elsewhere instead of in the project (e.g. a broadly diversified fund). All of "
        "the member's savings are invested at the same return."
    ),
    "info.inflation_pct": (
        "Yearly inflation. Rent, running costs and ground rent rise with it. All interest"
        " rates are entered relative to inflation and move with it; once a loan is taken "
        "out, its interest and repayment stay fixed in nominal terms. That is why the "
        "first year is usually the tightest."
    ),
    "summary.rates": (
        "Nominal at {inflation} inflation: bank {bank} (after 10 y. {follow_up}), subsidy"
        " {subsidy}, direct loans {dk5} / {dk10}, member loans {member}"
    ),
    "label.member_loan_payoff": "Repayment of member loans",
    "info.member_loan_payoff": (
        "Where the money comes from when member loans fall due with their interest. From "
        "liquidity: the account pays what it can without falling below the reserve, the "
        "rest is paid later as arrears. New bank loan: the whole amount is financed at "
        "the bank's follow-up rate, as an annuity or linear loan over the remaining term "
        "of the bank loan, at least 10 years. New direct loans: the whole amount is "
        "financed with 10-year direct loans at the 10-year rate, due after 10 years."
    ),
    "option.member_loan_payoff.liquidity": "From liquidity",
    "option.member_loan_payoff.bank": "New bank loan",
    "option.member_loan_payoff.direct_loans": "New direct loans 10 y.",
    "label.display": "Charts",
    "info.display": (
        "Adjusted for inflation: all amounts in purchasing power of year 1, so years can "
        "be compared directly. Nominal: the actual euro amounts of each year; rent and "
        "costs then visibly grow with inflation."
    ),
    "option.display.real": "inflation-adjusted",
    "option.display.nominal": "nominal",
    "chart.nominal_subtitle": "nominal, actual euro amounts of each year",
    "help.nominal_note": (
        "*The chart currently shows nominal amounts; the explanation below refers to the "
        "inflation-adjusted view.*\n"
    ),
    "chart.tranche.bank_refinance": "Bank loan for member loans",
    "chart.tranche.direct_loans_refinance": "Direct loans for member loans",
    "chart.costs.refinancing": "New loan for member loans (inflow)",
}
