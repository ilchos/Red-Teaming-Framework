from datetime import timedelta

from authorization.authorization_utils import authenticate_user, create_access_token
from authorization.schemas import AuthSchema, Token, UserCreate, UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from pg_client import PostgresClient, get_postgres_client
from settings import pwd_context, settings

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: AuthSchema,
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    user = authenticate_user(postgres_client, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.jwt_settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
def register_user(
    user: UserCreate,
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    db_user = postgres_client.select_users(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)

    user_id = postgres_client.insert_user(user, hashed_password)

    return {"id": user_id, "username": user.username}
