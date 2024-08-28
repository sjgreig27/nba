from ...services.balldontlie.rest_api import RestApiService
from ...services.teams import TeamsService


async def get_teams_service() -> RestApiService:
    return TeamsService()
