from pydantic import BaseModel


class TestJson(BaseModel):
    userId: int
    id: int
    title: str
    body: str
