from pydantic import BaseModel


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    password: str


# Схема для вывода информации о пользователе
class UserOut(BaseModel):
    id: int
    username: str


# Схема для аутентификации
class Token(BaseModel):
    access_token: str
    token_type: str


# Схема для ввода данных аутентификации
class Login(BaseModel):
    username: str
    password: str


class AuthSchema(BaseModel):
    username: str
    password: str
