from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from typing import Optional

class TaskType(str, Enum):
    single_choice = "single_choice"
    multiple_choice = "multiple_choice"
    text = "text"

class TaskRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    task_type: TaskType
    is_global: bool
    assigned_user_id: Optional[UUID]

    class Config:
        from_attributes = True
