from sqlalchemy.orm import Session
from . import db_models, schemas
from .password_utils import get_password_hash
from .logger import logger, log_error

def get_user(db: Session, username: str):
    try:
        return db.query(db_models.User).filter(db_models.User.username == username).first()
    except Exception as e:
        log_error(e, f"Error getting user by username: {username}")
        raise

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(db_models.User).filter(db_models.User.email == email).first()
    except Exception as e:
        log_error(e, f"Error getting user by email: {email}")
        raise

def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(db_models.User).offset(skip).limit(limit).all()
    except Exception as e:
        log_error(e, "Error getting users list")
        raise

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = db_models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Created new user: {user.username}")
        return db_user
    except Exception as e:
        db.rollback()
        log_error(e, f"Error creating user: {user.username}")
        raise
