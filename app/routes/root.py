from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from models import RecoveryPlanRequest, RecoveryPlanResponse
from crud import CRUD
from .dependencies import cookie_scheme, templates
import logging


router = APIRouter()

_log = logging.getLogger(__name__)
_log.setLevel("DEBUG")


@router.get("/")
def index(request: Request):
    return RedirectResponse("/auth/login", status.HTTP_302_FOUND)


@router.get("/me")
async def user_profile(request: Request, session_id: str = Depends(cookie_scheme)):
    # TODO: keep an eye out for weird caching behavior with cookie_scheme
    if not session_id:
        return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

    current_user = CRUD().get_user_from_session(session_id)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "username": current_user.username,
            "password": current_user.password,
            "session_id": session_id,
        },
    )


@router.post(
    "/api/recovery_plan",
    response_model=RecoveryPlanResponse,
    response_class=JSONResponse,
)
async def get_recovery_plan(req: RecoveryPlanRequest):
    # maybe instead of doing it in a response like this, i should make a template
    # and return that? but then when am i calling the python functions?
    # i guess just before i return the page
    from core.debt_recovery import build_recovery_plan, execute_recovery_plan

    recovery_plan = build_recovery_plan(
        req.balances, req.net_monthly_income, req.needs, req.debts
    )
    print(recovery_plan)
    recovery_plan = execute_recovery_plan(recovery_plan, req.balances, req.debts)

    return RecoveryPlanResponse(
        balances=recovery_plan.get("balances"),
        debts=recovery_plan.get("debts"),
        emergency_fund=recovery_plan.get("emergency_fund"),
        debt_payments=recovery_plan.get("debt_payments"),
        is_debt_free=recovery_plan.get("is_debt_free"),
    )
