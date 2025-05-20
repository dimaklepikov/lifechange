import enum
from typing import Optional

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models import User


class TaskType(str, enum.Enum):
    single_choice = "single_choice"
    multiple_choice = "multiple_choice"
    text = "text"


    @property
    def label(self):
        match self:
            case TaskType.single_choice:
                return "Один вариант"
            case TaskType.multiple_choice:
                return "Несколько вариантов"
            case TaskType.text:
                return "Свой ответ"
        return None

task_option_association = Table(
    "task_option_link",
    Base.metadata,
    Column("task_id", ForeignKey("task.id"), primary_key=True),
    Column("option_id", ForeignKey("task_option.id"), primary_key=True),
)


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType, name='task_type_enum'), nullable=False)
    assigned_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    assigned_user: Mapped[Optional["User"]] = relationship("User", backref="assigned_tasks", lazy="joined")
    is_global: Mapped[bool] = mapped_column(Boolean, default=False)
    options = relationship(
        "TaskOption",
        secondary=task_option_association,
        back_populates="tasks"
    )

    def __str__(self):
        return self.title
