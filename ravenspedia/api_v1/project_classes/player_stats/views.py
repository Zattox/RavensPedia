from typing import Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TablePlayer
from . import crud
from .dependencies import get_stats_filter
from .schemes import PlayerStatsFilter, GeneralPlayerStats, DetailedPlayerStats
from ..player.dependencies import get_player_by_nickname

router = APIRouter(tags=["Players Stats"])


@router.get(
    "/{player_nickname}/",
    response_model=Union[GeneralPlayerStats, DetailedPlayerStats],
    status_code=status.HTTP_200_OK,
)
async def get_player_stats(
    player: TablePlayer = Depends(get_player_by_nickname),
    stats_filter: PlayerStatsFilter = Depends(get_stats_filter),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Union[GeneralPlayerStats, DetailedPlayerStats]:
    """
    Retrieve a player's statistics by their nickname.
    """
    stats = await crud.get_player_stats(player, stats_filter, session)
    return stats
