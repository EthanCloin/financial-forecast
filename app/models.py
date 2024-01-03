from pydantic import BaseModel


class RecoveryPlanRequest(BaseModel):
    balances: list[dict]
    net_monthly_income: int
    needs: list[dict]
    debts: list[dict]


class RecoveryPlanResponse(BaseModel):
    balances: list[dict]
    debts: list[dict]
    emergency_fund: int | None
    debt_payments: list[dict] | None
    is_debt_free: bool


class RegisterUserRequest(BaseModel):
    username: str
    password: str
