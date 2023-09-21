from enum import Enum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sentry_dsn: str = Field(json_schema_extra={"env": "sentry_dsn"})

    environment: str = Field(json_schema_extra={"env": "environment"})

    aws_access_key_id: str = Field(json_schema_extra={"env": "aws_access_key_id"})
    aws_secret_access_key: str = Field(json_schema_extra={"env": "aws_secret_access_key"})
    aws_region_name: str = Field(json_schema_extra={"env": "region_name"})
    aws_dynamodb_table_name: str = Field(
        json_schema_extra={"env": "aws_dynamodb_table_name"}
    )

    requests_per_second: int = Field(json_schema_extra={"env": "requests_per_second"})

    log_level: str = Field(json_schema_extra={"env": "log_level"}, default="INFO")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    max_upload_size: int = 409_600  # 400KB

    disable_existing_loggers: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


class Environment(str, Enum):
    Production = "production"
    Local = "local"
    Test = "test"
