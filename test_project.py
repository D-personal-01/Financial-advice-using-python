import pytest

from project import (
    calculate_needs_percentage,
    calculate_budget,
    calculate_allocation,
    assess_loan,
)


# ---------------------------------------------------------------------------
# calculate_needs_percentage
# ---------------------------------------------------------------------------

def test_calculate_needs_percentage_normal():
    assert calculate_needs_percentage(1000, 500) == 50.0
    assert calculate_needs_percentage(2000, 400) == 20.0


def test_calculate_needs_percentage_boundary():
    # Exactly 50% is a valid boundary case.
    assert calculate_needs_percentage(4000, 2000) == 50.0


def test_calculate_needs_percentage_zero_expenses():
    assert calculate_needs_percentage(1000, 0) == 0.0


def test_calculate_needs_percentage_invalid_income():
    with pytest.raises(ValueError):
        calculate_needs_percentage(0, 500)
    with pytest.raises(ValueError):
        calculate_needs_percentage(-1000, 500)


def test_calculate_needs_percentage_invalid_expenses():
    with pytest.raises(ValueError):
        calculate_needs_percentage(1000, -50)


# ---------------------------------------------------------------------------
# calculate_budget
# ---------------------------------------------------------------------------

def test_calculate_budget_condition_below_50():
    # Needs < 50% -> Condition B: save/invest at least 30% of income.
    budget = calculate_budget(income=2000, expenses=600)  # 30% needs
    assert budget["condition"] == "B"
    assert budget["needs_percentage"] == 30.0
    assert budget["remaining_income"] == 1400
    assert budget["recommended_savings"] == pytest.approx(600.0)  # 30% of 2000
    assert budget["recommended_wants"] == pytest.approx(800.0)


def test_calculate_budget_condition_exactly_50():
    # Needs == 50% -> should fall into Condition A (>= 50 rule).
    budget = calculate_budget(income=1000, expenses=500)
    assert budget["condition"] == "A"
    assert budget["needs_percentage"] == 50.0
    assert budget["remaining_income"] == 500
    assert budget["recommended_savings"] == pytest.approx(375.0)  # 75% of 500
    assert budget["recommended_wants"] == pytest.approx(125.0)


def test_calculate_budget_condition_above_50():
    # Needs > 50% -> Condition A: save/invest at least 75% of remaining money.
    budget = calculate_budget(income=1000, expenses=800)
    assert budget["condition"] == "A"
    assert budget["remaining_income"] == 200
    assert budget["recommended_savings"] == pytest.approx(150.0)
    assert budget["recommended_wants"] == pytest.approx(50.0)


def test_calculate_budget_zero_expenses():
    budget = calculate_budget(income=1000, expenses=0)
    assert budget["condition"] == "B"
    assert budget["needs_percentage"] == 0.0
    assert budget["recommended_savings"] == pytest.approx(300.0)


def test_calculate_budget_invalid_income_raises():
    with pytest.raises(ValueError):
        calculate_budget(income=0, expenses=100)


# ---------------------------------------------------------------------------
# calculate_allocation
# ---------------------------------------------------------------------------

def test_calculate_allocation_normal():
    allocation = calculate_allocation(1000)
    assert allocation["upskilling"] == pytest.approx(500.0)
    assert allocation["savings"] == pytest.approx(300.0)
    assert allocation["investments"] == pytest.approx(200.0)


def test_calculate_allocation_sums_to_total():
    amount = 733.0
    allocation = calculate_allocation(amount)
    total = allocation["upskilling"] + allocation["savings"] + allocation["investments"]
    assert total == pytest.approx(amount)


def test_calculate_allocation_zero():
    allocation = calculate_allocation(0)
    assert allocation == {"upskilling": 0.0, "savings": 0.0, "investments": 0.0}


def test_calculate_allocation_negative_raises():
    with pytest.raises(ValueError):
        calculate_allocation(-100)


# ---------------------------------------------------------------------------
# assess_loan
# ---------------------------------------------------------------------------

def test_assess_loan_high_needs_not_recommended():
    status, reason = assess_loan(income=1000, expenses=600, existing_emi=100, savings=150)
    assert status == "NOT RECOMMENDED"
    assert "50%" in reason


def test_assess_loan_high_emi_not_recommended():
    status, reason = assess_loan(income=1000, expenses=400, existing_emi=450, savings=200)
    assert status == "NOT RECOMMENDED"
    assert "EMI" in reason


def test_assess_loan_low_savings_not_recommended():
    status, reason = assess_loan(income=1000, expenses=400, existing_emi=50, savings=50)
    assert status == "NOT RECOMMENDED"
    assert "Savings" in reason


def test_assess_loan_can_be_considered():
    status, reason = assess_loan(income=1000, expenses=300, existing_emi=50, savings=300)
    assert status == "CAN BE CONSIDERED"
    assert isinstance(reason, str) and len(reason) > 0


def test_assess_loan_invalid_income_raises():
    with pytest.raises(ValueError):
        assess_loan(income=0, expenses=300, existing_emi=50, savings=100)


def test_assess_loan_negative_values_raise():
    with pytest.raises(ValueError):
        assess_loan(income=1000, expenses=-100, existing_emi=50, savings=100)
