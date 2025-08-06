import logging
from datetime import datetime

from config import PUBLIC_PATHS, SESSION_COOKIE_NAME, SESSION_TTL, TIME_TO_INACTIVATE
from database.deps import get_db_context
from fastapi import status
from models.session import Session as UserSession
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

logger = logging.getLogger(__name__)


class SessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)

        session_id = request.cookies.get(SESSION_COOKIE_NAME)

        logger.info(f'Has "session_id": {session_id is not None}')
        logger.info(session_id)

        if not session_id:
            logger.info('Missing "session_id", redirecting to login.')
            return RedirectResponse("/auth/login", status_code=status.HTTP_302_FOUND)

        try:
            valid_user_session = None
            db: Session

            with get_db_context() as db:

                valid_user_session: UserSession = (
                    db.query(UserSession)
                    .filter(
                        UserSession.id == session_id, UserSession.expired.is_(False)
                    )
                    .first()
                )

                logger.info(f"Has valid user session: {valid_user_session is not None}")

                if not valid_user_session:
                    logger.info(
                        'Invalid or expired "session_id", redirecting to login.'
                    )
                    return RedirectResponse(
                        "/auth/login", status_code=status.HTTP_302_FOUND
                    )

                now = datetime.now()

                # Validate if the session has expired by the total lifetime or due to inactivity time
                session_lifespan = (
                    now - valid_user_session.created_at
                ).total_seconds() / 60
                inactivity_time = (
                    now - valid_user_session.last_seen
                ).total_seconds() / 60

                if (
                    session_lifespan > SESSION_TTL
                    or inactivity_time > TIME_TO_INACTIVATE
                ):
                    valid_user_session.expired = True
                    valid_user_session.last_seen = now
                    db.commit()

                    logger.info(
                        "Session expired, redirecting user to the login page..."
                    )

                    return RedirectResponse(
                        "/auth/login", status_code=status.HTTP_302_FOUND
                    )

                valid_user_session.last_seen = now
                db.commit()

        except Exception as e:

            logger.error("Something went wrong on the SessionMiddleware.")
            logger.error(e)

        return await call_next(request)
