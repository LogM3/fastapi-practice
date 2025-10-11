from pytest import fixture
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine)

from app.auth.connector import UserConnector
from app.auth.repository import AuthRepo
from app.auth.service import AuthService
from app.core.database import Base
from app.project.repository import ProjectRepo
from app.project.schemas import SProjectCreate
from app.project.service import ProjectService
from app.settings import settings
from app.users.repository import UserRepo
from app.users.service import UserService
from app.core.security import PasswordService, pwd_service


# @fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     asyncio.set_event_loop(None)
#     loop.close()


@fixture()
async def async_engine():
    settings.TESTING = True
    engine = create_async_engine(settings.db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@fixture()
async def async_session(async_engine: AsyncEngine):
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@fixture()
async def user_repo(async_session: AsyncSession):
    yield UserRepo(async_session)


@fixture()
async def user_service(user_repo: UserRepo):
    yield UserService(user_repo)


@fixture()
async def create_user(user_repo: UserRepo):
    return await user_repo.create_user({
        'username': 'maksu',
        'hashed_password': 'password'
    })


@fixture
async def pwd():
    yield pwd_service


@fixture
async def user_connector(user_service: UserService):
    yield UserConnector(user_service)


@fixture
async def auth_repo(async_session: AsyncSession):
    yield AuthRepo(async_session)


@fixture
async def auth_service(
    user_connector: UserConnector,
    pwd: PasswordService,
    auth_repo: AuthRepo
):
    return AuthService(user_connector, pwd, auth_repo)


@fixture
async def project_repo(async_session: AsyncSession):
    yield ProjectRepo(async_session)


@fixture
async def project_service(project_repo: ProjectRepo):
    yield ProjectService(project_repo)


@fixture
async def create_projects(project_repo: ProjectRepo):
    yield [
        await project_repo.create(SProjectCreate(name='pr1').model_dump()),
        await project_repo.create(SProjectCreate(name='pr2').model_dump()),
        await project_repo.create(SProjectCreate(name='pr3').model_dump())
    ]
