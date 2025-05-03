from fastapi_users import schemas
from uuid import UUID
from typing import Optional

class UserRead(schemas.BaseUser[UUID]):
    name: Optional[str] = None

class UserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None