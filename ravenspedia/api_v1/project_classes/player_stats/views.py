from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TablePlayer
from .crud import get_player_stats
from .dependencies import get_stats_filter
from .schemes import PlayerStatsFilter
from ..player.crud import get_player_by_id
from ..player.dependencies import get_player_by_nickname

router = APIRouter(tags=["Players Stats"])


@router.get("/{player_nickname}/")
async def get_player_stats(
    player: TablePlayer = Depends(get_player_by_nickname),
    stats_filter: PlayerStatsFilter = Depends(get_stats_filter),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    stats = await get_player_stats(player, stats_filter, session)
    return stats
