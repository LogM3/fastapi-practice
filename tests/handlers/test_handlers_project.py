from httpx import AsyncClient
from pytest import mark

from app.project.models import Project
from app.project.repository import ProjectRepo
from app.project.schemas import SProjectCreate, SProjectUpdate


@mark.handlers
async def test_project_get(
    get_auth: dict[str, str],
    client: AsyncClient,
    create_projects: list[Project]
):
    response = await client.get(
        f'projects/{create_projects[1].id}', headers=get_auth)
    assert response.status_code == 200
    assert response.json()['name'] == create_projects[1].name


@mark.handlers
async def test_project_get_all(
    get_auth: dict[str, str],
    client: AsyncClient,
    create_projects: list[Project]
):
    response = await client.get(
        'projects/?page=2&per_page=2&sort_by=id&sort_order=desc',
        headers=get_auth
    )
    assert response.status_code == 200
    assert len(response.json()['items']) == 1


@mark.handlers
async def test_project_create(
    get_auth: dict[str, str],
    client: AsyncClient
):
    response = await client.post(
        'projects/',
        json=SProjectCreate(name='pr1').model_dump(),
        headers=get_auth
    )
    assert response.status_code == 201
    assert response.json()['name'] == 'pr1'


@mark.handlers
async def test_project_create_bulk(
    get_auth: dict[str, str],
    client: AsyncClient
):
    data = [
        SProjectCreate(name='pr1').model_dump(),
        SProjectCreate(name='pr2').model_dump(),
        SProjectCreate(name='pr1').model_dump()
    ]

    response = await client.post('/projects/bulk', json=data, headers=get_auth)
    assert response.status_code == 200
    assert len(response.json()) == 2


@mark.handlers
async def test_project_update(
    get_auth: dict[str, str],
    client: AsyncClient,
    create_projects: list[Project]
):
    data = SProjectUpdate(name='changed', description='changed').model_dump()
    response = await client.put(
        f'projects/{create_projects[0].id}',
        json=data,
        headers=get_auth
    )
    assert response.status_code == 200
    assert response.json()['description'] == 'changed'


@mark.handlers
async def test_project_delete(
    get_auth: dict[str, str],
    client: AsyncClient,
    create_projects: list[Project],
    project_repo: ProjectRepo
):
    assert await project_repo.get_by_id(create_projects[0].id)
    response = await client.delete(
        f'projects/{create_projects[0].id}',
        headers=get_auth
    )
    assert response.status_code == 200
    assert not await project_repo.get_by_id(create_projects[0].id)
