from config import FRONTEND_PREFIX, templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from models.user import User
from modules.session import get_session_owner

router = APIRouter(prefix=FRONTEND_PREFIX, tags=["home"])


@router.get("/register", response_class=HTMLResponse, name="register")
def register(request: Request):

    return templates.TemplateResponse(
        name="auth/register.html", context={"request": request}, status_code=200
    )


@router.get("/login", response_class=HTMLResponse, name="login")
def login(request: Request):

    return templates.TemplateResponse(
        name="auth/login.html", context={"request": request}, status_code=200
    )


@router.get("/", response_class=HTMLResponse, name="home")
def home(request: Request, current_user: User = Depends(get_session_owner)):

    return templates.TemplateResponse(
        name="home/home.html",
        context={"request": request, "user": current_user.friendly_dict()},
        status_code=200,
    )
