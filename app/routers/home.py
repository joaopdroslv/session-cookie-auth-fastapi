from config import templates
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from models.user import User
from modules.session import get_session_owner

router = APIRouter(prefix="/app", tags=["home"])


@router.get("/", response_class=HTMLResponse)
def home_page(request: Request, current_user: User = Depends(get_session_owner)):

    return templates.TemplateResponse(
        name="home/home.html",
        context={"request": request, "user": current_user.friendly_dict()},
        status_code=200,
    )
