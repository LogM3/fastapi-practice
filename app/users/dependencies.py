from typing import Annotated

from fastapi import Depends

from app.core.database import Database
from app.core.dependencies import get_database
from app.users.repository import UserRepo
from app.users.service import UserService


async def get_user_repo(db: Annotated[Database, Depends(get_database)]) -> UserRepo:
    return UserRepo(db)


async def get_user_service(
    repo: Annotated[UserRepo, Depends(get_user_repo)]
) -> UserService:
    return UserService(repo)
