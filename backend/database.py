import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "kko_site.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SESSIONLOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

Base = declarative_base()

# Dependency
def get_db():
    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()
