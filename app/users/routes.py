from fastapi import APIRouter, Depends
from app.models.user import User
from app.users.schemas import UserRead
from app.auth.routes import current_user

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_user)):
    return user
