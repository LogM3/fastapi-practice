from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_connection
from app.project.repository import ProjectRepo
from app.project.service import ProjectService


async def get_project_repo(
    db: Annotated[AsyncSession, Depends(get_db_connection)]
) -> ProjectRepo:
    return ProjectRepo(db)


async def get_project_service(
        repo: Annotated[ProjectRepo, Depends(get_project_repo)]
) -> ProjectService:
    return ProjectService(repo)
