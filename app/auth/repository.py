from dataclasses import dataclass
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import TokenUser


@dataclass
class AuthRepo:
    db: AsyncSession

    async def save_refresh_token(
            self,
            token: str,
            sub: str,
            expires_at: int
    ) -> None:
        async with self.db as session:
            session.add(
                TokenUser(username=sub, token=token, expire=expires_at))
            await session.commit()

    async def compare_refresh(
            self,
            token: str,
            payload: dict[str, Any]
    ) -> bool:
        async with self.db as session:
            db_token: TokenUser | None = (await session.execute(
                select(TokenUser)
                .where(TokenUser.username == payload['sub']))
            ).scalar_one_or_none()

        return (
            False if not db_token
            or db_token.expire != payload['exp']
            or db_token.token != token else True
        )

    async def delete_refresh(self, token: str) -> None:
        async with self.db as session:
            await session.execute(
                delete(TokenUser).where(TokenUser.token == token))
            await session.commit()
