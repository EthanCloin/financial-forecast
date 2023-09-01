import logging
from pprint import pprint
from net_worth import NetWorth
from cash_flow import CashFlow


logging.basicConfig(level=logging.DEBUG)


def main():
    net_worth = initialize_net_worth()
    cash_flow = initialize_monthly_cashflow()

    after_a_month = simulate_month(net_worth=net_worth, cash_flow=cash_flow)
    pprint(after_a_month)


def apply_passive_growth(net_worth: NetWorth, cash_flow: CashFlow) -> NetWorth:
    net_worth.accrue_savings_interest()
    net_worth.grow_investments()
    return net_worth


def contribute_to_retirement(
    net_worth: NetWorth, cash_flow: CashFlow, current_monthly_income: int
) -> tuple[NetWorth, int]:
    ira_retirement = cash_flow.get_monthly_roth_contribution()
    job_retirement = cash_flow.get_monthly_precheck_contribution()
    net_worth.contribute_to_401k(job_retirement)
    net_worth.contribute_to_roth_ira(ira_retirement)

    current_monthly_income -= ira_retirement

    return net_worth, current_monthly_income


def save_spend_invest(
    net_worth: NetWorth, cash_flow: CashFlow, current_month_income: int
) -> tuple[NetWorth, int]:
    net_worth.deposit_to_savings(cash_flow.longterm_savings)
    current_month_income -= cash_flow.longterm_savings

    net_worth.deposit_to_brokerage(cash_flow.investment_brokerage)
    current_month_income -= cash_flow.investment_brokerage

    # TODO: update this to own 'budget' function which applies correct
    #   amount of expenses to decrease debt value.
    current_month_income -= cash_flow.expenses
    current_month_income -= cash_flow.shortterm_savings

    return net_worth, current_month_income


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
    roth_contribution = 250
    monthly_expenses = 3500

    # according to rocketmoney budget, i typically have 650
    # to play with after roth, retirement, and expenses for a paycheck
    investments = 400
    savings = 250  # since emergency fund is filled, this goes to purchases or whateva

    return CashFlow(
        paycheck=paycheck,
        precheck_contribution=retirement_contribution,
        roth_ira_contribution=roth_contribution,
        expenses=monthly_expenses,
        investment_brokerage=investments,
        shortterm_savings=savings,
    )


def simulate_month(net_worth: NetWorth, cash_flow: CashFlow) -> NetWorth:
    """
    return updated net worth object for a typical month

    accrue interest on cash_savings, apply growth to investments, apply payments to debts.
    """
    old_net_worth = net_worth.shallow_clone()
    pprint(old_net_worth)

    # passive growth
    current_monthly_income = cash_flow.get_monthly_paycheck()
    net_worth = apply_passive_growth(net_worth, cash_flow)

    # retirement
    net_worth, current_monthly_income = contribute_to_retirement(
        net_worth, cash_flow, current_monthly_income
    )

    # saving, investing, spending
    net_worth, current_monthly_income = save_spend_invest(
        net_worth, cash_flow, current_monthly_income
    )

    logging.info(
        f"Paycheck remaining after all spending and saving: {current_monthly_income}. Depositing in checking"
    )
    net_worth.deposit_to_checking(current_monthly_income)
    print(f"updated net worth: {net_worth.get_total()}")
    return net_worth


if __name__ == "__main__":
    main()
