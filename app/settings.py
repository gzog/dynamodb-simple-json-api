from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    sentry_dsn: str = "https://b5c2f49ccf20cdd5daec6f03d656cbdc@o4504411712258048.ingest.sentry.io/4505773483950080"

    environment: str = Field(..., env="environment")

    aws_access_key_id: str = Field(..., env="aws_access_key_id")
    aws_secret_access_key: str = Field(..., env="aws_secret_access_key")
    aws_region_name: str = Field(..., env="region_name")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


class Environment(str, Enum):
    Production = "production"
    Local = "local"