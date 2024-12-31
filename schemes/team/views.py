from fastapi import APIRouter

from schemes.team.scheme import Team

router = APIRouter(tags=['Team'])

@router.get("/{team_id}")
async def get_team(team_id:int, team: Team):
    return {"team_id": team_id,
            "team_name": team.name,
            "description": team.description,
            "players": team.players
            }