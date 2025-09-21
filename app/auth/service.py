from dataclasses import dataclass
import time
from typing import Any

from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.repository import AuthRepo
from app.settings import settings
from app.auth.connector import UserConnector
from app.auth.schemas import SAuthRegister, TokenPair
from app.core.security import PasswordService
from app.users.schemas import SUserCreate, SUserOut


@dataclass
class AuthService:
    connector: UserConnector
    pwd_service: PasswordService
    repo: AuthRepo

    async def register(self, payload: SAuthRegister) -> SUserOut | None:
        user_data: SUserCreate = SUserCreate.model_validate(
            payload.model_dump()
        )
        return await self.connector.create_user(user_data, self.pwd_service)

    async def _validate_credentials(
            self,
            credentials: OAuth2PasswordRequestForm
    ) -> bool:
        user: SUserOut | None = await self.connector.get_user_by_username(
            credentials.username
        )
        if (not user or not await self.pwd_service.verify_pwd_hash(
            user.password, credentials.password
        )):
            return False

        return True

    async def _create_tokens(self, username: str) -> TokenPair:
        now: int = int(time.time())
        access_expire: int = now + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        refresh_expire: int = (
            now + settings.REFRESH_TOKEN_EXPIRE_DAYS * 3600 * 24
        )

        access_payload: dict[str, Any] = {
            'sub': username,
            'exp': access_expire,
            'iat': now,
            'typ': 'access'
        }
        refresh_payload: dict[str, Any] = {
            'sub': username,
            'exp': refresh_expire,
            'iat': now,
            'typ': 'refresh'
        }

        return TokenPair(
            access_token=jwt.encode(
                access_payload,
                settings.JWT_SECRET,
                settings.JWT_ALGORITHM
            ),
            refresh_token=jwt.encode(
                refresh_payload,
                settings.JWT_SECRET,
                settings.JWT_ALGORITHM
            ),
            expires_in=access_expire
        )

    async def login(
            self,
            credentials: OAuth2PasswordRequestForm
    ) -> TokenPair | None:
        if not await self._validate_credentials(credentials):
            return

        tokens: TokenPair = await self._create_tokens(credentials.username)
        await self.repo.save_refresh_token(
            tokens.refresh_token,
            credentials.username,
            tokens.expires_in
        )
        return tokens
