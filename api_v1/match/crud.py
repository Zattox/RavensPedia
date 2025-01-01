from fastapi import APIRouter

from api_v1.match.scheme import Match

router = APIRouter(tags=["Match"])


@router.get("/{match_id}")
async def get_match(match_id: int, match: Match):
    return {
        "match_id": match_id,
        "first_team": match.first_team,
        "second_team": match.second_team,
        "tournament": match.tournament,
        "date": match.date,
    }
