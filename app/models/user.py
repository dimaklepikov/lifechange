from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Float
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[str] = mapped_column(Integer, nullable=True)
    weight: Mapped[str] = mapped_column(Float, nullable=True)
    height: Mapped[str] = mapped_column(Float, nullable=True)
