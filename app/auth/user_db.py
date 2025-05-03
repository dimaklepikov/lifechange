import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from app.models.user import User
from app.database import async_session_maker
from typing import AsyncGenerator

class CustomUserDatabase(SQLAlchemyUserDatabase[User, uuid.UUID]):
    async def get_by_username(self, username: str):
        stmt = select(self.user_table).where(self.user_table.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

async def get_user_db() -> AsyncGenerator[CustomUserDatabase, None]:
    async with async_session_maker() as session:
        yield CustomUserDatabase(session, User)