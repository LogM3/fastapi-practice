import time

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import TokenUser
from app.auth.repository import AuthRepo


@pytest.fixture()
async def repo(async_session: AsyncSession):
    yield AuthRepo(async_session)


@pytest.fixture()
async def create_token(repo: AuthRepo):
    return await repo.save_refresh_token(
        token='dsfmkldlkfglek',
        sub='maksu',
        expires_at=int(time.time())
    )


async def test_token_user_empty(repo: AuthRepo):
    assert await repo.get_all() == []


async def test_token_user_create(repo: AuthRepo):
    await repo.save_refresh_token(
        token='dsfmkldlkfglek',
        sub='maksu',
        expires_at=int(time.time())
    )
    assert await repo.get_refresh('maksu') and len(await repo.get_all()) == 1


async def test_token_user_delete(create_token: TokenUser, repo: AuthRepo):
    assert await repo.get_refresh(create_token.username)
    await repo.delete_refresh(create_token.token)
    assert not await repo.get_refresh(create_token.username)
