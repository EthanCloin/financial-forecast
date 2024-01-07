import logging
from crud import CRUD
from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse
from .dependencies import cookie_scheme, templates
import security


router = APIRouter(prefix="/auth")
_log = logging.getLogger(__name__)
_log.setLevel("DEBUG")
TWO_DAYS = 3600 * 24 * 2


@router.post("/register")
async def register(request: Request):
    """
    process registration form request
    return updated HTML for invalid username or password
    """
    form_data = await request.form()
    username = form_data.get("username")

    # check if username already exists in db
    _log.debug("beginning register user: %s", request)
    db = CRUD()
    user = db.lookup_user(username)

    if user:
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
    # TODO: implement password min requirements regex
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


@router.post("/logout")
async def logout(request: Request, session_id: str = Depends(cookie_scheme)):
    """drop session cookie and session record, redirect to login"""
    response = RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    CRUD().delete_session(session_id)
    response.delete_cookie("session")
    return response
