"""
script form of financial forecaster.
to force simplicity, do not utilize any OOP
"""
from pprint import pprint, pformat
import logging

logging.basicConfig(level="INFO")


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
    gross_annual = 750000000
    # Retirement Contribution
    contribution_401k = 0.08
    # Net Monthly
    net_monthly = 4800000000

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

    action_plan = {
        "high_interest_debt_payments": [],
        "emergency_fund_contribution": 0,
        "roth_ira_contribution": 0,
        "401k_contribution": 0,
        "brokerage_contribution": 0,
    }

    remaining_monthly_income = spending.get("remaining_monthly_income")
    if remaining_monthly_income <= 0:
        raise Exception("you're broke son")

    # these methods mutate the provided action_plan dict
    # similar pattern to Builder
    add_401k_contribution(action_plan, income)

    # Priority One: Pay to High-Interest Debt
    debts: list[dict] = net_worth.get("debt")
    remaining_monthly_income = add_debt_payments(
        action_plan=action_plan,
        debts=debts,
        remaining_monthly_income=remaining_monthly_income,
    )
    if not remaining_monthly_income:
        return action_plan

    # Priority Two: Save Emergency Fund (3mo)
    emergency_fund = next(
        acct
        for acct in net_worth.get("banking", [])
        if acct.get("name") == "emergency_fund"
    )
    remaining_monthly_income = add_emergency_fund_contribution(
        action_plan, emergency_fund, remaining_monthly_income
    )
    if not remaining_monthly_income:
        return action_plan

    # Priority Three: Roth IRA
    remaining_monthly_income = add_roth_ira_contribution(
        action_plan, remaining_monthly_income
    )
    if not remaining_monthly_income:
        return action_plan

    # Priority Four: Company 401k
    remaining_monthly_income = increase_401k_contribution(
        action_plan, income, remaining_monthly_income
    )
    if not remaining_monthly_income:
        return action_plan

    # Priority Five: Brokerage
    action_plan.update(
        {
            "brokerage_contribution": remaining_monthly_income,
        }
    )

    return action_plan


def add_401k_contribution(action_plan, income) -> None:
    """
    apply whatever 401k contribution was specified upon collection
    of spending data to action_plan.

    doubling contribution to represent 100% employer match
    """
    # super simple 100% match assuming provided value qualifies for max value.
    matched_401k_contribution = income.get("401k_monthly_contribution") * 2
    action_plan.update({"401k_contribution": matched_401k_contribution})


def add_debt_payments(action_plan: dict, debts, remaining_monthly_income: int) -> int:
    """
    directly update action plan with amount of extra payments to high interest debts.

    returns updated amount of remaining_monthly_income
    """
    high_interest_repayments: list[dict] = []
    # filter to only high-interest debts which will not be paid off after applying
    # planned monthly payment.
    for debt in filter(
        lambda d: d.get("is_high_interest")
        and d.get("balance") > d.get("monthly_payment"),
        debts,
    ):
        cur_balance = debt.get("balance") - debt.get("monthly_payment")
        can_payoff_balance = remaining_monthly_income >= cur_balance

        if can_payoff_balance:
            high_interest_repayments.append(
                {
                    "name": debt.get("name"),
                    "payment": cur_balance,
                    "is_final_payment": True,
                }
            )
            remaining_monthly_income -= cur_balance
            logging.info(f"paying off debt: {pformat(debt)}")
        else:
            high_interest_repayments.append(
                {"name": debt.get("name"), "payment": remaining_monthly_income}
            )
            remaining_monthly_income = 0
            logging.info(
                f"remaining savings going to debt: {pformat(high_interest_repayments)}"
            )
            break

    action_plan.update({"high_interest_debt_payments": high_interest_repayments})
    return remaining_monthly_income


def add_emergency_fund_contribution(
    action_plan: dict,
    emergency_fund: dict,
    remaining_monthly_income: int,
) -> int:
    emergency_balance = emergency_fund.get("balance")
    emergency_goal = emergency_fund.get("goal")

    fully_funded = emergency_balance >= emergency_goal
    if fully_funded:
        logging.debug("emergency fund is fully funded")
        return remaining_monthly_income

    goal_remaining = emergency_goal - emergency_balance

    can_fully_fund_emergency = remaining_monthly_income >= goal_remaining
    if can_fully_fund_emergency:
        emergency_fund_contribution = goal_remaining
        remaining_monthly_income -= goal_remaining
        logging.info("fully funding emergency fund")
    else:
        emergency_fund_contribution = remaining_monthly_income
        logging.info(f"contributing final {remaining_monthly_income} to emergency fund")

    action_plan.update({"emergency_fund_contribution": emergency_fund_contribution})
    return remaining_monthly_income


def add_roth_ira_contribution(action_plan: dict, remaining_monthly_income: int):
    # simplify to say we can only contribute $500 / month to roth
    # later consider tracking annual contribution and contribute until max
    ira_contribution_limit = 50000

    can_max_contribution = ira_contribution_limit < remaining_monthly_income
    if can_max_contribution:
        roth_ira_contribution = ira_contribution_limit
        remaining_monthly_income -= ira_contribution_limit
        logging.info("maxing roth ira contribution")
    else:
        roth_ira_contribution = remaining_monthly_income
        logging.info(f"contributing final {remaining_monthly_income} to roth_ira")

    action_plan.update({"roth_ira_contribution": roth_ira_contribution})
    return remaining_monthly_income


def increase_401k_contribution(
    action_plan: dict, income: dict, remaining_monthly_income: int
) -> int:
    # saying we can max contribute 25% gross income to 401k
    # potential bug here if income ever exceeds 0.25
    additional_contribution_percent = 0.25 - income.get("401k_percent_contribution")
    gross_monthly_income = income.get("gross_annual") / 12
    current_401k_contribution = action_plan.get("401k_contribution")
    max_additional_contribution = round(
        additional_contribution_percent * gross_monthly_income
    )

    can_max_401k = remaining_monthly_income >= max_additional_contribution

    if can_max_401k:
        contribution_to_401k = current_401k_contribution + max_additional_contribution
        remaining_monthly_income -= max_additional_contribution
        logging.info("maxing 401k contribution")
    else:
        contribution_to_401k = current_401k_contribution + remaining_monthly_income
        logging.info(f"contributing final {remaining_monthly_income} to 401k")
        remaining_monthly_income = 0

    action_plan.update({"401k_contribution": contribution_to_401k})
    return remaining_monthly_income


def execute_action_plan(net_worth, action_plan):
    """
    returned an updated net worth after applying contributions to decrease
    debts and increase investments
    """
    pass


if __name__ == "__main__":
    main()
