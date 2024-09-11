from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pg_client import PostgresClient
from settings import pwd_context

# Секретный ключ для JWT
SECRET_KEY = "12345"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(postgres_client: PostgresClient, email: str, password: str):
    user = postgres_client.select_users(email)[0]
    if not user:
        return False
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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
