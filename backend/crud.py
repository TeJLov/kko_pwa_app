from sqlalchemy.orm import Session
from sqlalchemy import func
from . import db_models, schemas
from .password_utils import get_password_hash
from .logger import logger, log_error
from .models import Visit

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
def log_visit(db: Session, page_url: str, referrer: str, user_agent: str):
    try:
        visit = Visit(page_url=page_url, referrer=referrer, user_agent=user_agent)
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return visit
    except Exception as e:
        log_error(e, "Error log visits")
        raise
'''
def get_visits(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Visit).offset(skip).limit(limit).all()
'''
def get_visit_statistics(db: Session):
    """
    Возвращает агрегированные данные по посещениям.
    """
    try:
        # Получаем общее количество посещений
        total_visits = db.query(func.count(Visit.id)).scalar()

        # Получаем количество уникальных страниц
        unique_pages = db.query(func.count(Visit.page_url.distinct())).scalar()

        # Получаем посещения по датам
        visits_by_date = (
            db.query(func.date(Visit.visit_time), func.count(Visit.id))
            .group_by(func.date(Visit.visit_time))
            .all()
        )

        return {
            "total_visits": total_visits,
            "unique_pages": unique_pages,
            "visits_by_date": [{"date": date, "count": count} for date, count in visits_by_date],
        }
    except Exception as e:
        log_error(e, "Error getting visit statistics")
        raise
