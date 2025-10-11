from datetime import datetime

from pydantic import BaseModel

from app.project.models import ProjectStatus


class SProjectCreate(BaseModel):
    name: str
    status: ProjectStatus | None = ProjectStatus.NEW
    description: str | None = None
    person_in_charge: int | None = None
    start_time: datetime | None = None
    complete_time: datetime | None = None


class SProjectOut(BaseModel):
    id: int
    name: str
    status: ProjectStatus
    description: str | None
    person_in_charge: int | None
    create_time: datetime
    start_time: datetime | None
    complete_time: datetime | None

    model_config = {'from_attributes':  True}


class SProjectOutList(BaseModel):
    items: list[SProjectOut]
    page: int
    per_page: int
    has_prev: bool
    has_next: bool
    total_count: int


class SProjectUpdate(BaseModel):
    name: str | None = None
    status: ProjectStatus | None = None
    description: str | None = None
    person_in_charge: int | None = None
    start_time: datetime | None = None
    complete_time: datetime | None = None
