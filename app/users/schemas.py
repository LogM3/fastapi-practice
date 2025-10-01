from pydantic import BaseModel, Field


class SUser(BaseModel):
    username: str


class SUserOut(SUser):
    id: int
    is_staff: bool
    hashed_password: str

    model_config = {'from_attributes':  True}


class SUserUpdate(SUser):
    password: str | None = None


class SUserCreate(SUser):
    hashed_password: str
    is_staff: bool | None = Field(default=False)
