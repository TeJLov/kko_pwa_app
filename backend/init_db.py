from kko_pwa_app.backend.database import SESSIONLOCAL, ENGINE
from kko_pwa_app.backend import db_models
from kko_pwa_app.backend.schemas import UserCreate
from kko_pwa_app.backend.crud import create_user

def init_db():
    db_models.Base.metadata.create_all(bind=ENGINE)

    db = SESSIONLOCAL()

    # Проверяем, существует ли уже админ
    admin = db.query(db_models.User).filter(db_models.User.username == "admin").first()
    if not admin:
        admin_user = UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role="admin"
        )
        create_user(db, admin_user)
        print("Admin user created successfully")
    
    db.close()

if __name__ == "__main__":
    init_db()
