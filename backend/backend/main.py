from fastapi import FastAPI
from .routers.teams import router as team_router
from .routers.players import router as player_router

app = FastAPI()


app.include_router(team_router)
app.include_router(player_router)
