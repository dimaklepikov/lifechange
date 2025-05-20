from typing import Optional
from uuid import UUID

from fastapi_users import schemas


class AuthUserRead(schemas.BaseUser[UUID]):
    id: UUID
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class AuthUserCreate(schemas.BaseUserCreate):
    name: Optional[str] = None

class AuthUserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None
