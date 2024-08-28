from ...services.balldontlie.rest_api import RestApiService
from ...services.players import PlayerService


async def get_player_service() -> RestApiService:
    return PlayerService()
