from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.users.routes import router as user_router
from app.db.database import engine, Base
from app.admin import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.config import SECRET_KEY

app = FastAPI()

setup_admin(app)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth_router)
app.include_router(user_router, prefix="/users", tags=["users"])  # app.include_router(user_router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
