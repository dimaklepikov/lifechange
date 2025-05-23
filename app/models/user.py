from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)

    def __str__(self):
        return f"{self.name} ({self.email})" if self.name else self.email
