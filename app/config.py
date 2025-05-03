import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/lifechange")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
