
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.routes import current_user
from app.db.session import get_async_session
from app.models.user import User
from app.users.schemas import UserRead, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_user)):
    return user

@router.patch("/me", response_model=UserUpdate)
async def update_me(
    data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    db_user = await session.scalar(select(User).where(User.id == user.id))

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    await session.commit()
    await session.refresh(db_user)
    return db_user
