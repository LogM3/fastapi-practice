from dataclasses import dataclass

from app.users.schemas import SUserCreate, SUserOut, SUserUpdate
from app.core.database import Database


@dataclass
class UserRepo:
    db: Database

    async def get_by_id(self, id: int) -> SUserOut | None:
        with self.db as db:
            result = db['users'].get(id)
        return SUserOut.model_validate(result) if result else None

    async def get_all(self) -> list[SUserOut]:
        with self.db as db:
            result = db['users'].values()
        return [SUserOut.model_validate(user) for user in result]

    async def get_by_username(self, username: str) -> SUserOut | None:
        with self.db as db:
            for user in db['users'].values():
                if user['username'] == username:
                    return user

    async def create_user(self, user_data: SUserCreate) -> SUserOut:
        with self.db as db:
            id: int = max(db['users'].keys()) + 1
            user: dict = user_data.model_dump()
            user.update({'id': id})
            db['users'].update({id: user})
            return SUserOut.model_validate(db['users'][id])

    async def update_user(
            self,
            user_id: int,
            user_data: SUserUpdate
    ) -> SUserOut:
        with self.db as db:
            data: dict = user_data.model_dump()
            if not data['password']:
                del data['password']
            db['users'][user_id].update(data)
            return SUserOut.model_validate(db['users'][user_id])

    async def delete_user(self, user_id: int) -> SUserOut:
        with self.db as db:
            deleted_user: SUserOut = SUserOut.model_validate(
                db['users'][user_id]
            )
            del db['users'][user_id]
        return deleted_user
