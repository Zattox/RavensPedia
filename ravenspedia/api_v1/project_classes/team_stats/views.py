from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TableTeam
from ravenspedia.core.project_models.table_team_stats import TableTeamMapStats
from .crud import get_team_map_stats
from .schemes import ResponseTeamMapStats
from ..team.dependencies import get_team_by_name

router = APIRouter(tags=["Team Stats"])


def table_to_response_form(
    map_stats: TableTeamMapStats,
) -> ResponseTeamMapStats:
    result = ResponseTeamMapStats(
        map=map_stats.map,
        matches_won=map_stats.matches_won,
        matches_played=map_stats.matches_played,
        win_rate=map_stats.win_rate,
    )

    return result


@router.get(
    "/{team_name}/",
    response_model=List[ResponseTeamMapStats],
    status_code=status.HTTP_200_OK,
)
async def get_team_stats(
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> List[ResponseTeamMapStats]:
    team_stats = await get_team_map_stats(
        session=session,
        team=team,
    )
    result = [table_to_response_form(map_name) for map_name in team_stats]
    return result
