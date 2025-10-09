from pytest import fixture
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine)

from app.core.database import Base
from app.settings import settings
from app.users.models import User
from app.auth.models import TokenUser
from app.project.models import Project


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
    async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
