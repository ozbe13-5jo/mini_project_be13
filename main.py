import os
import asyncio
from fastapi import FastAPI
from tortoise import Tortoise
from dotenv import load_dotenv
from app.models import User  # models.py 안 User 모델
from app.config import DB_CONFIG
from app.routers import quote
from app.crud.bookmark import is_bookmarked, add_bookmark, remove_bookmark

app = FastAPI(title="Quotes App")

# 라우터 등록
app.include_router(quote.router)

load_dotenv()

DB_CONFIG = {
    "connections": {
        "default": f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    },
    "apps": {
        "models": {
            "models": ["app.models.models"],  # models 폴더 안 models.py
            "default_connection": "default",
        }
    },
}

async def init():
    await Tortoise.init(config=DB_CONFIG)
    await Tortoise.generate_schemas()
    user = await User.create(name="승현")
    users = await User.all()
    print([u.name for u in users])

if __name__ == "__main__":
    asyncio.run(init())
