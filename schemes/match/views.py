from fastapi import APIRouter

from schemes.match.scheme import Match

router = APIRouter(tags=['Match'])

@router.get("/")
async def get_player(
    match: Match
):
    return {"match_id": match.id,
            "first_team": match.first_team,
            "second_team": match.second_team,
            "tournament": match.tournament,
            "date": match.date,
            }