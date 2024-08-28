from fastapi import APIRouter
from typing import List, Annotated
from fastapi.params import Depends
from ..models.teams import Team
from ..services.balldontlie.rest_api import RestApiService
from ..dependencies.pagination import pagination_parameters
from ..dependencies.services.teams import get_teams_service

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
