import uvicorn
from fastapi import FastAPI
from routes import (
    auth_router,
    garak_list_probes,
    leaderboard_competitors,
    models_list,
    test,
    test_leaderboard,
)

app = FastAPI(
    title="Leaderboard API",
    description="API for red teaming testing",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


# @app.middleware("http")
# async def verify_token_middleware(request: Request, call_next):
#     print(f"REQUEST URL PATH: {request.url.path}")
#     if request.url.path in ["/docs", "/openapi.json", "/register", "/token"]:
#         return await call_next(request)

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     authorization: str = request.headers.get("Authorization")
#     if not authorization:
#         raise credentials_exception

#     scheme, token = authorization.split()
#     if scheme.lower() != "bearer":
#         raise credentials_exception

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     response = await call_next(request)
#     return response


app.include_router(garak_list_probes)
app.include_router(leaderboard_competitors)
app.include_router(models_list)
app.include_router(test)
app.include_router(test_leaderboard)
app.include_router(auth_router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
