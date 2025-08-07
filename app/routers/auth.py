from uuid import uuid4

from config import SESSION_COOKIE_NAME, templates
from database.deps import get_db
from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import RedirectResponse
from models.session import Session as UserSession
from models.user import User
from modules.user import create_user, get_user_by_email, validate_unique_email
from passlib.context import CryptContext
from pydantic import ValidationError
from schemas.auth import RegisterForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", name="auth_register")
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
                context={
                    "request": request,
                    "error": f"ERROR! Email is already in use.",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        form_dict = form.model_dump()
        form_dict["password"] = pwd_context.hash(form_dict["password"])
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

    return RedirectResponse(url="/app/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/login", name="auth_login")
def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    # Validate password
    user = get_user_by_email(db, email)

    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse(
            name="auth/login.html",
            context={
                "request": request,
                "error": f"ERROR! Incorrect e-mail or password.",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Creating the new session
    session_id = str(uuid4())
    client_host = request.client.host
    user_agent = request.headers.get("user-agent")

    new_session = UserSession(
        id=session_id,
        user_id=user.id,
        ip_address=client_host,
        user_agent=user_agent,
    )
    db.add(new_session)
    db.commit()

    # Redirecting to the homepage
    redirect = RedirectResponse("/app/", status_code=status.HTTP_303_SEE_OTHER)
    redirect.set_cookie(
        key=SESSION_COOKIE_NAME, value=session_id, httponly=True, max_age=3600
    )
    return redirect
