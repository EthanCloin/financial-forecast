from net_worth import NetWorth
from cash_flow import CashFlow
import logging


logging.basicConfig(level=logging.INFO)


def main():
    net_worth = initialize_net_worth()
    cash_flow = initialize_monthly_cashflow()

    print(net_worth.get_total())
    print(cash_flow.get_monthly_income())

    for i in range(0, 10):
        old_net_worth = NetWorth(**net_worth)
        net_worth.accrue_savings_interest()
        net_worth.grow_investments()


def initialize_net_worth() -> NetWorth:
    cash = {
        "savings": 9000,
        "checking": 3200,
    }

    retirement = {
        "401k": 2500,
        "Traditional IRA": 1900,
        "Roth IRA": 19100,
    }

    brokerage = 300
    crypto = 1500

    debt = {
        "student": 6500,
        "auto": 14000,
    }

    return NetWorth(
        cash=cash, retirement=retirement, crypto=crypto, brokerage=brokerage, debt=debt
    )


def initialize_monthly_cashflow() -> CashFlow:
    paycheck = 2500
    retirement_contribution = 410
    monthly_expenses = 3500

    return CashFlow(
        paycheck=paycheck,
        retirement_contribution=retirement_contribution,
        expenses=monthly_expenses,
    )


def simulate_month(current_net_worth, debt_payments, cash_savings, investments):
    """
    return updated net worth object for a typical month

    accrue interest on cash_savings, apply growth to investments, apply payments to debts.
    """
    pass


def current_net_worth(cash, investments, debt):
    cash_total = sum(cash.values())
    investment_total = (
        sum(investments["retirement"].values())
        + investments["brokerage"]
        + investments["crypto"]
    )
    debt_total = sum(debt.values())

    return cash_total + investment_total - debt_total


if __name__ == "__main__":
    main()
