from datetime import datetime

from database.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)  # uuid
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    last_seen = Column(DateTime, default=datetime.now, nullable=False)
    expired = Column(Boolean, default=False, nullable=False)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
