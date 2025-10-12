from httpx import AsyncClient
from pytest import mark

from app.users.models import User


@mark.handlers
async def test_user_get_by_id(create_user: User, client: AsyncClient):
    response = await client.get(f'/users/{create_user.id}')
    assert response.status_code == 200
    assert response.json() == {
        'username': create_user.username,
        'id': create_user.id,
        'is_staff': create_user.is_staff,
        'hashed_password': create_user.hashed_password
    }


@mark.handlers
async def test_user_get_all(create_user: User, client: AsyncClient):
    response = await client.get('/users/')
    assert response.status_code == 200
    assert response.json() == [{
        'username': create_user.username,
        'id': create_user.id,
        'is_staff': create_user.is_staff,
        'hashed_password': create_user.hashed_password
    }]


@mark.handlers
async def test_user_create(client: AsyncClient, get_auth: dict[str, str]):
    user_data = {
        "username": "test",
        "hashed_password": "password",
        "is_staff": "true"
    }
    response = await client.post('/users/', json=user_data, headers=get_auth)
    assert response.status_code == 201
    assert response.json()['username'] == user_data['username']


@mark.handlers
async def test_user_bulk_create(client: AsyncClient, get_auth: dict[str, str]):
    data = [
        {
            "username": "test",
            "hashed_password": "password",
            "is_staff": "true"
        },
        {
            "username": "test2",
            "hashed_password": "password",
            "is_staff": "true"
        },
        {
            "username": "test",
            "hashed_password": "password",
            "is_staff": "true"
        },
    ]
    response = await client.post('/users/bulk', json=data, headers=get_auth)
    assert response.status_code == 201
    assert len(response.json()) == 2


@mark.handlers
async def test_user_update(client: AsyncClient, get_auth: dict[str, str]):
    user = (await client.get('/users/', headers=get_auth)).json()[0]
    data = {"username": "changed"}
    response = await client.put(
        f'/users/{user['id']}', json=data, headers=get_auth)
    assert response.status_code == 200
    assert response.json()['username'] == data['username']


@mark.handlers
async def test_user_delete(client: AsyncClient, get_auth: dict[str, str]):
    response = await client.delete('/users/1', headers=get_auth)
    assert response.status_code == 200
    assert (await client.post('/users/', headers=get_auth)).status_code == 401
