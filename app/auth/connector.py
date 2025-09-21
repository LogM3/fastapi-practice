from dataclasses import dataclass

from app.core.security import PasswordService
from app.users.schemas import SUserCreate, SUserOut
from app.users.service import UserService


@dataclass
class UserConnector:
    user_service: UserService

    async def create_user(
            self,
            user_data: SUserCreate,
            pwd: PasswordService
    ) -> SUserOut | None:
        return await self.user_service.create_user(user_data, pwd)

    async def get_user_by_username(self, username: str) -> SUserOut | None:
        return await self.user_service.get_user_by_username(username)
