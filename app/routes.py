from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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
