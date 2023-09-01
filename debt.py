from dataclasses import dataclass
import logging


@dataclass
class Debt:
    title: str
    principal: int
    APR: float

    term: int = 5
    min_monthly_payment: int = 0
    current_balance: int = 0

    def __post_init__(self):
        if self.min_monthly_payment == 0:
            self.min_monthly_payment = self.calculate_monthly_payment()
        if self.current_balance == 0:
            self.current_balance = self.principal

    def calculate_monthly_payment(self):
        """use numpy-financial to calculate monthly payment"""
        pass

    def make_payment(self, additional=0):
        payment = self.min_monthly_payment + additional
        logging.debug(
            f"applying ${payment} payment to current balance of ${self.current_balance}"
        )
        self.current_balance -= payment
        logging.info(f"current balance: {self.current_balance}")

        if self.current_balance < 0:
            logging.warning(f"below zero balance on {self.title}")

    def accrue_interest(self):
        """use numpy-financial to accrue interest and update current balance"""
        pass
