from sqlalchemy.exc import IntegrityError

import pytest

from app.users.models import User
from app.users.repository import UserRepo


async def test_user_empty(user_repo: UserRepo):
    assert await user_repo.get_all() == []


async def test_user_create(user_repo: UserRepo):
    user_data = {
        'username': 'maksu',
        'hashed_password': 'password'
    }
    user: User = await user_repo.create_user(user_data)
    assert user and await user_repo.get_by_username(user_data['username'])
    with pytest.raises(IntegrityError):
        await user_repo.create_user(user_data)


async def test_user_edit(create_user: User, user_repo: UserRepo):
    user_data = {
        'username': 'changed',
        'hashed_password': 'pass_to_hash'
    }

    user: User = await user_repo.update_user(create_user.id, user_data)
    assert user.username == user_data['username']
    assert user.hashed_password != create_user.hashed_password
    assert user.id == (
        await user_repo.get_by_username(user_data['username'])).id


async def test_delete_user(create_user: User, user_repo: UserRepo):
    user: User = await user_repo.delete_user(create_user.id)
    assert not await user_repo.get_by_id(user.id)
