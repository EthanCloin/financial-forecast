from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from models import RecoveryPlanRequest, RecoveryPlanResponse

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("shared/_base.html", {"request": request})


@router.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/net-worth")
def intro_net_worth(request: Request):
    return templates.TemplateResponse("net-worth.html", {"request": request})


@router.get("/net-worth/survey")
async def survey_net_worth(request: Request):
    return templates.TemplateResponse("net-worth-survey.html", {"request": request})


@router.get("/income")
def intro_income(request: Request):
    return templates.TemplateResponse("income.html", {"request": request})


@router.get("/income/survey")
async def survey_income(request: Request):
    return templates.TemplateResponse("income-survey.html", {"request": request})


@router.post(
    "/api/recovery_plan",
    response_model=RecoveryPlanResponse,
    response_class=JSONResponse,
)
async def get_recovery_plan(req: RecoveryPlanRequest):
    from core.debt_recovery import build_recovery_plan, execute_recovery_plan

    recovery_plan = build_recovery_plan(
        req.balances, req.net_monthly_income, req.needs, req.debts
    )
    print(recovery_plan)
    recovery_plan = execute_recovery_plan(recovery_plan, req.balances, req.debts)

    return RecoveryPlanResponse(
        balances=recovery_plan.get("balances"),
        debts=recovery_plan.get("debts"),
        emergency_fund=str(recovery_plan.get("emergency_fund")),
        debt_payments=recovery_plan.get("debt_payments"),
        is_debt_free=recovery_plan.get("is_debt_free"),
    )
