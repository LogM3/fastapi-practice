from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProjectStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    status: Mapped[ProjectStatus] = mapped_column(
        nullable=False, default=ProjectStatus.NEW)
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    complete_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    description: Mapped[str | None]
    person_in_charge: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL')
    )
    # person_in_charge: Mapped[User | None] = relationship(
    #     'User', back_populates='projects'
    # )
