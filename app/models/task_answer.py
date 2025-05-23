import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models import Task, User


class TaskAnswer(Base):
    __tablename__ = "task_answer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)

    selected_option_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer), nullable=True)
    text_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    task: Mapped["Task"] = relationship("Task")
    user: Mapped["User"] = relationship("User")
