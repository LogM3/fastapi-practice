from app.core.security import PasswordService
from app.users.models import User
from app.users.schemas import SUserCreate, SUserOut, SUserUpdate
from app.users.service import UserService


async def test_user_get(
    user_service: UserService,
    create_user: User
):
    assert await user_service.get_user_by_id(create_user.id)
    assert await user_service.get_user_by_username(create_user.username)
    assert len(await user_service.get_users()) == 1
    assert await user_service.get_users_by_ids([create_user.id])


async def test_user_create(
    user_service: UserService,
    pwd: PasswordService
):
    user_data = SUserCreate(username='maksu', hashed_password='password')

    assert not await user_service.get_user_by_username(user_data.username)
    assert await user_service.create_user(user_data, pwd)
    assert await user_service.get_user_by_username(user_data.username)
    assert not await user_service.create_user(user_data, pwd)


async def test_user_bulk_create(
    user_service: UserService,
    pwd: PasswordService
):
    users_data = [
        SUserCreate(username='maksu', hashed_password='password'),
        SUserCreate(username='maksu', hashed_password='password'),
        SUserCreate(username='test', hashed_password='password')
    ]

    assert len(await user_service.create_user_bulk(users_data, pwd)) == 2
    assert await user_service.get_user_by_username('test')
    assert await user_service.get_user_by_username('maksu')


async def test_user_update(
    user_service: UserService,
    pwd: PasswordService,
    create_user: User
):
    user_data = SUserUpdate(username='changed')
    assert await user_service.update_user(
        SUserOut.model_validate(create_user),
        user_data,
        pwd
    )
    assert not await user_service.get_user_by_username(create_user.username)
    assert await user_service.get_user_by_username(user_data.username)


async def test_user_delete(
    user_service: UserService,
    create_user: User
):
    assert await user_service.get_user_by_id(create_user.id)
    assert await user_service.delete_user(create_user.id)
    assert not await user_service.get_user_by_id(create_user.id)
