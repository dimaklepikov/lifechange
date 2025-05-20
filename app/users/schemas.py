from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel, field_validator


class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]

    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    is_admin: Optional[bool] = None

    @classmethod
    @field_validator("weight", "height", mode="before")
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v