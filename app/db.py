from typing import Optional, AsyncGenerator
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from contextlib import asynccontextmanager


DB_URL = "postgresql://testuser:asdfg123@localhost:5432/testdb"

async def init_db():
    await Tortoise.init(
        config={
            "connections": {"default": DB_URL},
            "apps": {
                "models": {
                    "models": ["app.models"]
                }
            },
        }
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()


def init_tortoise(app: FastAPI, db_url: Optional[str] = None) -> None:
    """
    Register Tortoise ORM with FastAPI. Call from your app startup.

    Example:
        from app.db import init_tortoise
        init_tortoise(app, db_url="sqlite://db.sqlite3")
    """
    register_tortoise(
        app,
        db_url=db_url or "sqlite://db.sqlite3",
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 앱 시작 시 DB 초기화
    await init_db()
    yield
    # 앱 종료 시 DB 연결 종료
    await close_db()
