from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, db_models, schemas

from .auth import (
    authenticate_user, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from .logger import logger, log_error
from .init_db import init_db

# Инициализируем базу данных при запуске
init_db()

app = FastAPI()

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Промежуточное ПО для логирования всех HTTP запросов и ответов.
    Args:
        request: Входящий HTTP запрос
        call_next: Следующий обработчик в цепочке
    """
    try:
        logger.info("Request: %s %s", request.method, request.url)
        response = await call_next(request)
        logger.info("Response Status: %s", response.status_code)
        return response
    except Exception as e:
        log_error(e, f"Error processing request: {request.method} {request.url}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Обработчик ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log_error(exc, f"Unhandled exception: {request.method} {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Аутентификация пользователя и создание JWT токена.
    Args:
        form_data: Данные формы с username и password
        db: сессия базы данных
    Returns:
        dict: Токен доступа и его тип
    """
    try:
        logger.info("Token request received for username: %s", form_data.username)
        logger.info("Received form data: username=%s", form_data.username)

        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning("Authentication failed for user: %s", form_data.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        logger.info("Token generated successfully for user: %s", user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error("Login error: %s", str(e))
        log_error(e, f"Error during login for user: {form_data.username}")
        raise

@app.post("/api/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Создание нового пользователя (только для администраторов).
    Args:
        user: Данные нового пользователя
        db: Сессия базы данных
        current_user: Текущий пользователь (должен быть админом)
    Returns:
        User: Созданный пользователь
    """
    try:
        if current_user.role != "admin":
            logger.warning("Unauthorized user creation attempt by: %s", current_user.username)
            raise HTTPException(status_code=403, detail="Not enough permissions")

        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            logger.warning("Attempt to create user with existing email: %s", user.email)
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = crud.create_user(db=db, user=user)
        logger.info("New user created: %s by admin: %s", new_user.username, current_user.username)
        return new_user
    except Exception as e:
        log_error(e, f"Error creating user: {user.username}")
        raise

@app.get("/api/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Получение информации о текущем пользователе.
    Args:
        current_user: Текущий аутентифицированный пользователь
    Returns:
        User: Данные текущего пользователя
    """
    try:
        logger.info("User %s accessed their profile", current_user.username)
        return current_user
    except Exception as e:
        log_error(e, f"Error accessing profile for user: {current_user.username}")
        raise

@app.get("/api/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user)
):
    """
    Получение списка всех пользователей (только для администраторов).
    Args:
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей
        db: Сессия базы данных
        current_user: Текущий пользователь (должен быть админом)
    Returns:
        List[User]: Список пользователей
    """
    try:
        if current_user.role != "admin":
            logger.warning("Unauthorized users list access attempt by: %s", current_user.username)
            raise HTTPException(status_code=403, detail="Not enough permissions")

        users = crud.get_users(db, skip=skip, limit=limit)
        logger.info("Users list accessed by admin: %s", current_user.username)
        return users
    except Exception as e:
        log_error(e, f"Error accessing users list by: {current_user.username}")
        raise

# Подключение статических файлов
app.mount("/", StaticFiles(directory="kko_pwa_app/build", html=True), name="static")

@app.get("/api/videos")
async def get_videos():
    """
    Получение списка доступных видео.
    Returns:
        dict: Список видеофайлов
    """
    return {"videos": ["video1.mp4", "video2.mp4"]}
