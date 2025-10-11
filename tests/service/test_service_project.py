from app.project.models import ProjectStatus
from app.project.schemas import SProjectCreate, SProjectOut, SProjectUpdate
from app.project.service import ProjectService


async def test_project_get(
    project_service: ProjectService,
    create_projects: list[SProjectOut]
):
    assert (
        await project_service.get_by_id(create_projects[2].id)
        ).name == create_projects[2].name

    assert len((await project_service.get_all(
        page=2,
        per_page=2,
        person_in_charge=None,
        status=ProjectStatus.NEW,
        sort_by='id',
        sort_order='asc'
        )).items) == 1


async def test_project_create(project_service: ProjectService):
    project = await project_service.create_project(
        SProjectCreate(name='pr1')
    )

    assert project and (
        await project_service.get_by_id(project.id)).name == project.name

    assert len(await project_service.create_project_bulk([
        SProjectCreate(name='pr2'),
        SProjectCreate(name='pr3')
    ])) == 2


async def test_project_update(
    project_service: ProjectService,
    create_projects: list[SProjectOut]
):
    project_update = SProjectUpdate(status=ProjectStatus.IN_PROGRESS)
    await project_service.update(project_update, create_projects[0].id)
    assert (
        await project_service.get_by_id(create_projects[0].id)
    ).status != create_projects[0].status
    assert (
        await project_service.get_by_id(create_projects[0].id)
    ).name == create_projects[0].name


async def test_project_delete(
    project_service: ProjectService,
    create_projects: list[SProjectOut]
):
    assert await project_service.delete(create_projects[0].id)
    assert not await project_service.get_by_id(create_projects[0].id)
