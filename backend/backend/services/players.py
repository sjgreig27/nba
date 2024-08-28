from .balldontlie.rest_api import PaginatedRestApiService
from ..models.players import Player


class PlayerService(PaginatedRestApiService[Player]):

    def get_entity_name(self) -> str:
        return "players"
