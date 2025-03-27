from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.match_stats.schemes import MatchStatsInput
from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import TableMatch, TablePlayer, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def add_manual_match_stats(
    session: AsyncSession,
    stats_input: MatchStatsInput,
    match_id: int,
) -> TableMatch:
    # Получаем матч
    result = await session.execute(select(TableMatch).filter_by(id=match_id))
    match = result.scalars().first()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found",
        )

    # Проверяем наличие статистики (асинхронно)
    stats_result = await session.execute(
        select(TableMatchStats).filter_by(match_id=match_id)
    )
    existing_stats = stats_result.scalars().first()

    if existing_stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics have already been added to the match {match.id}",
        )

    if stats_input.best_of != match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The best_of field differs from the specified one. Needed {match.best_of}, but passed {stats_input.best_of}",
        )

    # Обновляем статус матча
    match = await manual_update_match_status(
        match.id,
        MatchStatus.COMPLETED,
        session,
    )

    # Добавляем статистику игроков
    for player_stats in stats_input.stats:
        # Ищем игрока
        player_result = await session.execute(
            select(TablePlayer).filter_by(nickname=player_stats.nickname)
        )
        player = player_result.scalars().first()

        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Player with nickname {player_stats.nickname} not found",
            )

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
            player=player,
            match=match,
            match_stats=stats_data,
        )
        session.add(round_player_stats)

    await session.flush()
    await session.commit()

    return match
