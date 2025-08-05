from config import templates
from database.deps import get_db
from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from modules.user import create_user
from pydantic import ValidationError
from schemas.auth import RegistrationForm
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db),
):

    try:
        form = RegistrationForm(  # Validating all inputed values
            email=email,
            password=password,
            confirm_password=confirm_password,
            name=name,
        )

    except ValidationError as e:
        error_msg = e.errors()[0]["msg"]
        return templates.TemplateResponse(
            name="auth/register.html",
            context={"request": request, "error": f"ERROR! {error_msg}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    form_dict = form.model_dump()
    del form_dict["confirm_password"]  # This field is useless now

    create_user(db, **form_dict)

    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)


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
