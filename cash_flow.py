from dataclasses import dataclass
import logging


@dataclass
class CashFlow:
    """
    Represents income and expenses, generally by a monthly basis


    Attributes:
        paycheck (int): Amount of paycheck which hits checking account.
            Assumed semi-monthly payment schedule
        expenses (int): Spending within the month, excluding any saving
            or investing.
        precheck_contribution (int):
        roth_ira_contribution (int):
        investment_brokerage (int):
        longterm_savings (int): Savings to set aside as cash in a bank account
        shortterm_savings (int): Savings set as cash, but expected to be spent
            after exceeding a goal amount. Vacation, vehicle purchase, etc.

    Methods:
        method1(arg1, arg2):
            Description of method1.
        method2(arg1, arg2):
            Description of method2.
    """

    # income
    paycheck: int

    # expenditure
    expenses: int
    debt_payments: int = 0
    shortterm_savings: int = 0

    # saving + investing
    longterm_savings: int = 0

    precheck_contribution: int = 0
    roth_ira_contribution: int = 0
    investment_brokerage: int = 0

    def get_monthly_paycheck(self, payment_schedule="semimonthly"):
        if payment_schedule != "semimonthly":
            raise NotImplementedError("Only support semimonthly rn")

        return 2 * self.paycheck

    def get_monthly_precheck_contribution(self, payment_schedule="semimonthly") -> int:
        if payment_schedule != "semimonthly":
            raise NotImplementedError("Only support semimonthly rn")

        return 2 * self.precheck_contribution

    def get_monthly_roth_contribution(self, payment_schedule="semimonthly"):
        if payment_schedule != "semimonthly":
            raise NotImplementedError("Only support semimonthly rn")
        return 2 * self.roth_ira_contribution
