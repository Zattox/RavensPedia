from datetime import datetime
from typing import Optional, List

from fastapi import Query

from .schemes import PlayerStatsFilter


async def get_stats_filter(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    tournament_ids: Optional[List[int]] = Query(None),
    detailed: bool = False,
) -> PlayerStatsFilter:
    """
    Create a PlayerStatsFilter object from query parameters.
    """
    return PlayerStatsFilter(
        start_date=start_date,
        end_date=end_date,
        tournament_ids=tournament_ids,
        detailed=detailed,
    )
