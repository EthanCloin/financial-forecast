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
class CashFlowMonthly:
    gross_income: int
    net_income: int
    income_taxes: int
    retirement_contribution: int

    @staticmethod
    def from_annual(annual: CashFlowAnnual):
        net_income, taxes, retirement = CashFlowMonthly.get_monthly_paydata(annual)
        return CashFlowMonthly(
            gross_income=round((annual.salary_dollars / 12) * 100, 2),
            net_income=net_income,
            income_taxes=taxes,
            retirement_contribution=retirement,
        )

    @staticmethod
    def get_monthly_paydata(annual: CashFlowAnnual) -> tuple[int, int, int]:
        if annual.payroll_schedule != "semimonthly":
            raise NotImplementedError("only supporting semimonthly schedule rn")

        # TODO: here we would use a lookup for other payroll schedules
        #   or maybe create separate entity for payroll
        checks_per_month = 2

        pretax_paycheck = round((annual.salary_dollars / 12) / 2, 2)
        # TODO: here is where we would fork logic for Roth v Traditional
        taxes_witheld = pretax_paycheck * annual.income_tax_rate
        retirement_contribution = round(annual.company_retirement_contribution / 12, 2)
        net_pay = (
            pretax_paycheck - taxes_witheld - retirement_contribution
        ) * checks_per_month

        net_pay_cents = round(net_pay * 100)
        income_tax_cents = round(taxes_witheld * 100)
        retirement_cents = round(retirement_cents * 100)

        return net_pay_cents, income_tax_cents, retirement_cents
