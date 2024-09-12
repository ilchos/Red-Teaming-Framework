from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from jose import jwt
from loguru import logger
from pg_client import PostgresClient, get_postgres_client
from psycopg.errors import UniqueViolation
from settings import pwd_context, settings


def authenticate_user(
    postgres_client: PostgresClient, username: str, password: str
) -> Optional[Dict]:
    """
    Аутентифицирует пользователя по имени пользователя и паролю.

    Args:
        postgres_client (PostgresClient): Клиент для работы с PostgreSQL.
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Returns:
        Optional[Dict]: Информация о пользователе, если аутентификация прошла успешно, иначе None.
    """
    user = postgres_client.select_users(username)

    if not user:
        logger.warning(f"User {username} not found")
        return None
    user = user[0]
    if not pwd_context.verify(password, user["password_hash"]):
        logger.warning(f"Invalid password for user {username}")
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT-токен доступа.

    Args:
        data (dict): Данные для кодирования в токене.
        expires_delta (Optional[timedelta]): Время жизни токена. Если не указано,
        токен будет действителен 15 минут.

    Returns:
        str: Закодированный JWT-токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_settings.secret_key,
        algorithm=settings.jwt_settings.algorithm,
    )
    return encoded_jwt


def create_tech_user() -> None:
    """
    Создает технического пользователя, если он еще не существует.
    """
    hashed_password = pwd_context.hash(settings.backend_auth.password)
    postgres_client = get_postgres_client(settings=settings)
    try:
        postgres_client.insert_user(settings.backend_auth, hashed_password)
        logger.info("TECH USER CREATED")
    except UniqueViolation:
        logger.info("TECH USER ALREADY EXISTS")
