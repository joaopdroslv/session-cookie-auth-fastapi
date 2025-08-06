from datetime import datetime

from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)  # uuid
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    last_seen = Column(DateTime)
    expired = Column(Boolean, default=False)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
