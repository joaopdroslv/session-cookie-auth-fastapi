from config import templates
from fastapi import status


def go_to_401_error_page(request):
    return templates.TemplateResponse(
        "errors/401.html",
        {"request": request},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
