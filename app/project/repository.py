from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.repo import BaseRepo
from app.project.models import Project, ProjectStatus


ALLOWED_SORT_COLUMNS: dict[str, Any] = {
    'create_time': Project.create_time,
    'start_time': Project.start_time,
    'complete_time': Project.complete_time
}


@dataclass
class ProjectRepo(BaseRepo[Project]):
    db: AsyncSession
    model: type[Project] = Project

    async def get_by_id(self, id: int) -> Project | None:
        return await self.db.get(self.model, id)

    async def get_all(
            self,
            page: int,
            per_page: int,
            person_in_charge: int | None,
            status: str | None,
            sort_by: str,
            sort_order: str
    ) -> tuple[Sequence[Project], int]:
        query = select(self.model)
        total_query = select(func.count()).select_from(self.model)

        if person_in_charge:
            condition = self.model.person_in_charge == person_in_charge
            query = query.where(condition)
            total_query = total_query.where(condition)
        if status and status in ProjectStatus:
            condition = self.model.status == status
            query = query.where(condition)
            total_query = total_query.where(condition)

        sort_col = ALLOWED_SORT_COLUMNS.get(sort_by, self.model.id)
        query = (
            query.order_by(asc(sort_col)) if sort_order.lower() == 'asc'
            else query.order_by(desc(sort_col))
        )

        query = query.offset(per_page * (page - 1)).limit(per_page + 1)
        async with self.db as session:
            total = (await session.execute(total_query)).scalar_one()
            result = (await session.execute(query)).scalars().all()
            return (result[:per_page], total)

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
