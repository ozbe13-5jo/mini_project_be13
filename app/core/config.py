from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    APP_NAME: str = "fastapi-mini-project"
    ENV: str = "dev"
    SECRET_KEY: str = "change-me"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()