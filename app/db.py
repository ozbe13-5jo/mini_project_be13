from typing import Optional
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI


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


def init_tortoise(app: FastAPI, db_url: Optional[str] = None) -> None:
        register_tortoise(
            app,
            db_url=DB_URL,
            modules={"models": ["app.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
    )
