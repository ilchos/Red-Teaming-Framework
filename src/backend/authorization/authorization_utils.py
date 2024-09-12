from datetime import datetime, timedelta, timezone

from jose import jwt
from loguru import logger
from pg_client import PostgresClient, get_postgres_client
from psycopg.errors import UniqueViolation
from settings import pwd_context, settings


def authenticate_user(postgres_client: PostgresClient, username: str, password: str):
    user = postgres_client.select_users(username)

    if not user:
        return False
    user = user[0]
    if not pwd_context.verify(password, user["password_hash"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
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


def create_tech_user():
    hashed_password = pwd_context.hash(settings.backend_auth.password)
    postgres_client = get_postgres_client(settings=settings)
    try:
        postgres_client.insert_user(settings.backend_auth, hashed_password)
    except UniqueViolation:
        logger.info("TECH USER ALREADY EXISTS")
