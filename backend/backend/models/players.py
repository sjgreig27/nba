from pydantic import BaseModel
from .teams import Team


class Player(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    height: str | None
    weight: str | None
    jersey_number: str | None
    college: str | None
    country: str | None
    draft_year: int | None
    draft_round: int | None
    draft_number: int | None
    team: Team
