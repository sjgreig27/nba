from operator import itemgetter
from typing import List, Optional
from .balldontlie.rest_api import PaginatedRestApiService
from ..models.players import Player


class PlayerService(PaginatedRestApiService[Player]):

    def get_entity_name(self) -> str:
        return "players"

    def get_players_for_team(
        self,
        team_id: int,
        pagination_params: dict,
    ) -> List[Player]:
        url = self.get_url()
        kwargs = {"params": {"team_ids[]": team_id}}
        limit, offset = itemgetter("limit", "offset")(pagination_params)
        return self.fetch_paginated_data(url, limit=limit, offset=offset, kwargs=kwargs)
