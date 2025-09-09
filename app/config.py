from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME: str = "fastapi-mini-project"
    ENV: str = "dev"
    SECRET_KEY: str = "change-me"
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")
settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "connections": {
        "default": f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    },
    "apps": {
        "models": {
            "models": ["app.models.models"],
            "default_connection": "default",
        }
    },
}

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models.users", "aerich.models"],  # 여기에 aerich.models 추가
            "default_connection": "default",
        }
    },
}
