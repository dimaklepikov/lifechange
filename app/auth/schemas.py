from uuid import UUID
from fastapi_users import schemas

class UserRead(schemas.BaseUser[UUID]):
    pass  # больше не нужно username

class UserCreate(schemas.BaseUserCreate):
    pass  # наследуем всё как есть: email + password

class UserUpdate(schemas.BaseUserUpdate):
    pass