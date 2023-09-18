"""
script form of financial forecaster.
to force simplicity, do not utilize any OOP
"""


def main():
    GOAL_DOLLARS = 100000
    net_worth = get_net_worth()
    income = get_income()
    spending = get_spending(net_worth["debts"], income["net_monthly"])
    action_plan = build_action_plan(income, spending, net_worth)

    months = 0
    while net_worth["total_dollars"] < GOAL_DOLLARS:
        new_net_worth = execute_action_plan(net_worth, action_plan)
        net_worth = new_net_worth
        months += 1

    pass


def get_net_worth():
    # Banking
    # Retirement
    # Investment
    # Debt
    pass


def get_income():
    # Gross Annual
    # Retirement Contribution
    # Net Monthly
    pass


def get_spending(debts, net_monthly_income):
    # Minimum Debt Payments
    # Housing
    # Groceries
    # Frivolous Spending (dining, subscriptions, etc)
    # Available for Saving (net monthly - above)
    pass


def build_action_plan(net_monthly_income, monthly_spending, net_worth):
    """
    is there available income ? prioritize : exception
        is there high-interest-debt ? pay to it
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to roth ira :
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to 401k
            is there remaining available income ? return that amt w status
        is there remaining available income ? contribute to brokerage

    action_plan: {
        available_income: int,
        high_interest_debt_payments: int,
        roth_ira_contribution: int,
        401k_contribution: int,
        brokerage_contribution: int,
    }
    """
    pass


def execute_action_plan(net_worth, action_plan):
    """
    returned an updated net worth after applying contributions to decrease
    debts and increase investments
    """
    pass


if __name__ == "__main__":
    print("Hello World!")
    main()
