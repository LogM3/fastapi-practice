from pydantic import BaseModel, Field


class SUser(BaseModel):
    username: str


class SUserOut(SUser):
    id: int
    is_staff: bool
    password: str


class SUserUpdate(SUser):
    password: str | None = None


class SUserCreate(SUser):
    password: str
    is_staff: bool | None = Field(default=False)
