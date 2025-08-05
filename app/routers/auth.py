from config import templates
from database.deps import get_db
from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from modules.user import create_user, validate_unique_email
from pydantic import ValidationError
from schemas.auth import RegisterForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt

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
        form = RegisterForm(  # Validating form values
            email=email,
            password=password,
            confirm_password=confirm_password,
            name=name,
        )

        if not validate_unique_email(db, form.email):
            return templates.TemplateResponse(
                name="auth/register.html",
                context={"request": request, "error": f"ERROR! Email is already in use."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        form_dict = form.model_dump()
        form_dict["password"] = bcrypt.hash(form_dict["password"])
        del form_dict["confirm_password"]  # This field is useless now

        create_user(db, **form_dict)

    except ValidationError as e:

        # Formatting pydantic's error message, it would be possible to make a more elegant solution
        error_msg = e.errors()[0]["msg"]

        return templates.TemplateResponse(
            name="auth/register.html",
            context={"request": request, "error": f"ERROR! {error_msg}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

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
