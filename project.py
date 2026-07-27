"""
Financial Plan Maker
A rule-based personal/household financial planning tool.

CS50P Final Project
"""


def main():
    print("=" * 40)
    print("        FINANCIAL PLAN MAKER")
    print("=" * 40)
    print("This tool gives a rule-based financial planning estimate.")
    print("It is NOT professional financial or lending advice.\n")

    income = get_income()
    expenses = get_expenses()

    budget = calculate_budget(income, expenses)
    allocation = calculate_allocation(budget["recommended_savings"])
    loan_status, loan_reason = assess_loan(
        income, expenses, expenses_breakdown_emi(), budget["recommended_savings"]
    )

    print_report(income, expenses, budget, allocation, loan_status, loan_reason)


# ---------------------------------------------------------------------------
# Input collection (kept separate from calculation logic)
# ---------------------------------------------------------------------------

def get_positive_float(prompt):
    """Repeatedly prompt the user until a valid non-negative float is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value < 0:
            print("Please enter a value that is zero or greater.")
            continue
        return value


def get_yes_no(prompt):
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer Yes or No.")


def get_income():
    """Ask household status and collect total monthly income."""
    single = get_yes_no("Are you single? (Yes/No): ")

    if single:
        income = get_positive_float("Enter your monthly income: ")
    else:
        while True:
            try:
                members = int(input("How many earning members are in the household? ").strip())
                if members <= 0:
                    print("Please enter a number of earning members greater than zero.")
                    continue
                break
            except ValueError:
                print("Please enter a valid whole number.")

        income = 0.0
        for i in range(1, members + 1):
            income += get_positive_float(f"Enter monthly income for earning member {i}: ")

    if income <= 0:
        print("Income must be greater than zero. Please restart the program.")
        raise SystemExit(1)

    return income


# Module-level storage so main() can retrieve the EMI figure for loan
# assessment without changing the signature of calculate_budget().
_last_emi_amount = 0.0


def expenses_breakdown_emi():
    """Return the existing EMI amount captured during expense collection."""
    return _last_emi_amount


def get_expenses():
    """Ask for each essential expense category and return the total."""
    global _last_emi_amount

    print("\nNow enter your monthly ESSENTIAL expenses.")
    rent = get_positive_float("Rent: ")
    food = get_positive_float("Food/Groceries: ")
    utilities = get_positive_float("Utilities: ")
    transport = get_positive_float("Necessary Transportation: ")
    emi = get_positive_float("Existing EMIs: ")
    medical = get_positive_float("Medical/Insurance: ")
    other = get_positive_float("Other Necessary Expenses: ")

    _last_emi_amount = emi

    total = rent + food + utilities + transport + emi + medical + other
    return total


# ---------------------------------------------------------------------------
# Core calculation logic (pure functions, independently testable)
# ---------------------------------------------------------------------------

def calculate_needs_percentage(income, expenses):
    """
    Return essential expenses as a percentage of income.

    Raises ValueError for non-positive income or negative expenses.
    """
    if income <= 0:
        raise ValueError("Income must be greater than zero.")
    if expenses < 0:
        raise ValueError("Expenses cannot be negative.")

    return (expenses / income) * 100


def calculate_budget(income, expenses):
    """
    Determine the user's financial condition and recommended budget split.

    Returns a dict with:
        needs_percentage, remaining_income,
        recommended_savings, recommended_wants, condition
    """
    needs_percentage = calculate_needs_percentage(income, expenses)
    remaining_income = income - expenses

    if needs_percentage >= 50:
        # Condition A: essentials consume 50% or more of income.
        safe_remaining = max(remaining_income, 0)
        recommended_savings = safe_remaining * 0.75
        recommended_wants = safe_remaining - recommended_savings
        condition = "A"
    else:
        # Condition B: essentials consume less than 50% of income.
        recommended_savings = income * 0.30
        recommended_wants = remaining_income - recommended_savings
        if recommended_wants < 0:
            recommended_wants = 0
        condition = "B"

    return {
        "needs_percentage": needs_percentage,
        "remaining_income": remaining_income,
        "recommended_savings": recommended_savings,
        "recommended_wants": recommended_wants,
        "condition": condition,
    }


def calculate_allocation(amount):
    """
    Split a savings/investment pool into upskilling, savings and investments
    using an approximate 50 / 30 / 20 split.

    Raises ValueError for negative amounts.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    return {
        "upskilling": amount * 0.50,
        "savings": amount * 0.30,
        "investments": amount * 0.20,
    }


def assess_loan(income, expenses, existing_emi, savings):
    """
    Provide a basic rule-based assessment of whether taking on a new loan
    is currently advisable.

    Returns a tuple: (status, reason)
    """
    if income <= 0:
        raise ValueError("Income must be greater than zero.")
    if expenses < 0 or existing_emi < 0 or savings < 0:
        raise ValueError("Expenses, EMI and savings cannot be negative.")

    needs_percentage = calculate_needs_percentage(income, expenses)
    emi_percentage = (existing_emi / income) * 100
    savings_ratio = savings / income

    if needs_percentage >= 50:
        return (
            "NOT RECOMMENDED",
            "Essential expenses already consume 50% or more of income, "
            "leaving little room for additional debt.",
        )

    if emi_percentage > 40:
        return (
            "NOT RECOMMENDED",
            "Existing EMI obligations are already high relative to income.",
        )

    if savings_ratio < 0.10:
        return (
            "NOT RECOMMENDED",
            "Savings capacity is too low to safely support a new loan.",
        )

    return (
        "CAN BE CONSIDERED",
        "Essential expenses are moderate, existing EMI load is manageable, "
        "and savings capacity is healthy.",
    )


# ---------------------------------------------------------------------------
# Reporting (UI only, no calculation logic)
# ---------------------------------------------------------------------------

def print_report(income, expenses, budget, allocation, loan_status, loan_reason):
    print("\n================================")
    print("      FINANCIAL PLAN REPORT")
    print("================================")
    print(f"Monthly Income:          {income:.2f}")
    print(f"Essential Expenses:      {expenses:.2f}")
    print(f"Needs Percentage:        {budget['needs_percentage']:.2f}%")
    print(f"Remaining Income:        {budget['remaining_income']:.2f}")
    print()
    print(f"Recommended Savings:     {budget['recommended_savings']:.2f}")
    print(f"Recommended Wants:       {budget['recommended_wants']:.2f}")
    print()
    print("------ MONEY ALLOCATION ------")
    print(f"Upskilling:              {allocation['upskilling']:.2f}")
    print(f"Savings:                 {allocation['savings']:.2f}")
    print(f"Investments:             {allocation['investments']:.2f}")
    print()
    print("------ LOAN ASSESSMENT -------")
    print(f"Loan Status:             {loan_status}")
    print(f"Reason:                  {loan_reason}")
    print("================================")
    print("Note: This is a financial planning estimate only and does")
    print("not constitute professional financial or lending advice.")


if __name__ == "__main__":
    main()
