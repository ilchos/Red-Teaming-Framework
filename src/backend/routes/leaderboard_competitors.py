from authorization.jwt_bearer import JWTBearer
from fastapi import APIRouter, Depends
from loguru import logger
from pg_client import PostgresClient, get_postgres_client
from schemas import LeaderboardCompetitorsResponse

router = APIRouter()


@router.get(
    "/leaderboard_competitors",
    response_model=LeaderboardCompetitorsResponse,
    dependencies=[Depends(JWTBearer())],
)
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
