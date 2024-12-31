from fastapi import APIRouter

from schemes.tournament.scheme import Tournament

router = APIRouter(tags=['Tournament'])

@router.get("/{tournament_id}")
async def get_tournament(tournament_id:int, tournament: Tournament):
    return {"team_id": tournament_id,
            "team_name": tournament.name,
            "description": tournament.description,
            "teams": tournament.teams,
            "matches": tournament.matches
            }