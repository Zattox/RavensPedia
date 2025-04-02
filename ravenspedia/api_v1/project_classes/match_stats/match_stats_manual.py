from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.api_v1.project_classes.match_stats.helpers import sync_player_tournaments
from ravenspedia.api_v1.project_classes.match_stats.schemes import MatchStatsInput
from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import TableMatch, TablePlayer, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def add_manual_match_stats(
    session: AsyncSession,
    stats_input: MatchStatsInput,
    match: TableMatch,
) -> TableMatch:
    if match.status != MatchStatus.COMPLETED:
        match = await manual_update_match_status(
            match.id,
            MatchStatus.COMPLETED,
            session,
        )

    player_result = await session.execute(
        select(TablePlayer).where(TablePlayer.nickname == stats_input.nickname)
    )
    player = player_result.scalars().first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with nickname {stats_input.nickname} not found",
        )

    stats_data = {
        "nickname": stats_input.nickname,
        "round_of_match": stats_input.round_of_match,
        "match_id": match.id,
        "map": stats_input.map,
        "Result": stats_input.result,
        "Kills": stats_input.kills,
        "Assists": stats_input.assists,
        "Deaths": stats_input.deaths,
        "ADR": stats_input.adr,
        "Headshots %": stats_input.headshots_percentage,
    }

    round_player_stats = TableMatchStats(
        player=player,
        match=match,
        match_stats=stats_data,
    )
    session.add(round_player_stats)
    await sync_player_tournaments(session, player)

    await session.flush()
    await session.commit()

    return match

async def delete_last_statistic_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    if not match.stats:
        return match

    match.stats.pop()
    await session.commit()
    await session.refresh(match)
    return match