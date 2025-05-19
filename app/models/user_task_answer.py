import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models import Task, User
from sqlalchemy.dialects.postgresql import ARRAY



class UserTaskAnswer(Base):
    __tablename__ = "user_task_answer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"), nullable=False)

    selected_option_ids: Mapped[Optional[list[int]]] = mapped_column(ARRAY(Integer), nullable=True)
    text_answer: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    task: Mapped["Task"] = relationship("Task")
    user: Mapped["User"] = relationship("User")
