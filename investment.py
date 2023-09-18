from dataclasses import dataclass


@dataclass
class Investment:
    """represents a monthly contribution to some investment"""

    amount: int
    expected_annual_yield: float


class Roth401kContribution(Investment):
    employer_match_percent: float
    employer_match_limit: float
    expected_annual_yield: float = 0.10
