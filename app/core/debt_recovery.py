"""
the debt_recovery strategy provides an action plan for the user
prioritizing the paying down of high interest debt. 

no consideration for retirement plan or investments.
"""

"""
action_plan = {
        "high_interest_debt_payments": [], 
        "emergency_fund_contribution": 0,
        "roth_ira_contribution": 0,
        "401k_contribution": {},
        "brokerage_contribution": 0,
    }
"""
def main():
    # what are your checking, saving, and investment account balances?
    # how much money hits your account each month?
    pass

def get_banking_balances():
    """whats in the bank right now?"""
    checking = {"name": "checking", "balance": 200000}
    savings = {"name": "savings", "balance": 800000}
    emergency_fund = {"name": "emergency_fund", "balance": 1000000, "goal": 10000000}
    investments = {"name": "investments", "balance": 100000}

    return [checking, savings, emergency_fund, investments]


def get_income():
    """just tell me how much u make a month"""
    income = {
        "net_monthly": 280000
    }
    return income

# this function may be unchanged between different strategies
def get_debts():
    """what are we paying off?"""
    car_loan = {"name": "car_loan", "balance": 1618428, "monthly_payment": 44956}
    student_loan = {"name": "student_loan", "balance": 753174, "monthly_payment": 6276}

    credit_cards = {
        "name": "credit_cards",
        "balance": 20000,
        "monthly_payment": 2000,
        "is_high_interest": True,
    }

    return [
        car_loan,
        student_loan,
        credit_cards,
    ]

if __name__ == "__main__":
    main()