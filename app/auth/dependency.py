from typing import Annotated, Any
from fastapi import Depends, HTTPException, Request

from app.auth.connector import UserConnector
from app.auth.repository import AuthRepo
from app.auth.service import AuthService
from app.core.database import Database
from app.core.dependencies import get_database, get_password_service
from app.core.exceptions import UserNotFoundError
from app.core.security import PasswordService, oauth2_scheme
from app.users.dependencies import get_user_service
from app.users.schemas import SUserOut
from app.users.service import UserService


async def get_connector(
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    return UserConnector(user_service)


async def get_auth_repo(
        db: Annotated[Database, Depends(get_database)]
) -> AuthRepo:
    return AuthRepo(db)


async def get_auth_service(
        connector: Annotated[UserConnector, Depends(get_connector)],
        pwd: Annotated[PasswordService, Depends(get_password_service)],
        repo: Annotated[AuthRepo, Depends(get_auth_repo)]
) -> AuthService:
    return AuthService(connector, pwd, repo)


async def get_current_user(
        connector: Annotated[UserConnector, Depends(get_connector)],
        request: Request,
        _: Annotated[str, Depends(oauth2_scheme)]
) -> SUserOut:
    user_payload: dict[str, Any] | None | HTTPException = getattr(
        request.state,
        'user_payload',
        None
    )
    if not user_payload:
        raise HTTPException(401)
    if isinstance(user_payload, HTTPException):
        raise user_payload
    user: SUserOut | None = await connector.get_user_by_username(
        user_payload['sub']
    )
    if not user:
        raise UserNotFoundError
    return user
