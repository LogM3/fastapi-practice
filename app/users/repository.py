from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repo import BaseRepo
from app.users.models import User


@dataclass
class UserRepo(BaseRepo[User]):
    db: AsyncSession
    model: type[User] = User

    async def get_by_id(self, id: int) -> User | None:
        return await self.db.get(self.model, id)

    async def get_all(self) -> Sequence[User]:
        async with self.db as session:
            return (await session.execute(select(self.model))).scalars().all()

    async def get_by_username(self, username: str) -> User | None:
        async with self.db as session:
            return (await session.execute(
                select(self.model)
                .where(self.model.username == username)
            )).scalar_one_or_none()

    async def create_user(self, user_data: dict[Any, Any]) -> User:
        async with self.db as session:
            result = User(**user_data)
            session.add(result)
            await session.commit()
            return result

    async def update_user(
            self,
            user_id: int,
            user_data: dict[Any, Any]
    ) -> User:
        if not user_data['hashed_password']:
            del user_data['hashed_password']
        async with self.db as session:
            result = (await session.execute(
                update(self.model)
                .where(self.model.id == user_id)
                .values(**user_data)
                .returning(User)
            )).scalar_one()
            await session.commit()
            return result

    async def delete_user(self, user_id: int) -> User:
        async with self.db as session:
            result = (await session.execute(
                delete(self.model)
                .where(self.model.id == user_id)
                .returning(User)
            )).scalar_one()
            await session.commit()
            return result
