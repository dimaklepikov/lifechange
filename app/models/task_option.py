import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models import Task, task_option_association


class TaskOption(Base):
    __tablename__ = "task_option"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String, nullable=False)

    tasks = relationship(
        "Task",
        secondary=task_option_association,
        back_populates="options"
    )

    def __str__(self):
        return self.text
