import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, Enum, DateTime
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String, index=True)
    referrer = Column(String, nullable=True)
    user_agent = Column(String)
    visit_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
