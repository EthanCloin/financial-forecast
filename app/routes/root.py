from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from models import RecoveryPlanRequest, RecoveryPlanResponse
from crud import CRUD
from .dependencies import cookie_scheme, templates, dollars_to_cents
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


@router.get("/balances")
def balances_page(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse("balances.html", {"request": request})


@router.post("/balances")
async def balances(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # grab values from the form
    form = await request.form()
    checking = dollars_to_cents(form.get("checking"))
    saving = dollars_to_cents(form.get("saving"))
    investments = dollars_to_cents(form.get("investments"))

    user_balances = [
        {"name": "checking", "balance": checking},
        {"name": "saving", "balance": saving},
        {"name": "investments", "balance": investments},
    ]
    # insert to db
    db = CRUD()
    user_id = db.get_user_from_session(session_id).id
    db.update_user_balances(user_id, user_balances)

    # redirect to next page
    return RedirectResponse("/income", status.HTTP_302_FOUND)


@router.get("/income")
def income_page(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse("income.html", {"request": request})


@router.post("/income")
async def income(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # grab values from the form
    form = await request.form()
    income = dollars_to_cents(form.get("income"))

    # insert to db
    db = CRUD()
    user_id = db.get_user_from_session(session_id).id
    db.update_user_income(user_id, income)

    # redirect to next page
    return RedirectResponse("/spending", status.HTTP_302_FOUND)


@router.get("/spending")
def spending_page(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse("spending.html", {"request": request})


@router.post("/spending")
async def spending(request: Request, session_id: str = Depends(cookie_scheme)):
    if not session_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # grab values from the form
    form = await request.form()
    spending = dollars_to_cents(form.get("spending"))
    needs = [{"name": "total", "amount": spending}]

    # insert to db
    db = CRUD()
    user_id = db.get_user_from_session(session_id).id
    db.update_user_needs(user_id, needs)

    # redirect to next page
    # return RedirectResponse("/spending", status.HTTP_302_FOUND)


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
