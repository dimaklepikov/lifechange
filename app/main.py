from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.database import engine, Base

app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
