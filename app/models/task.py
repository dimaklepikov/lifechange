from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import UUID
from app.database import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
