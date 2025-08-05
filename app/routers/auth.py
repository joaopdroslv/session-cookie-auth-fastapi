from config import templates
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/auth")


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        name="auth/register.html", context={"request": request}, status_code=200
    )


@router.post("/register")
async def register(
    request: Request,
    response: Response,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):

    print(name)
    print(email)
    print(password)
    print(confirm_password)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        name="auth/login.html", context={"request": request}, status_code=200
    )


@router.post("/login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
):

    print(email)
    print(password)
