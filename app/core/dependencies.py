from app.core.database import Database, db
from app.core.security import PasswordService, pwd_service


async def get_database() -> Database:
    return db


async def get_password_service() -> PasswordService:
    return pwd_service
