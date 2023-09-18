from net_worth import NetWorth
from cash_flow import CashFlow, CashFlowMonthly
from debt import Debt
from dataclasses import dataclass


@dataclass
class ClientProfile:
    name: str
    net_worth: NetWorth
    cash_flow: CashFlow


JOHN_THE_BUTCHER = ClientProfile(
    "John the Butcher",
    net_worth=NetWorth(
        cash={
            "checking": 240000,
            "saving": 500000,
        },
        retirement={
            "IRA": 2000000,
            "401k": 2500000,
        },
        brokerage=0,
        crypto=0,
        debts=[
            Debt(
                title="Auto Loan",
                principal=3000000,
                APR=0.06,
                term_years=4,
            ),
            Debt(
                title="Mortgage",
                principal=45000000,
                APR=0.04,
                term_years=30,
            ),
        ],
    ),
    cash_flow=CashFlowMonthly,
)
