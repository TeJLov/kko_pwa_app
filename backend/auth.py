from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db
from .logger import logger
from .password_utils import verify_password

# Настройки безопасности
SECRET_KEY = "your-secret-key"  # В продакшене использовать переменные окружения
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str):
    logger.info(f"Starting authentication for user: {username}")
    
    user = crud.get_user(db, username)
    if not user:
        logger.warning(f"User not found in database: {username}")
        return False
    
    logger.info(f"User found: {user.username}, role: {user.role}")
    logger.info(f"Attempting to verify password for user: {username}")
    
    # Добавляем отладку для проверки пароля
    is_valid = verify_password(password, user.hashed_password)
    logger.info(f"Password verification result: {is_valid}")
    logger.info(f"Stored hash: {user.hashed_password}")
    
    if not is_valid:
        logger.warning(f"Invalid password for user: {username}")
        return False
    
    logger.info(f"Authentication successful for user: {username}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc

    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
