from httpx import AsyncClient
from pytest import mark

from app.auth.repository import AuthRepo
from app.users.models import User


user_data = {"username": "maksu", "password": "password"}


@mark.handlers
async def test_auth_register(client: AsyncClient):
    response = await client.post('/auth/register', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']


@mark.handlers
async def test_auth_login(create_user: User, client: AsyncClient):
    response = await client.post(
        '/auth/login',
        data={
            "grant_type": "password",
            "username": user_data['username'],
            "password": user_data['password']
        }
    )
    assert response.status_code == 200
    assert response.json()['access_token']


@mark.handlers
async def test_auth_update_tokens(
        create_user: User,
        client: AsyncClient,
        auth_repo: AuthRepo
):
    tokens = (await client.post('/auth/login', data={
        "grant_type": "password",
        "username": user_data["username"],
        "password": user_data["password"]
    })).json()

    response = await client.post(
        f'auth/refresh?refresh={tokens['refresh_token']}')
    assert response.status_code == 200
    assert response.json()['access_token']
