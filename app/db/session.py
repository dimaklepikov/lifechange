from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        return session
