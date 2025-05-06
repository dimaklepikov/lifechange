from uuid import UUID
from typing import AsyncGenerator

from fastapi_users.manager import BaseUserManager
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from app.models.user import User
from app.auth.user_db import get_user_db
from app.config import SECRET_KEY
from app.auth.schemas import AuthUserCreate

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    def __init__(self, user_db):
        super().__init__(user_db)


    def parse_id(self, user_id: str) -> UUID:
        return UUID(user_id)

    async def create(
        self,
        user_create: AuthUserCreate,
        safe: bool = False,
        request=None
    ) -> User:
        user_dict = {
            "email": user_create.email,
            "hashed_password": self.password_helper.hash(user_create.password),
            "name": user_create.name,
            "is_active": True,
            "is_admin": False
        }

        return await self.user_db.create(user_dict)

async def get_user_manager() -> AsyncGenerator[UserManager, None]:
    async for user_db in get_user_db():
        yield UserManager(user_db)