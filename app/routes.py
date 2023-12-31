from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.security import APIKeyCookie
from models import RecoveryPlanRequest, RecoveryPlanResponse
from crud import CRUD
from config import Settings
import security
import logging


settings = Settings()
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)
router = APIRouter()
# using Depends(cookie_scheme) will check the request for a cookie named 'session'
cookie_scheme = APIKeyCookie(name="session")
_log = logging.getLogger(__name__)
TWO_DAYS = 3600 * 24 * 2


@router.get("/")
def index(request: Request):
    # return templates.TemplateResponse("shared/_base.html", {"request": request})
    return RedirectResponse("/login", status.HTTP_302_FOUND)


@router.post("/register")
async def register(request: Request):
    form_data = await request.form()
    username = form_data.get("username")

    # check if username already exists in db
    _log.debug("beginning register user: %s", request)
    db = CRUD()
    # TODO: in addition to this, have an htmx check on the username input field to attempt
    #   lookup and have feedback recommending user to switch to login 'username already exists'
    user = db.lookup_user(username)
    if user:
        # redirect payload to login route
        # would be nice to autofill the login page with provided credentials
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "username": username,
                "status": "username_exists",
                "popup_text": "This username already exists!",
            },
        )
    provided = form_data.get("password")

    # just don't accept empty password for now
    if not provided:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "username": username,
                "status": "bad_password",
                "popup_text": "Must provide a valid password!",
            },
        )

    enc_password = security.encrypt_password(provided)
    user = db.insert_user(username, enc_password)
    session = db.create_session(user.id)
    response = RedirectResponse("/me", status.HTTP_302_FOUND)
    response.set_cookie("session", session.session_id, max_age=TWO_DAYS)

    return response


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request):
    """
    for returning users

    valid credentials redirects to /me
    invalid returns updated login page with message
    """

    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    db = CRUD()
    user = db.lookup_user(username)
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "status": "bad_username",
                "username": username,
                "popup_text": "This username doesn't exist!",
            },
        )
    if not security.verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "status": "bad_password",
                "username": username,
                "popup_text": "Your password is not correct, try again!",
            },
        )

    session = db.create_session(user.id)
    response = RedirectResponse(
        "/me",
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie("session", session.session_id, max_age=TWO_DAYS)
    return response


@router.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/me")
async def user_profile(request: Request, session_id: str = Depends(cookie_scheme)):
    # TODO: determine what the issue is with cookie caching
    #   seems to be grabbing old users tho i'm not exactly following
    #   a typical user flow rn
    if not session_id:
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

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


@router.get("/net-worth")
def intro_net_worth(request: Request):
    return templates.TemplateResponse("net-worth.html", {"request": request})


@router.get("/net-worth/survey")
async def survey_net_worth(request: Request):
    return templates.TemplateResponse("net-worth-survey.html", {"request": request})


@router.get("/income")
def income_page(request: Request):
    return templates.TemplateResponse("income.html", {"request": request})


@router.get("/income/survey")
async def survey_income(request: Request):
    return templates.TemplateResponse("income-survey.html", {"request": request})


# TODO: delete this once i have made real authed pages, keeping for now for reference
# @router.get("/ethantest")
# async def ethan_test(request: Request):
#     """just trying to get stuff out the tinydb"""
#     db = CRUD().with_table("users")
#     ethan = db.get_ethan_user()
#     print(ethan)

#     def format_dollar_amount(cents: int) -> str:
#         return "${dollar_amount:.2f}".format(dollar_amount=round(cents / 100, 2))

#     return templates.TemplateResponse(
#         "user-data.html",
#         {
#             "request": request,
#             "username": ethan["id"],
#             "accounts": ethan["balances"],
#             "format_dollar_amount": format_dollar_amount,
#         },
#     )


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
