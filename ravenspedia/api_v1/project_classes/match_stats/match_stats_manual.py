from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.api_v1.project_classes.match_stats.schemes import MatchStatsInput
from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import TableMatch, TablePlayer, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def add_manual_match_stats(
    session: AsyncSession,
    stats_input: MatchStatsInput,
    match_id: int,
) -> TableMatch:
    result = await session.execute(
        select(TableMatch)
        .where(TableMatch.id == match_id)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        )
    )
    match = result.scalars().first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    stats_result = await session.execute(
        select(TableMatchStats).where(TableMatchStats.match_id == match_id)
    )
    if stats_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics have already been added to the match {match.id}",
        )

    if stats_input.best_of != match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The best_of field differs from the specified one. Needed {match.best_of}, but passed {stats_input.best_of}",
        )

    match = await manual_update_match_status(
        match.id,
        MatchStatus.COMPLETED,
        session,
    )

    nicknames = [p.nickname for p in stats_input.stats]
    players_result = await session.execute(
        select(TablePlayer).where(TablePlayer.nickname.in_(nicknames))
    )
    players = {p.nickname: p for p in players_result.scalars().all()}

    missing_players = [
        p.nickname for p in stats_input.stats if p.nickname not in players
    ]
    if missing_players:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Players not found: {', '.join(missing_players)}",
        )

    for player_stats in stats_input.stats:
        stats_data = {
            "nickname": player_stats.nickname,
            "round_of_match": player_stats.round_of_match,
            "match_id": match_id,
            "map": player_stats.map,
            "Result": player_stats.result,
            "Kills": player_stats.kills,
            "Assists": player_stats.assists,
            "Deaths": player_stats.deaths,
            "ADR": player_stats.adr,
            "Headshots %": player_stats.headshots_percentage,
        }

        round_player_stats = TableMatchStats(
            player=players[player_stats.nickname],
            match=match,
            match_stats=stats_data,
        )
        session.add(round_player_stats)

    await session.flush()
    await session.commit()

    return match
