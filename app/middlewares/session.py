from datetime import datetime

from config import INACTIVITY_MINUTES, SESSION_COOKIE_NAME, SESSION_LIFESPAN_MINUTES
from database.deps import get_db
from models.session import Session as UserSession
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        print(request)

        session_id = request.cookies.get(SESSION_COOKIE_NAME)

        print(session_id)

        return await call_next(request)
