from dataclasses import dataclass
import logging


@dataclass
class NetWorth:
    cash: dict[str, int]
    retirement: dict[str, int]
    brokerage: int
    crypto: int
    debt: dict[str, int]

    def __post_init__(self):
        # simplify debt calc by consolidating into total
        if self.debt.get("total", None) is None:
            total_debt = sum(self.debt.values())
            logging.debug(f"total debt: {total_debt}")
            self.debt.update({"total": total_debt})

    def shallow_clone(self):
        return NetWorth(
            cash=self.cash,
            retirement=self.retirement,
            brokerage=self.brokerage,
            crypto=self.crypto,
            debt=self.debt,
        )

    def get_total(self) -> int:
        """sum assets and subtract liabilities"""
        asset_type = [self.cash, self.retirement, self.brokerage, self.crypto]
        assets = sum(
            (sum(a.values()) if isinstance(a, dict) else a for a in asset_type)
        )
        liabilities = self.debt.get("total")

        return assets - liabilities

    def accrue_savings_interest(self, APY=4.50):
        """apply 1 month of APY to cash.savings"""
        savings = self.cash["savings"]
        APY = APY / 100  # convert from percentage
        interest_earned = round((APY / 12) * savings)
        self.cash["savings"] = savings + interest_earned
        logging.info(
            "accrued $%d interest on savings. updated savings to $%d",
            interest_earned,
            self.cash["savings"],
        )

    def grow_investments(self, annual_rate=8.00):
        """apply 1 month of annual growth factor to retirement and brokerage"""
        annual_rate = annual_rate / 100  # convert from percentage
        for account, value in self.retirement.items():
            growth = round((annual_rate / 12) * value)
            new_value = value + growth
            self.retirement[account] = new_value
            logging.info(
                "investment in %s grew by $%d. updated value to $%d",
                account,
                growth,
                new_value,
            )

        brokerage_growth = round((annual_rate / 12) * self.brokerage)
        new_brokerage_value = self.brokerage + brokerage_growth
        logging.info(
            "investment in brokerage grew by $%d. updated value to %d",
            brokerage_growth,
            new_brokerage_value,
        )

    def submit_debt_payment_to_total(self, total_payment, APR=6.0) -> None:
        # TODO: utilize numpy-financial to perform proper calculations of
        #   interest, monthly payments, etc.

        APR = APR / 100  # convert from percentage

        total_debt = self.debt.get("total")
        logging.debug(
            f"applied payments of ${total_payment} to existing debt of ${total_debt}"
        )
        total_debt -= total_payment

        monthly_interest = round((APR / 12) * total_debt)
        total_debt += monthly_interest
        logging.debug(
            f"applied ${monthly_interest} of interest. new total=${total_debt}"
        )

        self.debt.update({"total": total_debt})

    def deposit_to_brokerage(self, amount):
        """increase brokerage by given amount"""
        self.brokerage += amount
        logging.debug(
            f"deposited ${amount} in brokerage. new balance: ${self.brokerage}"
        )

    def deposit_to_savings(self, amount):
        """increase cash.savings by given amount"""
        self.cash["savings"] += amount
        logging.debug(
            f"deposited ${amount} in savings. new balance: ${self.cash['savings']}"
        )

    def deposit_to_checking(self, amount):
        """increase cash.checking by given amount"""
        self.cash["checking"] += amount
        logging.debug(
            f"deposited ${amount} in checking. new balance: ${self.cash['checking']}"
        )

    def contribute_to_401k(self, amount):
        """increase retirement['401k'] by given amount"""
        self.retirement["401k"] += amount
        logging.debug(
            f"deposited ${amount} in 401k. new balance: ${self.retirement['401k']}"
        )

    def contribute_to_roth_ira(self, amount):
        """increase retirement['Roth IRA'] by given amount"""
        self.retirement["Roth IRA"] += amount
        logging.debug(
            f"deposited ${amount} in Roth IRA. new balance: ${self.retirement['Roth IRA']}"
        )
