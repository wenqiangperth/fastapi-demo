from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = "fastapi-demo"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "test", "prod"] = "local"


settings = Settings()
