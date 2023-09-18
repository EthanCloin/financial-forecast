from dataclasses import dataclass
import numpy_financial as npf
import logging


@dataclass
class Debt:
    """
    currency values are stored as integers in cents.
    no support yet for additional payments, only minimum monthlies
    """

    title: str
    principal: int
    APR: float
    term_years: int

    min_monthly_payment: int = 0
    payments_made: int = 0
    interest_paid: int = 0
    remaining_balance: int = 0

    # threshold introduced to compensate for $0.02 discrepancy in interest calculation
    # over $6500 loan over 10 years. this is a simulator, not going to split hairs here.
    ROUNDING_ERR_THRESH = 100

    def __post_init__(self):
        if self.remaining_balance == 0:
            self.remaining_balance = self.principal
        self.payment_count = self.term_years * 12
        self.monthly_interest_rate = self.APR / 12

        if self.min_monthly_payment == 0:
            self.min_monthly_payment = self.calculate_monthly_payment()

    def calculate_monthly_payment(self) -> int:
        """use numpy-financial to calculate minimum monthly payment in cents"""

        monthly_payment = npf.pmt(
            self.monthly_interest_rate, self.payment_count, -self.principal
        )
        monthly_payment = round(monthly_payment)

        logging.info(
            f"monthly payment for {self.title} calculated at {dollars_str(monthly_payment)}"
        )
        return monthly_payment

    def determine_principal_portion(self, additional=0) -> tuple[int, int]:
        """
        calculate the principal portion of current monthly payment and update balance

        returns total payment and principal_portion in cents like (6202, 4712)
        """

        if additional == 0:
            payment = self.min_monthly_payment
        else:
            raise NotImplementedError("no support yet for additional payments to debts")
            payment = self.min_monthly_payment + additional

        principal_portion = npf.ppmt(
            self.monthly_interest_rate,
            self.payments_made + 1,
            self.payment_count,
            self.principal,
        )

        principal_portion = -round(principal_portion)
        logging.debug(
            f"determined principal paid for payment {self.payments_made + 1} as {dollars_str(principal_portion)}"
        )

        return payment, principal_portion

    def make_min_monthly_payment(self):
        is_last_payment = self.payment_count == self.payments_made + 1
        if is_last_payment:
            self.apply_payment_to_balance()
            self.conclude_loan()
            return
        elif self.remaining_balance == 0:
            raise Exception("This loan is already paid off!")
        else:
            self.apply_payment_to_balance()

    def apply_payment_to_balance(self):
        """apply interest and principal for a minimum monthly payment to loan balance"""

        # get payment and principal for minimum monthly payment
        payment, principal_portion = self.determine_principal_portion()

        # update attributes to reflect changes
        self.remaining_balance -= principal_portion
        self.interest_paid += payment - principal_portion
        self.payments_made += 1

        logging.debug(
            f"{{payment: {payment}, principal: {principal_portion}, interest: {payment - principal_portion}}}"
        )

    def conclude_loan(self):
        if self.remaining_balance >= Debt.ROUNDING_ERR_THRESH:
            logging.error(f"remaining balance over threshold! check your math")
        else:
            logging.debug(f"balance after final payment: {self.remaining_balance}")
            self.remaining_balance = 0


def dollars_str(cents: int) -> str:
    dollars = round(cents / 100, 2)
    return "$" + str(dollars)
