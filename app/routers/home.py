from config import templates
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/app", tags=["home"])


@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):

    return templates.TemplateResponse(
        name="home/home.html", context={"request": request}, status_code=200
    )
