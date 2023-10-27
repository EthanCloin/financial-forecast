"""
the debt_recovery strategy provides an action plan for the user
prioritizing the paying down of high interest debt. 

no consideration for retirement plan or investments.
"""

"""
action_plan = {
        "high_interest_debt_payments": [], 
        "emergency_fund_contribution": 0,
        "roth_ira_contribution": 0,
        "401k_contribution": {},
        "brokerage_contribution": 0,
    }
"""


def main():
    balances = [{"name": "emergency", "balance": 1000}]
    net_monthly_income = 5000
    needs = [{"name": "total", "amount": 2000}]
    debts = [{"name": "total", "balance": 12000, "min_monthly": 300}]

    recovery_plan = build_recovery_plan(balances, net_monthly_income, needs, debts)

    while True:
        # here i need to apply the plan to get a new set of balances and debts
        paid_to_emergency_fund = recovery_plan.get("emergency_fund")
        if paid_to_emergency_fund:
            # update to emergency_fund is carried into balances array, thx python
            emergency_fund = next(
                acct for acct in balances if acct.get("name") == "emergency"
            )
            emergency_fund.update(
                {"balance": emergency_fund.get("balance") + paid_to_emergency_fund}
            )

        paid_to_debts = recovery_plan.get("debt_payments")
        if paid_to_debts:
            for payment in paid_to_debts:
                debt = next(d for d in debts if d.get("name") == payment.get("name"))
                debt.update({"balance": debt.get("balance") - payment.get("amount")})
                if debt.get("balance") == 0:
                    debt.update({"min_monthly": 0})

        debt_free = sum(d.get("balance") for d in debts) == 0
        if debt_free:
            break

        # at this point the balances and debts are updated, needs and income shouldn't change
        recovery_plan = build_recovery_plan(balances, net_monthly_income, needs, debts)

    paid_to_debts = recovery_plan.get("debt_payments")
    leftovers = (
        net_monthly_income
        - sum(p.get("amount") for p in paid_to_debts)
        - sum(n.get("amount") for n in needs)
    )
    print(f"good work soldier, you paid off your debt with {leftovers} leftover")
    pass


def build_recovery_plan(
    bank_balances, net_monthly_income, needs, debts, strategy="snowball"
):
    recovery_plan = {}
    available_income = (
        net_monthly_income
        - sum(n.get("amount") for n in needs)
        - sum(d.get("min_monthly") for d in debts)
    )

    # emergency fund first
    available_income = fill_emergency_fund(
        available_income, recovery_plan, needs, bank_balances
    )
    if available_income == 0:
        return recovery_plan

    available_income = pay_to_debts(available_income, recovery_plan, debts, strategy)
    if available_income == 0:
        recovery_plan.update({"is_debt_free": False})
    """
    note on the is_debt_free flag:
    expecting to use it in some function making repeated calls to 
    this recovery plan method. when that sees this flag, it should
    cease calling.
    """
    return recovery_plan


def fill_emergency_fund(
    available_income: int, recovery_plan, needs, bank_balances
) -> int:
    target = emergency_fund_recommendation(needs, "recovery")
    balance = next(
        acct.get("balance") for acct in bank_balances if acct.get("name") == "emergency"
    )
    remainder = target - balance

    if remainder > 0:
        # 1. Emergency Fund
        if remainder >= available_income:
            recovery_plan.update({"emergency_fund": available_income})
            return 0
        else:
            available_income -= remainder
            recovery_plan.update({"emergency_fund": remainder})
    return available_income


def pay_to_debts(available_income: int, recovery_plan, debts, strategy) -> int:
    quick_mode = len(debts) == 1
    if quick_mode:
        total_debt = debts[0].get("balance")

        if total_debt >= available_income:
            recovery_plan.update(
                {"debt_payments": [{"name": "total", "amount": available_income}]}
            )
            return 0
        else:
            available_income -= total_debt
            recovery_plan.update(
                {
                    "debt_payments": [{"name": "total", "amount": total_debt}],
                    "is_debt_free": True,
                }
            )
            return available_income
    else:
        raise NotImplementedError("only supporting quick mode rn")


def emergency_fund_recommendation(needs, strategy="recovery"):
    """use strategy to determine target balance for emergency_fund"""
    if strategy == "recovery":
        return sum(n.get("amount") for n in needs)
    if strategy == "growth":
        return sum(n.get("amount") for n in needs) * 3
    if strategy == "risk_averse":
        return sum(n.get("amount") for n in needs) * 6


if __name__ == "__main__":
    main()
