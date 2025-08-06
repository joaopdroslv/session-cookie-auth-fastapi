from typing import Optional

from database.deps import get_db
from fastapi import Cookie, Depends, HTTPException
from models.session import Session as UserSession
from models.user import User
from modules.user import get_user_by_id
from sqlalchemy.orm import Session


def get_session_by_id(db: Session, id: str) -> Optional[UserSession]:
    return db.query(UserSession).filter(UserSession.id == id).first()


def get_session_owner(
    session_id: str = Cookie(default=None), db: Session = Depends(get_db)
) -> User:

    # At this point, the session has already been validated in the middleware,
    # just retrieve the owner

    db_session = get_session_by_id(db, session_id)
    db_user = get_user_by_id(db, db_session.user_id)

    if not db_user:

        # TODO: Think about this later...
        raise HTTPException(status_code=401, detail="Session owner not found.")

    return db_user
