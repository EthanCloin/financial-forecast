import pytest
from main import (
    add_401k_contribution,
    add_debt_payments,
    add_emergency_fund_contribution,
    build_action_plan,
    increase_401k_contribution,
)

ZERO_INCOME = {
    "gross_annual": 0,
    "401k_monthly_contribution": 0,  # this should rly be a calculated field
    "401k_percent_contribution": 0.0,
    "net_monthly": 0,
}

ZERO_NET_WORTH = {
    "banking": [
        {"name": "checking", "balance": 0},
        {"name": "savings", "balance": 0},
        {"name": "emergency_fund", "balance": 0},
    ],
    "retirement": {"name": "401k", "balance": 0},
    "investment": {"balance": 0},
    "debt": [],
}

ZERO_SPENDING = {
    "debt_obligations": 0,
    "living_expenses": 0,
    "bullshit": 0,
    "remaining_monthly_income": 1,
}

ZERO_ACTION_PLAN = {
    "available_income": 0,
    "high_interest_debt_payments": [],
    "emergency_fund_contribution": 0,
    "roth_ira_contribution": 0,
    "401k_contribution": 0,
    "brokerage_contribution": 0,
}


def test_action_plan_401k_contribution_from_income_is_doubled():
    contribution = 100
    income = ZERO_INCOME.copy()
    income.update({"401k_monthly_contribution": contribution})

    action_plan = ZERO_ACTION_PLAN.copy()
    action_plan.update({"available_income": 1})

    add_401k_contribution(action_plan, income)
    assert action_plan.get("401k_contribution") == contribution * 2


def test_debt_payment_planned_when_remaining_balance_after_monthly_payment():
    credit_cards = {
        "name": "credit_cards",
        "balance": 200,
        "monthly_payment": 20,
        "is_high_interest": True,
    }

    action_plan = ZERO_ACTION_PLAN.copy()
    add_debt_payments(action_plan, [credit_cards], 180)
    debt_payment = action_plan.get("high_interest_debt_payments")[0]

    assert debt_payment.get("payment") == 180
    assert debt_payment.get("is_final_payment") is True


def test_debt_payment_not_planned_when_no_remaining_balance_after_monthly_payment():
    credit_cards = {
        "name": "credit_cards",
        "balance": 200,
        "monthly_payment": 200,
        "is_high_interest": True,
    }

    action_plan = ZERO_ACTION_PLAN.copy()
    available_income = 180
    updated_income = add_debt_payments(action_plan, [credit_cards], available_income)
    debt_payments = action_plan.get("high_interest_debt_payments")

    assert not debt_payments
    assert updated_income == available_income


def test_emergency_fund_doesnt_overfund_with_extra_income():
    emergency_fund = {
        "balance": 100,
        "goal": 200,
    }
    available_income = 300
    action_plan = ZERO_ACTION_PLAN.copy()

    updated_income = add_emergency_fund_contribution(
        action_plan, emergency_fund, available_income
    )

    assert (available_income - 100) == updated_income
    assert action_plan.get("balance") == action_plan.get("goal")


def test_emergency_fund_doesnt_fund_when_full():
    emergency_fund = {
        "balance": 200,
        "goal": 200,
    }
    available_income = 300
    action_plan = ZERO_ACTION_PLAN.copy()

    updated_income = add_emergency_fund_contribution(
        action_plan, emergency_fund, available_income
    )

    assert available_income == updated_income
    assert action_plan.get("balance") == action_plan.get("goal")


def test_increasing_401k_contribution_maxes_at_25_percent():
    income = {
        "gross_annual": 36000,
        "401k_monthly_contribution": 300,  # this should rly be a calculated field
        "401k_percent_contribution": 0.10,
        "net_monthly": 2500,
    }
    action_plan = ZERO_ACTION_PLAN.copy()

    expected_additional_contribution = 450

    available_income = income.get("net_monthly")
    updated_income = increase_401k_contribution(action_plan, income, available_income)

    assert updated_income == available_income - expected_additional_contribution
    assert action_plan.get("401k_contribution") == expected_additional_contribution


def test_action_plan_fails_on_no_income():
    with pytest.raises(Exception):
        build_action_plan(
            ZERO_INCOME.copy(), ZERO_SPENDING.copy(), ZERO_NET_WORTH.copy()
        )


def test_action_plan_distributes_to_all_priorities():
    income = {
        "gross_annual": 3600000,
        "401k_monthly_contribution": 30000,  # this should rly be a calculated field
        "401k_percent_contribution": 0.10,
        "net_monthly": 250000,
    }

    net_worth = {
        "banking": [
            {"name": "checking", "balance": 100000},
            {"name": "savings", "balance": 0},
            {
                "name": "emergency_fund",
                "balance": 280000,
                "goal": 300000,
            },  # expect 200 contribution
        ],
        "retirement": {"name": "401k", "balance": 0},
        "investment": {"balance": 0},
        "debt": [
            {
                "name": "credit_cards",
                "balance": 20000,
                "monthly_payment": 10000,  # expect 100 additional_payment
                "is_high_interest": True,
            },
            {
                "name": "auto_loan",
                "balance": 200000,
                "monthly_payment": 10000,
                "is_high_interest": False,
            },
        ],
    }

    spending = {
        "debt_obligations": sum(
            d.get("monthly_payment") for d in net_worth.get("debt")
        ),  # 200
        "living_expenses": 90000,  # 900
        "bullshit": 0,
        "remaining_monthly_income": income.get("net_monthly")
        - 110000,  # 1400 available
    }

    action_plan = build_action_plan(income, spending, net_worth)

    expected_action_plan = {
        "high_interest_debt_payments": [
            {
                "name": "credit_cards",
                "payment": 10000,  # 1400 - 100 = 1300
                "is_final_payment": True,
            }
        ],
        "emergency_fund_contribution": 20000,  # 1300 - 200 = 1100
        "roth_ira_contribution": 50000,  # 1100 - 500 = 600
        "401k_contribution": 45000 + (2 * 30000),  # 600 - 450 = 150
        "brokerage_contribution": 15000,  # 150 - 150 = 0
    }

    assert action_plan == expected_action_plan
