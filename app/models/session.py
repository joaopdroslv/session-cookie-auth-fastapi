from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)  # uuid
    user_id = Column(Integer, ForeignKey("users.id"))
