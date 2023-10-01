import logging
from pprint import pformat


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
