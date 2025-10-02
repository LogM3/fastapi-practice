from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import sessionmaker
from app.core.security import PasswordService, pwd_service


async def get_db_connection() -> AsyncGenerator[AsyncSession, Any]:
    async with sessionmaker() as session:
        yield session


async def get_password_service() -> PasswordService:
    return pwd_service
