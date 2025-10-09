from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import TokenUser


@dataclass
class AuthRepo:
    db: AsyncSession

    async def get_all(self) -> Sequence[TokenUser]:
        async with self.db as session:
            return (await session.execute(select(TokenUser))).scalars().all()

    async def get_refresh(self, sub: str) -> TokenUser | None:
        async with self.db as session:
            return (await session.execute(
                select(TokenUser).where(TokenUser.username == sub)
            )).scalar_one_or_none()

    async def save_refresh_token(
            self,
            token: str,
            sub: str,
            expires_at: int
    ) -> TokenUser:
        async with self.db as session:
            result: TokenUser = TokenUser(
                username=sub, token=token, expire=expires_at)
            session.add(result)
            await session.commit()
            return result

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
