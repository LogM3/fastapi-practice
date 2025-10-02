from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TokenUser(Base):
    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    expire: Mapped[int] = mapped_column(nullable=False)
