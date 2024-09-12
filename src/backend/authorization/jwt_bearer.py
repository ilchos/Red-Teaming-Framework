from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from loguru import logger
from settings import settings


class JWTBearer(HTTPBearer):
    """
    Класс для проверки JWT-токенов в запросах.

    Attributes:
        auto_error (bool): Флаг, указывающий, следует ли автоматически возвращать ошибку,
        если токен недействителен.
    """

    def __init__(self, auto_error: bool = True):
        """
        Инициализация класса JWTBearer.

        Args:
            auto_error (bool): Флаг, указывающий, следует ли автоматически возвращать ошибку,
            если токен недействителен.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Проверяет наличие и валидность JWT-токена в запросе.

        Args:
            request (Request): Запрос FastAPI.

        Returns:
            Optional[str]: JWT-токен, если он действителен, иначе None.
        """
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                logger.error("Invalid authentication scheme.")
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                logger.error("Invalid token or expired token.")
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            logger.error("Invalid authorization code.")
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Проверяет валидность JWT-токена.

        Args:
            jwtoken (str): JWT-токен для проверки.

        Returns:
            bool: True, если токен действителен, иначе False.
        """
        isTokenValid: bool = False

        try:
            payload = jwt.decode(
                jwtoken,
                settings.jwt_settings.secret_key,
                algorithms=[settings.jwt_settings.algorithm],
            )
        except Exception as e:
            logger.error(f"Error decoding JWT token: {e}")
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid
