from typing import Annotated
from fastapi import APIRouter, Depends

from app.auth.dependency import staff_only
from app.project.dependencies import get_project_service
from app.core.exceptions import ProjectNotFoundError, WrongDataError
from app.project.schemas import (
    SProjectCreate, SProjectOut, SProjectOutList, SProjectUpdate)
from app.project.service import ProjectService
from app.users.schemas import SUserOut


router: APIRouter = APIRouter(prefix='/projects', tags=['Projects'])


@router.get('/{project_id}')
async def get_project_by_id(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    project_id: int
) -> SProjectOut:
    result: SProjectOut | None = await service.get_by_id(project_id)
    if not result:
        raise ProjectNotFoundError
    return result


@router.get('/')
async def get_all_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    page: int = 1,
    per_page: int = 5,
    person_in_charge: int | None = None,
    status: str | None = None,
    sort_by: str = 'id',
    sort_order: str = 'desc'

) -> SProjectOutList:
    return await service.get_all(
        page,
        per_page,
        person_in_charge,
        status,
        sort_by,
        sort_order
    )


@router.post('/')
async def create_project(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    project_data: SProjectCreate
) -> SProjectOut:
    result: SProjectOut | None = await service.create_project(project_data)
    if not result:
        raise WrongDataError
    return result


@router.post('/bulk')
async def create_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    projects_data: list[SProjectCreate]
) -> list[SProjectOut]:
    return await service.create_project_bulk(projects_data)


@router.put('/{project_id}')
async def update_project(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    project_data: SProjectUpdate,
    project_id: int
) -> SProjectOut:
    if not await service.get_by_id(project_id):
        raise ProjectNotFoundError

    result: SProjectOut | None = await service.update(project_data, project_id)
    if not result:
        raise WrongDataError
    return result


@router.delete('/{project_id}')
async def delete_project(
    service: Annotated[ProjectService, Depends(get_project_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    project_id: int
) -> SProjectOut:
    if not await service.get_by_id(project_id):
        raise ProjectNotFoundError

    return await service.delete(project_id)
