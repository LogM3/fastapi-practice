from dataclasses import dataclass
from app.core.database import Database


@dataclass
class AuthRepo:
    db: Database

    async def save_refresh_token(
            self,
            token: str,
            sub: str,
            expires_at: int
    ) -> None:
        with self.db as db:
            db['refresh'][token] = {'sub': sub, 'expires_at': expires_at}
