from models.user import User
from sqlalchemy.orm import Session


def validate_unique_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first() is None


def create_user(db: Session, email: str, password: str, name: str) -> User:

    new_user = User(email=email, password=password, name=name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
