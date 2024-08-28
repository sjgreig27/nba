from fastapi import FastAPI
from .routers.teams import router as team_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(team_router)
