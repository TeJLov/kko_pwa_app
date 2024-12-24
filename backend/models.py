from datetime import datetime, timezone
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"

class User(BaseModel):
    username: str
    email: str
    role: UserRole
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    page_url = Column(String, index=True)
    referrer = Column(String, nullable=True)
    user_agent = Column(String)
    visit_time = Column(DateTime, default=datetime.now(timezone.utc))
