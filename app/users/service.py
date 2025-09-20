from dataclasses import dataclass

from app.core.security import PasswordService
from app.users.repository import UserRepo
from app.users.schemas import SUserCreate, SUserOut, SUserUpdate


@dataclass
class UserService:
    repo: UserRepo

    async def get_user_by_id(self, user_id: int) -> SUserOut | None:
        return await self.repo.get_by_id(user_id)

    async def get_users(self) -> list[SUserOut]:
        return await self.repo.get_all()

    async def get_users_by_ids(self, user_ids: list[int]) -> list[SUserOut]:
        return [user for id in user_ids if (
            user := await self.repo.get_by_id(id))]

    async def create_user(
            self,
            user_data: SUserCreate,
            pwd: PasswordService
    ) -> SUserOut | None:
        if await self.repo.get_by_username(user_data.username):
            return

        user_data.password = await pwd.get_pwd_hash(user_data.password)
        return await self.repo.create_user(user_data)

    async def create_user_bulk(
            self,
            users_data: list[SUserCreate],
            pwd: PasswordService
    ) -> list[SUserOut]:
        return [user for user_data in users_data if (
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
            user_data.password = await pwd.get_pwd_hash(user_data.password)

        return await self.repo.update_user(
            user_to_update.id,
            user_data
        )
    
    async def delete_user(self, user_id: int) -> SUserOut | None:
        if not await self.repo.get_by_id(user_id):
            return
        
        return await self.repo.delete_user(user_id)

