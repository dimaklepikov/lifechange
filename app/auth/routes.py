from uuid import UUID

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.auth.manager import auth_backend, get_user_manager
from app.auth.schemas import AuthUserCreate, AuthUserRead
from app.models.user import User

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
