from typing import Union

from loguru import logger
from passlib.context import CryptContext
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


class BackendAuth(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BACKEND_")

    username: str
    password: str


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):

    postgres_settings: PostgresSettings = PostgresSettings()
    logger_settings: LoggerSettings = LoggerSettings()
    backend_auth: BackendAuth = BackendAuth()
    jwt_settings: JWTSettings = JWTSettings()


settings = Settings()
logger.add(
    settings.logger_settings.log_file,
    format=settings.logger_settings.log_format,
    level=settings.logger_settings.log_level,
    rotation=settings.logger_settings.log_rotation,
    compression=settings.logger_settings.log_compression,
)
logger.info(settings.model_dump_json(indent=4))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
