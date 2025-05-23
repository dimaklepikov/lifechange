from typing import AsyncGenerator

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.db.database import async_session_maker
from app.models.user import User


async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(session, User)