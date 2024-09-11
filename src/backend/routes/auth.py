from datetime import timedelta

from authorization.authorization_utils import authenticate_user, create_access_token
from authorization.schemas import AuthSchema, Token, UserCreate, UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from pg_client import PostgresClient, get_postgres_client
from settings import pwd_context

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: AuthSchema,
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    user = authenticate_user(postgres_client, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
def register_user(
    user: UserCreate,
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    db_user = postgres_client.select_users(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)

    user_id = postgres_client.insert_user(user, hashed_password)

    return {"id": user_id, "email": user.email, "full_name": user.full_name}
