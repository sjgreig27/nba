from fastapi import APIRouter
from typing import List, Annotated
from fastapi.params import Depends
from ..models.teams import Team
from ..models.players import Player
from ..services.balldontlie.rest_api import RestApiService
from ..dependencies.pagination import pagination_parameters
from ..dependencies.services.teams import get_teams_service
from ..dependencies.services.players import get_player_service
from ..services.players import PlayerService

router = APIRouter()


@router.get("/teams/", tags=["teams"])
async def read_teams(
    pagination: Annotated[dict, Depends(pagination_parameters)],
    service: Annotated[RestApiService, Depends(get_teams_service)],
) -> List[Team]:
    return service.get_item_list(pagination)


@router.get("/teams/{team_id}", tags=["teams"])
async def get_team_details(
    team_id: int,
    service: Annotated[RestApiService, Depends(get_teams_service)],
) -> Team:
    return service.get_item(team_id)


@router.get("/teams/{team_id}/roster", tags=["teams"])
async def get_team_roster(
    team_id: int,
    pagination: Annotated[dict, Depends(pagination_parameters)],
    service: Annotated[PlayerService, Depends(get_player_service)],
) -> List[Player]:
    return service.get_players_for_team(team_id, pagination)
