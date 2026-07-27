# Financial-advice-using-python

# Financial Plan Maker

#### Description:

Financial Plan Maker is a Python-based personal financial planning
application built as my final project for Harvard's CS50P. The goal of
the project is to take a small amount of information about a person's
or household's monthly income and essential expenses, and turn it into
a clear, structured, rule-based financial plann how much to save, how
much to invest, how much to put toward upskilling, how much is
reasonable to spend on wants, and whether taking on a new loan makes
sense right now. The entire program is written in pure Python using
only the standard library, with `pytest` used for automated testing.
No AI, machine learning, or external financial APIs are used anywhere
in the project; every recommendation comes from a small set of
transparent, explainable rules, which felt important for something
as personal as money.

## How the program works

When you run `project.py`, the program first asks whether you are
single. If you are, it asks for your monthly income directly. If you
are part of a household with multiple earners, it asks how many
household members earn an income and then asks for each person's
monthly income in turn, summing them into a single total household
income figure. This two-path design (single vs. household) reflects
the fact that budgeting looks different depending on how many people
are contributing to  and depending on  the same pool of money.

Next, the program walks through a fixed list of **essential expense**
categories: rent, food/groceries, utilities, necessary transportation,
existing EMIs (loan installments), medical/insurance costs, and other
necessary expenses. These are summed into a single "Total Essential
Expenses" figure. Only essential, non-negotiable costs are counted
here this is deliberate, because the whole point of the plan is to
see how much of your income is already "spoken for" before any
saving, investing, or discretionary spending happens.

## The 50% needs rule

The core financial logic is a single, simple rule: what percentage of
income do essential expenses consume?

 -**Condition A - Needs >= 50% of income.** When essentials eat up half
  or more of the household's income, the program treats this as a
  tight financial situation. It recommends that at least 75% of
  whatever money is left over each month be directed toward savings
  and investment rather than discretionary wants, since there is
  little slack to work with. In this condition the plan also leans
  more heavily on upskilling, on the reasoning that when expenses are
  already high relative to income, growing one's earning potential
  can matter more than incremental savings. Loans are generally
  discouraged in this state.
- **Condition B - Needs < 50% of income.** When essential expenses take
  up less than half of income, there is more breathing room. The
  program recommends saving/investing at least 30% of total income,
  with whatever remains after essentials and savings available for
  wants.

In both conditions, the amount earmarked for "savings and investment"
is then split further using an approximate **50/30/20** rule:
50% toward upskilling (courses, certifications, skill development),
30% toward savings, and 20% toward investments such as stocks, bonds,
or debentures. Upskilling is placed first because increasing earning
capacity compounds over time in a way that a single month's savings
contribution does not.

## Loan assessment

The loan assessment is a second, independent rule-based check. It
looks at how much of income is consumed by essential expenses, how
large existing EMI obligations already are relative to income, and
how much savings capacity remains. If essential expenses already
consume 50%+ of income, if existing EMIs exceed 40% of income, or if
savings capacity falls below 10% of income, the program marks a new
loan as **NOT RECOMMENDED** and explains why. Otherwise, it reports
that a loan **CAN BE CONSIDERED**, while making clear this is only a
planning estimate, not professional financial or lending advice.

## Project files

- **`project.py`** contains the entire application. `main()` handles
  the interactive flow (asking questions, calling the calculation
  functions, and printing the final report). Four other top-level
  functions do the actual math and are intentionally kept free of any
  `input()`/`print()` calls so they can be tested in isolation:
  `calculate_needs_percentage()`, `calculate_budget()`,
  `calculate_allocation()`, and `assess_loan()`. Input collection is
  handled by small helper functions (`get_positive_float`,
  `get_yes_no`, `get_income`, `get_expenses`) that validate everything
  the user types, re-prompting on invalid or negative numbers instead
  of crashing.
- **`test_project.py`** contains 20 `pytest` tests covering the four
  core calculation functions: normal cases, the exact 50% boundary,
  zero expenses, invalid/negative inputs, low vs. high EMI load, and
  low vs. high savings capacity for the loan assessment.
- **`requirements.txt`** lists the one external dependency needed for
  development and testing (`pytest`). The application itself only
  relies on the Python standard library, keeping it lightweight and
  easy to run anywhere.

## Design decisions

I deliberately kept all financial calculations as pure functions that
take numbers in and return numbers/dicts out, with no side effects.
This was mainly done for testability - CS50P asks for meaningful
`pytest` coverage, and that's much easier when a function's behavior
depends only on its arguments. It also made the rule logic much
easier to reason about and adjust while building the project, since
each rule lives in exactly one function.

## Limitations and disclaimer

This project is intentionally simple and rule-based. It does not
account for taxes, inflation, irregular income, emergency funds,
regional cost-of-living differences, or long-term financial goals
like retirement. The percentages used (50%, 75%, 30%, 50/30/20, 40%,
10%) are reasonable general-purpose defaults, not personalized advice.
Financial Plan Maker is a learning project and a planning estimate
only - it is not, and should not be treated as, professional
financial or lending advice.

