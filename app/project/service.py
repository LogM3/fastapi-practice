from dataclasses import dataclass

from pydantic import ValidationError

from app.project.repository import ProjectRepo
from app.project.schemas import SProjectCreate, SProjectOut, SProjectUpdate


@dataclass
class ProjectService:
    repo: ProjectRepo

    async def get_by_id(self, id: int) -> SProjectOut | None:
        try:
            return SProjectOut.model_validate(await self.repo.get_by_id(id))
        except ValidationError:
            return

    async def get_all(self) -> list[SProjectOut]:
        return [
            SProjectOut.model_validate(project)
            for project in await self.repo.get_all()
        ]

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
        try:
            return SProjectOut.model_validate(
                await self.repo.update(project_data.model_dump(), project_id))
        except ValidationError:
            return

    async def delete(
        self,
        project_id: int
    ) -> SProjectOut:
        return SProjectOut.model_validate(await self.repo.delete(project_id))
