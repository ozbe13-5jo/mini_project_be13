from typing import Optional

from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI


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

