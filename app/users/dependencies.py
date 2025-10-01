from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_connection
from app.users.repository import UserRepo
from app.users.service import UserService


async def get_user_repo(
        db: Annotated[AsyncSession, Depends(get_db_connection)]) -> UserRepo:
    return UserRepo(db)


async def get_user_service(
    repo: Annotated[UserRepo, Depends(get_user_repo)]
) -> UserService:
    return UserService(repo)
