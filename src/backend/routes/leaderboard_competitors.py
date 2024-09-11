from fastapi import APIRouter, Depends
from loguru import logger
from pg_client import PostgresClient
from schemas import LeaderboardCompetitorsResponse
from settings import Settings

router = APIRouter()


def get_settings():
    return Settings()


def get_postgres_client(settings: Settings = Depends(get_settings)):
    return PostgresClient(settings=settings.postgres_settings)


@router.get("/leaderboard_competitors", response_model=LeaderboardCompetitorsResponse)
async def get_leaderboard_competitors(
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    try:
        result = postgres_client.select_competitors()
        logger.info(f"Fetched {len(result)} competitors from leaderboard")
        return LeaderboardCompetitorsResponse(result=result)
    except Exception as e:
        logger.error(f"Error fetching competitors: {e}")
        return LeaderboardCompetitorsResponse(error=str(e))