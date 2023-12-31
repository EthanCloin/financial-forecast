from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import RecoveryPlanRequest, RecoveryPlanResponse, RegisterUserRequest
from crud import CRUD
from config import Settings
import security
import logging


settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()
_log = logging.getLogger(__name__)


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("shared/_base.html", {"request": request})


@router.post("/register")
async def register(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = security.encrypt_password(form_data.get("password"))

    # check if username already exists in db
    _log.debug("beginning register user: %s", request)
    users = CRUD().with_table("users")
    user = users.lookup_user(username)
    if user:
        # redirect payload to login route
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    # else add to users table and create session
    users.insert_user(username, password)
    sessions = CRUD().with_table("sessions")
    session_id = sessions.create_session(user["id"])
    return RedirectResponse(
        "/",
        status_code=status.HTTP_302_FOUND,
        headers={"Set-Cookie": f"session:{session_id}"},
    )


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    users = CRUD().with_table("users")
    user = users.lookup_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="username does not exist"
        )
    if not security.verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="password is not correct"
        )

    sessions = CRUD().with_table("sessions")
    session_id = sessions.create_session(user["id"])
    return RedirectResponse(
        "/",
        status_code=status.HTTP_302_FOUND,
        headers={"Set-Cookie": f"session:{session_id}"},
    )


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


@router.get("/ethantest")
async def ethan_test(request: Request):
    """just trying to get stuff out the tinydb"""
    db = CRUD().with_table("users")
    ethan = db.get_ethan_user()
    print(ethan)

    def format_dollar_amount(cents: int) -> str:
        return "${dollar_amount:.2f}".format(dollar_amount=round(cents / 100, 2))

    return templates.TemplateResponse(
        "user-data.html",
        {
            "request": request,
            "username": ethan["id"],
            "accounts": ethan["balances"],
            "format_dollar_amount": format_dollar_amount,
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
