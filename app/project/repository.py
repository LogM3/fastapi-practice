from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.repo import BaseRepo
from app.project.models import Project


@dataclass
class ProjectRepo(BaseRepo[Project]):
    db: AsyncSession
    model: type[Project] = Project

    async def get_by_id(self, id: int) -> Project | None:
        return await self.db.get(self.model, id)

    async def get_all(self) -> Sequence[Project]:
        async with self.db as session:
            return (await session.execute(select(self.model))).scalars().all()

    async def create(self, data: dict[Any, Any]) -> Project | None:
        async with self.db as session:
            try:
                project = Project(**data)
                session.add(project)
                await session.commit()
                return project
            except IntegrityError:
                return

    async def update(self, data: dict[Any, Any], id: int) -> Project | None:
        async with self.db as session:
            try:
                result = (await session.execute(
                    update(self.model).where(self.model.id == id)
                    .values(**data)
                    .returning(self.model)
                )).scalar_one()
                await session.commit()
                return result
            except IntegrityError:
                return

    async def delete(self, project_id: int) -> Project:
        async with self.db as session:
            result = (await session.execute(
                delete(self.model).where(self.model.id == project_id)
                .returning(self.model)
            )).scalar_one()
            await session.commit()
            return result
