from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
