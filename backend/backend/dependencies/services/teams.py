from ...services.teams import TeamsService


async def get_teams_service() -> TeamsService:
    return TeamsService()
