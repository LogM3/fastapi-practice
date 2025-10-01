from dataclasses import dataclass

from pydantic import ValidationError

from app.core.security import PasswordService
from app.users.repository import UserRepo
from app.users.schemas import SUserCreate, SUserOut, SUserUpdate


@dataclass
class UserService:
    repo: UserRepo

    async def get_user_by_id(self, user_id: int) -> SUserOut | None:
        try:
            result: SUserOut = SUserOut.model_validate(
                await self.repo.get_by_id(user_id)
            )
        except ValidationError:
            return None
        return result

    async def get_user_by_username(self, username: str) -> SUserOut | None:
        try:
            result: SUserOut = SUserOut.model_validate(
                await self.repo.get_by_username(username)
            )
        except ValidationError:
            return None
        return result

    async def get_users(self) -> list[SUserOut]:
        return [
            SUserOut.model_validate(usr)
            for usr in await self.repo.get_all()
        ]

    async def get_users_by_ids(self, user_ids: list[int]) -> list[SUserOut]:
        return [SUserOut.model_validate(user) for id in user_ids if (
            user := await self.repo.get_by_id(id))]

    async def create_user(
            self,
            user_data: SUserCreate,
            pwd: PasswordService
    ) -> SUserOut | None:
        if await self.repo.get_by_username(user_data.username):
            return

        user_data.hashed_password = await pwd.get_pwd_hash(
            user_data.hashed_password
        )
        return SUserOut.model_validate(
            await self.repo.create_user(user_data.model_dump())
        )

    async def create_user_bulk(
            self,
            users_data: list[SUserCreate],
            pwd: PasswordService
    ) -> list[SUserOut]:
        return [SUserOut.model_validate(user) for user_data in users_data if (
            user := await self.create_user(user_data, pwd))]

    async def update_user(
            self,
            user_to_update: SUserOut,
            user_data: SUserUpdate,
            pwd: PasswordService
    ) -> SUserOut | None:
        if (
            user_data.username != user_to_update.username and
            await self.repo.get_by_username(user_data.username)
        ):
            return

        if user_data.password:
            user_data.password = await pwd.get_pwd_hash(
                user_data.password
            )

        return SUserOut.model_validate(await self.repo.update_user(
            user_to_update.id,
            {
                'username': user_data.username,
                'hashed_password': user_data.password
            }
        ))

    async def delete_user(self, user_id: int) -> SUserOut | None:
        if not await self.repo.get_by_id(user_id):
            return

        return SUserOut.model_validate(await self.repo.delete_user(user_id))
