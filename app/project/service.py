from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from app.project.repository import ProjectRepo
from app.project.schemas import (
    SProjectCreate, SProjectOut, SProjectOutList, SProjectUpdate)


@dataclass
class ProjectService:
    repo: ProjectRepo

    async def get_by_id(self, id: int) -> SProjectOut | None:
        try:
            return SProjectOut.model_validate(await self.repo.get_by_id(id))
        except ValidationError:
            return

    async def get_all(
            self,
            page: int,
            per_page: int,
            person_in_charge: int | None,
            status: str | None,
            sort_by: str,
            sort_order: str
    ) -> SProjectOutList:
        projects, total = await self.repo.get_all(
            page,
            per_page,
            person_in_charge,
            status,
            sort_by,
            sort_order
        )
        return SProjectOutList(
            items=[
                SProjectOut.model_validate(project) for project in projects],
            page=page,
            per_page=per_page,
            has_prev=page > 1,
            has_next=page * per_page < total,
            total_count=total
        )

    async def create_project(
            self,
            project_data: SProjectCreate
    ) -> SProjectOut | None:
        try:
            return SProjectOut.model_validate(
                await self.repo.create(project_data.model_dump()))
        except ValidationError:
            return

    async def create_project_bulk(
            self,
            projects_data: list[SProjectCreate]
    ) -> list[SProjectOut]:
        return [SProjectOut.model_validate(project)
                for project_data in projects_data
                if (project := await self.create_project(project_data))]

    async def update(
        self,
        project_data: SProjectUpdate,
        project_id: int
    ) -> SProjectOut | None:
        data: dict[Any, Any] = {}
        for k, v in project_data.model_dump().items():
            if v:
                data[k] = v
        try:
            return SProjectOut.model_validate(
                await self.repo.update(data, project_id))
        except ValidationError:
            return

    async def delete(
        self,
        project_id: int
    ) -> SProjectOut:
        return SProjectOut.model_validate(await self.repo.delete(project_id))
