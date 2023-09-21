"""
script form of financial forecaster.
to force simplicity, do not utilize any OOP
"""
from pprint import pprint
from re import match


def main():
    GOAL_DOLLARS = 100000
    net_worth = get_net_worth()
    income = get_income()
    spending = get_spending(net_worth.get("debt"), income.get("net_monthly"))
    action_plan = build_action_plan(income, spending, net_worth)
    pprint(action_plan)

    # months = 0
    # while net_worth["total_dollars"] < GOAL_DOLLARS:
    #     new_net_worth = execute_action_plan(net_worth, action_plan)
    #     net_worth = new_net_worth
    #     months += 1

    pass


def get_net_worth():
    # Banking
    checking = {"name": "checking", "balance": 200000}
    savings = {"name": "savings", "balance": 800000}
    emergency_fund = {"name": "emergency_fund", "balance": 800000}
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
        more_credit_cards,
    ]

    net_worth = {
        "banking": banking,
        "retirement": retirement,
        "investment": investment,
        "debt": debt,
    }
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
        "monthly_401k_contribution": round((contribution_401k * gross_annual) / 12),
        "net_monthly": net_monthly,
    }
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
    available_savings = net_monthly_income - (housing + groceries + bullshit)

    spending_profile = {
        "debt_obligations": debt_obligations,
        "living_expenses": housing + groceries,
        "bullshit": bullshit,
        "available_savings": available_savings,
    }

    return spending_profile


def build_action_plan(income, spending, net_worth):
    """
    is there available income ? prioritize : exception
        is there high-interest-debt ? pay to it
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to roth ira :
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to 401k
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to brokerage
    """

    # super simple 100% match assuming provided value qualifies for max value.
    match_with_401k = income.get("monthly_401k_contribution") * 2

    action_plan = {
        "available_income": 0,
        "high_interest_debt_payments": [],
        "emergency_fund_contribution": 0,
        "roth_ira_contribution": 0,
        "401k_contribution": match_with_401k,
        "brokerage_contribution": 0,
    }
    my_debts: list[dict] = net_worth.get("debt")
    plan_debt_payments: list[dict] = action_plan.get("high_interest_debt_payments", [])

    available_savings = spending.get("available_savings")
    action_plan.update({"available_income": available_savings})

    if available_savings <= 0:
        raise Exception("you're broke son")

    # Priority One: Pay to High-Interest Debt
    for debt in filter(lambda d: d.get("is_high_interest"), my_debts):
        cur_balance = debt.get("balance")
        if cur_balance >= available_savings:
            plan_debt_payments.append(
                {"name": debt.get("name"), "payment": available_savings}
            )
            return action_plan
        else:
            plan_debt_payments.append(
                {"name": debt.get("name"), "payment": cur_balance}
            )
            available_savings -= cur_balance

    return action_plan


def execute_action_plan(net_worth, action_plan):
    """
    returned an updated net worth after applying contributions to decrease
    debts and increase investments
    """
    pass


if __name__ == "__main__":
    main()
