from fastapi_users import schemas
from uuid import UUID
from typing import Optional

class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    is_active: Optional[bool]

    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None