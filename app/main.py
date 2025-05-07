from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from app.db.database import engine, Base
from app.admin import setup_admin


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

setup_admin(app)

app.include_router(auth_router)
app.include_router(user_router, prefix="/users", tags=["users"])
