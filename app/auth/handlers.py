from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependency import get_auth_service
from app.auth.schemas import SAuthRegister, TokenPair
from app.auth.service import AuthService
from app.users.schemas import SUserOut
from app.core.exceptions import UsernameExistsError, WrongCredentialsError


router: APIRouter = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(
    service: Annotated[AuthService, Depends(get_auth_service)],
    user_data: SAuthRegister
) -> SUserOut | None:
    user: SUserOut | None = await service.register(user_data)
    if not user:
        raise UsernameExistsError
    return user


@router.post('/login')
async def login(
    service: Annotated[AuthService, Depends(get_auth_service)],
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenPair:
    tokens: TokenPair | None = await service.login(credentials)
    if not tokens:
        raise WrongCredentialsError
    return tokens
