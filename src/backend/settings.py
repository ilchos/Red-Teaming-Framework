from typing import Union

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoggerSettings(BaseSettings):
    log_level: Union[str, int] = "DEBUG"
    log_file: str = "logs/log.txt"
    log_format: str = "{time} {level} {message}"
    log_rotation: str = "100 MB"
    log_compression: str = "zip"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PG_")

    host: str = "postgres"
    dbname: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"


class Settings(BaseSettings):

    postgres_settings: PostgresSettings = PostgresSettings()
    logger_settings: LoggerSettings = LoggerSettings()

    vse_gpt_url: str = "https://api.vsegpt.ru/v1/chat/completions"
    vse_gpt_api_key: str


settings = Settings()
logger.add(
    settings.logger_settings.log_file,
    format=settings.logger_settings.log_format,
    level=settings.logger_settings.log_level,
    rotation=settings.logger_settings.log_rotation,
    compression=settings.logger_settings.log_compression,
)
logger.info(settings.model_dump_json(indent=4))
