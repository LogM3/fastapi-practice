import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.project.models import Project, ProjectStatus
from app.project.repository import ProjectRepo


@pytest.fixture()
async def repo(async_session: AsyncSession):
    yield ProjectRepo(async_session)


@pytest.fixture()
async def create_project(repo: ProjectRepo):
    return await repo.create({
        'name': 'sample_project',
        'status': ProjectStatus.NEW,
        'description': 'description',
        'person_in_charge': None,
        'start_time': None,
        'complete_time': None
    })


@pytest.mark.database
async def test_project_empty(repo: ProjectRepo):
    assert await repo.get_all() == ([], 0)


@pytest.mark.database
async def test_project_create(repo: ProjectRepo):
    data = {
        'name': 'sample_project',
        'status': ProjectStatus.NEW,
        'description': 'description',
        'person_in_charge': None,
        'start_time': None,
        'complete_time': None
    }
    project = await repo.create(data)
    assert (await repo.get_by_id(project.id)).name == data['name']
    assert not await repo.create(data) and (await repo.get_all())[1] == 1


@pytest.mark.database
async def test_project_edit(create_project: Project, repo: ProjectRepo):
    project = await repo.update({
        'name': 'changed_name',
        'description': 'changed_description'
    }, create_project.id)
    assert (project.name == 'changed_name'
            and project.description == 'changed_description')


@pytest.mark.database
async def test_project_delete(create_project: Project, repo: ProjectRepo):
    await repo.delete(create_project.id)
    assert not await repo.get_by_id(create_project.id)
