from dataclasses import dataclass
from debt import Debt
from investment import Investment, Roth401kContribution
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
    # debt_payments: int = 0
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


@dataclass
class CashFlowAnnual:
    salary_dollars: int
    living_expenses: int
    discretionary_expenses: int

    savings_rate: float = 0.00
    investment_profile: str = "None"

    company_retirement_contribution: float = 0.00
    company_retirement_match: float = 0.0
    income_tax_rate: float = 0.24
    ira_contribution: int = 0
    # TODO: break retirement contribution types and percent into own class

    payroll_schedule: str = "semimonthly"


@dataclass
class MonthlyCashFlow:
    """ """

    net_income_dollars: float

    living_expenses: int

    debts: list[Debt]
    investments: list[Investment]
    # maybe later add a list of expenses / budget object

    # calculated fields
    net_income: int = 0
    discretionary_income: int = 0

    def __post_init__(self):
        self.net_income = round(self.net_income * 100)
        self.discretionary_income = self.get_discretionary_income()

    def get_total_debt_obligation(self) -> int:
        return sum(
            d.calculate_monthly_payment() for d in self.debts if d.remaining_balance > 0
        )

    def get_discretionary_income(self) -> int:
        discretionary_income = (
            self.net_income - self.living_expenses - self.get_total_debt_obligation()
        )

        if discretionary_income < 0:
            raise ValueError("Budget not possible! Spending exceeds income")
        else:
            return discretionary_income
