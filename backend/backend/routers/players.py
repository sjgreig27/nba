from fastapi import APIRouter
from typing import List, Annotated
from fastapi.params import Depends
from ..models.players import Player
from ..services.balldontlie.rest_api import RestApiService
from ..dependencies.pagination import pagination_parameters
from ..dependencies.services.players import get_player_service

router = APIRouter()


@router.get("/players/", tags=["players"])
async def read_players(
    pagination: Annotated[dict, Depends(pagination_parameters)],
    service: Annotated[RestApiService, Depends(get_player_service)],
) -> List[Player]:
    return service.get_item_list(pagination)


@router.get("/players/{player_id}", tags=["players"])
async def get_player_details(
    player_id: int,
    service: Annotated[RestApiService, Depends(get_player_service)],
) -> Player:
    return service.get_item(player_id)
