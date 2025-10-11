from pytest import fixture
from asyncio import sleep

from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schemas import SAuthRegister
from app.auth.service import AuthService
from app.users.repository import UserRepo


user_register = SAuthRegister(username='maksu', password='password')


@fixture
async def register_user(auth_service: AuthService):
    await auth_service.register(user_register)


async def test_auth_register(
    auth_service: AuthService,
    user_repo: UserRepo
):
    assert not await user_repo.get_by_username(user_register.username)
    assert await auth_service.register(user_register)
    assert await user_repo.get_by_username(user_register.username)


async def test_auth_login(
    auth_service: AuthService,
    register_user: None
):
    assert (await auth_service.login(OAuth2PasswordRequestForm(
        grant_type='password',
        username='maksu',
        password='password'
    ))).access_token


async def test_auth_update(
    auth_service: AuthService,
    register_user: None
):
    tokens = await auth_service.login(OAuth2PasswordRequestForm(
        grant_type='password',
        username='maksu',
        password='password'
    ))
    await sleep(1)
    assert (
        await auth_service.update_tokens(tokens.refresh_token)
    ).access_token != tokens.access_token
