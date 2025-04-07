from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_team_map_stats
from .schemes import ResponseTeamMapStats
from ..team.dependencies import get_team_by_name

from ravenspedia.core import db_helper, TableTeam, TableTeamMapStats

# Define a router for team statistics endpoints
router = APIRouter(tags=["Team Stats"])


def table_to_response_form(
    map_stats: TableTeamMapStats,
) -> ResponseTeamMapStats:
    """
    Convert a TableTeamMapStats object to a ResponseTeamMapStats model for API responses.
    """
    return ResponseTeamMapStats(
        map=map_stats.map,
        matches_won=map_stats.matches_won,
        matches_played=map_stats.matches_played,
        win_rate=map_stats.win_rate,
    )


@router.get(
    "/{team_name}/",
    response_model=List[ResponseTeamMapStats],
    status_code=status.HTTP_200_OK,
)
async def get_team_stats(
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[ResponseTeamMapStats]:
    """
    Retrieve map statistics for a team by its name.
    """
    # Fetch the team's map statistics from the database
    team_stats = await get_team_map_stats(session=session, team=team)
    # Convert each map stats object to the response format
    result = [table_to_response_form(map_name) for map_name in team_stats]
    return result
