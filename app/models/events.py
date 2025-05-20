from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models.task import TaskType
from app.models.task_option import TaskOption


@event.listens_for(Session, "before_flush")
def prevent_task_option_for_text_tasks(session, flush_context, instances):
    """
    Prevents saving task options for text tasks
    """
    for obj in session.new:
        if isinstance(obj, TaskOption):
            for task in obj.tasks:
                if task.task_type == TaskType.text:
                    raise ValueError("❌ Нельзя привязывать опцию к заданию со свободным типом ответа")
