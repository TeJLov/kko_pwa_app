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
