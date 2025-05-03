import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)