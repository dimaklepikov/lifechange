from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.session import get_async_session
from app.models.task import Task
from app.models.user import User
from app.auth.routes import current_user
from typing import List
from app.tasks.schemas import TaskRead

router = APIRouter()

# TODO: Add response model
@router.get("/me")
async def get_my_tasks(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    result = await session.execute(
        select(Task).where(
            or_(
                Task.is_global == True,
                Task.assigned_user_id == user.id
            )
        )
    )
    return result.scalars().all()
