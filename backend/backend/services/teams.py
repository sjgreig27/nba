from typing import List

from .balldontlie.rest_api import RestApiService
from ..models.players import Player
from ..models.teams import Team


class TeamsService(RestApiService[Team]):

    def get_entity_name(self) -> str:
        return "teams"
