from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.dependency import get_current_user, staff_only
from app.core.dependencies import get_password_service
from app.core.security import PasswordService
from app.users.dependencies import get_user_service
from app.users.schemas import SUserCreate, SUserOut, SUserUpdate
from app.users.service import UserService
from app.core.exceptions import UserNotFoundError, UsernameExistsError


router: APIRouter = APIRouter(prefix='/users', tags=['Users'])


@router.get('/{user_id}')
async def get_user_by_id(
    service: Annotated[UserService, Depends(get_user_service)],
    user_id: int
) -> SUserOut:
    user: SUserOut | None = await service.get_user_by_id(user_id)
    if not user:
        raise UserNotFoundError
    return user


@router.get('/')
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    user_ids: list[int] | None = Query(default=None)
) -> list[SUserOut]:
    if not user_ids:
        return await service.get_users()
    return await service.get_users_by_ids(user_ids)


@router.post('/')
async def create_user(
    service: Annotated[UserService, Depends(get_user_service)],
    pwd: Annotated[PasswordService, Depends(get_password_service)],
    cur_user: Annotated[SUserOut, Depends(get_current_user)],
    user_data: SUserCreate
) -> SUserOut:
    if not cur_user.is_staff:
        raise HTTPException(401)

    user: SUserOut | None = await service.create_user(user_data, pwd)
    if not user:
        raise UsernameExistsError
    return user


@router.post('/bulk')
async def create_users(
    service: Annotated[UserService, Depends(get_user_service)],
    pwd: Annotated[PasswordService, Depends(get_password_service)],
    _: Annotated[SUserOut, Depends(staff_only)],
    users_data: list[SUserCreate]
) -> list[SUserOut]:
    return await service.create_user_bulk(users_data, pwd)


@router.put('/{user_id}')
async def update_user(
    service: Annotated[UserService, Depends(get_user_service)],
    pwd: Annotated[PasswordService, Depends(get_password_service)],
    cur_user: Annotated[SUserOut, Depends(get_current_user)],
    user_id: int,
    user_data: SUserUpdate
) -> SUserOut:
    if not cur_user.is_staff and cur_user.id != user_id:
        raise HTTPException(401)

    user_to_update: SUserOut | None = await service.get_user_by_id(user_id)
    if not user_to_update:
        raise UserNotFoundError

    user: SUserOut | None = await service.update_user(
        user_to_update,
        user_data,
        pwd
    )
    if not user:
        raise UsernameExistsError
    return user


@router.delete('/{user_id}')
async def delete_user(
    service: Annotated[UserService, Depends(get_user_service)],
    cur_user: Annotated[SUserOut, Depends(get_current_user)],
    user_id: int
) -> SUserOut:
    if not cur_user.is_staff and cur_user.id != user_id:
        raise HTTPException(401)

    deleted_user: SUserOut | None = await service.delete_user(user_id)
    if not deleted_user:
        raise UserNotFoundError
    return deleted_user
