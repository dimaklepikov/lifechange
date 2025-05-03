from uuid import UUID
from fastapi_users import schemas

class UserRead(schemas.BaseUser[UUID]):
    username: str

class UserCreate(schemas.BaseUserCreate):
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    username: str | None = None