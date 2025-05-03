from typing import AsyncGenerator
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.database import async_session_maker

async def get_user_db() -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    async with async_session_maker() as session:
        print("🧪 Connected to DB:", session.bind.url)
        yield SQLAlchemyUserDatabase(session, User)