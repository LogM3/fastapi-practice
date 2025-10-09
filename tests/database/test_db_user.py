from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import pytest

from app.users.models import User
from app.users.repository import UserRepo


@pytest.fixture()
async def repo(async_session: AsyncSession):
    yield UserRepo(async_session)


@pytest.fixture()
async def create_user(repo: UserRepo):
    return await repo.create_user({
        'username': 'maksu',
        'hashed_password': 'password'
    })


async def test_user_empty(repo: UserRepo):
    assert await repo.get_all() == []


async def test_user_create(repo: UserRepo):
    user_data = {
        'username': 'maksu',
        'hashed_password': 'password'
    }
    user: User = await repo.create_user(user_data)
    assert user and await repo.get_by_username(user_data['username'])
    with pytest.raises(IntegrityError):
        await repo.create_user(user_data)


async def test_user_edit(create_user: User, repo: UserRepo):
    user_data = {
        'username': 'changed',
        'hashed_password': 'pass_to_hash'
    }

    user: User = await repo.update_user(create_user.id, user_data)
    assert user.username == user_data['username']
    assert user.hashed_password != create_user.hashed_password
    assert user.id == (await repo.get_by_username(user_data['username'])).id


async def test_delete_user(create_user: User, repo: UserRepo):
    user: User = await repo.delete_user(create_user.id)
    assert not await repo.get_by_id(user.id)
