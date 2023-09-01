from dataclasses import dataclass
import logging


@dataclass
class CashFlow:
    paycheck: int
    retirement_contribution: int
    expenses: int

    def get_monthly_income(self, payment_schedule="semimonthly"):
        if payment_schedule != "semimonthly":
            raise NotImplementedError("Only support semimonthly rn")

        return 2 * (self.paycheck + self.retirement_contribution)
