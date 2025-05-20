from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models import task_option_association


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
