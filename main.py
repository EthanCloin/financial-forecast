"""
script form of financial forecaster.
to force simplicity, do not utilize any OOP
"""
from pprint import pprint


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
    emergency_fund = {"name": "emergency_fund", "balance": 1000000}
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
    match_with_401k = income.get("401k_monthly_contribution") * 2

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

    # Priority Two: Save Emergency Fund (3mo)
    emergency_goal = (
        spending.get("living_expenses") + spending.get("debt_obligations") * 3
    )
    emergency_fund = next(
        (a for a in net_worth.get("banking") if a.get("name") == "emergency_fund"), {}
    )
    emergency_balance = emergency_fund.get("balance")

    if emergency_balance < emergency_goal:
        remaining_to_goal = emergency_goal - emergency_balance
        if remaining_to_goal >= available_savings:
            action_plan.update({"emergency_fund_contribution": available_savings})
            return action_plan
        else:
            action_plan.update({"emergency_fund_contribution": remaining_to_goal})
            available_savings -= remaining_to_goal

    # Priority Three: Roth IRA
    # simplify to say we can only contribute $500 / month to roth
    # later consider tracking annual contribution and contribute until max
    ira_contribution_limit = 50000
    if ira_contribution_limit >= available_savings:
        action_plan.update({"roth_ira_contribution": available_savings})
        return action_plan
    else:
        action_plan.update({"roth_ira_contribution": ira_contribution_limit})
        available_savings -= ira_contribution_limit

    # Priority Four: Company 401k
    # saying we can max contribute 25% gross income to 401k
    additional_contribution_percent_limit = 0.25 - income.get(
        "401k_percent_contribution"
    )
    contribution_limit_401k = round(
        income.get("gross_annual") * additional_contribution_percent_limit
    )
    if contribution_limit_401k >= available_savings:
        action_plan.update(
            {
                "401k_contribution": action_plan.get("401k_contribution")
                + available_savings
            }
        )
        return action_plan
    else:
        action_plan.update(
            {
                "401k_contribution": action_plan.get("401k_contribution")
                + contribution_limit_401k
            }
        )
        available_savings -= contribution_limit_401k

    return action_plan


def execute_action_plan(net_worth, action_plan):
    """
    returned an updated net worth after applying contributions to decrease
    debts and increase investments
    """
    pass


if __name__ == "__main__":
    main()
