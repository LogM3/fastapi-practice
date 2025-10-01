from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AuthRepo:
    db: AsyncSession

    async def save_refresh_token(
            self,
            token: str,
            sub: str,
            expires_at: int
    ) -> None:
        with self.db as db:
            db['refresh'][token] = {'sub': sub, 'exp': expires_at}

    async def compare_refresh(
            self,
            token: str,
            payload: dict[str, Any]
    ) -> bool:
        with self.db as db:
            db_payload: dict[str, Any] = db['refresh'].get(token)
            print(db_payload == payload)
        return True if db_payload and db_payload == payload else False

    async def delete_refresh(self, token: str) -> None:
        with self.db as db:
            del db['refresh'][token]
