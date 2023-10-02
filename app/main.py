"""
script form of financial forecaster.
to force simplicity, do not utilize any OOP
"""
from pprint import pprint, pformat
import logging

from action_plan import build_action_plan

logging.basicConfig(level="INFO")


def main():
    net_worth = get_net_worth()
    income = get_income()
    spending = get_spending(net_worth.get("debt"), income.get("net_monthly"))
    action_plan = build_action_plan(income, spending, net_worth)
    pprint(action_plan)


def get_net_worth():
    # Banking
    checking = {"name": "checking", "balance": 200000}
    savings = {"name": "savings", "balance": 800000}
    emergency_fund = {"name": "emergency_fund", "balance": 1000000, "goal": 10000000}
    banking = [checking, savings, emergency_fund]

    # Retirement
    company_401k = 500000
    roth_ira = 1200000
    retirement = {"balance": company_401k + roth_ira}

    # Investment
    investment = {"balance": 200000}

    # Debt
    car_loan = {"name": "car_loan", "balance": 1618428, "monthly_payment": 44956}
    student_loan = {"name": "student_loan", "balance": 753174, "monthly_payment": 6276}

    credit_cards = {
        "name": "credit_cards",
        "balance": 20000,
        "monthly_payment": 2000,
        "is_high_interest": True,
    }

    more_credit_cards = {
        "name": "more_credit_cards",
        "balance": 100000,
        "monthly_payment": 10000,
        "is_high_interest": True,
    }

    # NOTE: Currently combining minimum monthlypayment
    debt = [
        car_loan,
        student_loan,
        credit_cards,
        # more_credit_cards,
    ]

    net_worth = {
        "banking": banking,
        "retirement": retirement,
        "investment": investment,
        "debt": debt,
    }

    logging.info(f"generated net_worth: {pformat(net_worth)}")

    return net_worth


def get_income():
    # Gross Annual
    gross_annual = 7500000
    # Retirement Contribution
    contribution_401k = 0.08
    # Net Monthly
    net_monthly = 480000

    income = {
        "gross_annual": gross_annual,
        "401k_monthly_contribution": round((contribution_401k * gross_annual) / 12),
        "401k_percent_contribution": contribution_401k,
        "net_monthly": net_monthly,
    }
    logging.info(f"generated income: {pformat(income)}")
    return income


def get_spending(debt, net_monthly_income):
    # Minimum Debt Payments
    debt_obligations = sum(d.get("monthly_payment") for d in debt)

    # Housing
    housing = 200000
    # Groceries
    groceries = 40000
    # Frivolous Spending (dining, subscriptions, etc)
    bullshit = 150000
    # Available for Saving (net monthly - above)
    remaining_monthly_income = net_monthly_income - (housing + groceries + bullshit)

    spending_profile = {
        "debt_obligations": debt_obligations,
        "living_expenses": housing + groceries,
        "bullshit": bullshit,
        "remaining_monthly_income": remaining_monthly_income,
    }
    logging.info(f"generated spending profile: {pformat(spending_profile)}")
    return spending_profile


def execute_action_plan(net_worth, action_plan):
    """
    returned an updated net worth after applying contributions to decrease
    debts and increase investments
    """

    pass


def interview_client(skip_for_hardcoded=False):
    """
    do you have a dedicated emergency fund? balance?
    what is the current balance in your checking and savings accounts?
    do you have any investments? IRA? Brokerage?

    do you have any debts (balance? minimum_monthly?) ?
    how much do you need to spend to live each month (non-debt bills, groceries) ?

    -- alternate path here is hourly rate --
    what is your gross annual income?
    what is received as net income each month?
    are you contributing to a company 401k (match?) ?

    which of these best describes your current goal?
    - become debt-free
    - reach a target net worth
    """
    pass


if __name__ == "__main__":
    main()
