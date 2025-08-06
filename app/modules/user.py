from typing import Optional

from models.user import User
from sqlalchemy.orm import Session


def validate_unique_email(db: Session, email: str) -> bool:

    return db.query(User).filter(User.email == email).first() is None


def create_user(db: Session, email: str, password: str, name: str) -> User:

    new_user = User(email=email, password=password, name=name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_id(db: Session, id: int) -> Optional[User]:

    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:

    return db.query(User).filter(User.email == email).first()
