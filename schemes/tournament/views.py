from fastapi import APIRouter

from schemes.tournament.scheme import Tournament

router = APIRouter(tags=['Tournament'])

@router.get("/")
async def get_tournament(
    tournament: Tournament
):
    return {"team_id": tournament.id,
            "team_name": tournament.name,
            "description": tournament.description,
            "teams": tournament.teams,
            "matches": tournament.matches
            }