from fastapi import APIRouter
from uuid import UUID
from fastapi_users import FastAPIUsers
from app.auth.manager import get_user_manager, auth_backend
from app.models.user import User
from app.auth.schemas import AuthUserRead, AuthUserCreate

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(AuthUserRead, AuthUserCreate),
    prefix="/auth",
    tags=["auth"],
)
