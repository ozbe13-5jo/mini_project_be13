from typing import Optional, AsyncGenerator
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

DB_URL = "postgres://testuser:asdfg123@localhost:5432/testdb"

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


def init_tortoise(app: Optional[FastAPI] = None, db_url: Optional[str] = None) -> None:
    if app:
        register_tortoise(
            app,
            db_url=DB_URL,
            modules={"models": ["app.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
    )
    else:
        asyncio.run(Tortoise.init(
            db_url=db_url,
            modules={"models": ["app.models"]}
        ))
        asyncio.run(Tortoise.generate_schemas())

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # 앱 시작 시 DB 초기화
    await init_db()
    yield
    # 앱 종료 시 DB 연결 종료
    await close_db()
