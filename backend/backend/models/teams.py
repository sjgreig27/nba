from pydantic import BaseModel

class Team(BaseModel):
    id: int
    conference: str
    division: str
    city: str
    name: str
    full_name: str
    abbreviation: str