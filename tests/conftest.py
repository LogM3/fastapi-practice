from httpx import ASGITransport, AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine)

from app.main import app
from app.core.dependencies import get_db_connection
from app.auth.connector import UserConnector
from app.auth.repository import AuthRepo
from app.auth.service import AuthService
from app.core.database import Base
from app.project.repository import ProjectRepo
from app.project.schemas import SProjectCreate
from app.project.service import ProjectService
from app.settings import settings
from app.users.models import User
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


@fixture
async def override_db(async_session: AsyncSession):
    async def _get_db_session():
        yield async_session
    app.dependency_overrides[get_db_connection] = _get_db_session
    yield
    app.dependency_overrides.pop(get_db_connection, None)


@fixture
async def client(override_db: None):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client


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
        'hashed_password': await PasswordService.get_pwd_hash('password'),
        'is_staff': True
    })


@fixture()
async def get_auth(create_user: User, client: AsyncClient):
    data = {
        "grant_type": "password",
        "username": 'maksu',
        "password": 'password'
    }
    response = await client.post('/auth/login', data=data)
    return {'Authorization': f'Bearer {response.json()['access_token']}'}


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
