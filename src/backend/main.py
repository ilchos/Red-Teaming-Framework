from contextlib import asynccontextmanager

import uvicorn
from authorization.authorization_utils import create_tech_user
from fastapi import FastAPI
from routes import auth_router, leaderboard_competitors, upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tech_user()
    yield


app = FastAPI(
    title="Leaderboard API",
    description="API for red teaming testing",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(leaderboard_competitors)
app.include_router(auth_router)
app.include_router(upload_router)


def main():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
