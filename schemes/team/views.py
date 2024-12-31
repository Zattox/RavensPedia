from fastapi import APIRouter

from schemes.team.schema import Team

router = APIRouter(tags=['Team'])

@router.get("/")
async def get_team(
    team: Team
):
    return {"team_id": team.id,
            "team_name": team.name,
            "description": team.description,
            "players": team.players
            }