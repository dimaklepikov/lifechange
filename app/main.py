from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.database import engine, Base
from app.admin import setup_admin
from starlette.middleware.sessions import SessionMiddleware
from app.config import SECRET_KEY

app = FastAPI()

setup_admin(app)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
