from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatchStats, TableMatch, TablePlayer
from .schemes import PlayerStatsFilter, GeneralPlayerStats, DetailedPlayerStats


async def get_player_stats(
    player: TablePlayer,
    stats_filter: PlayerStatsFilter,
    session: AsyncSession,
) -> GeneralPlayerStats | DetailedPlayerStats:
    stmt = (
        select(TableMatchStats)
        .join(TableMatchStats.match)
        .where(TableMatchStats.player_id == player.id)
        .options(
            selectinload(TableMatchStats.match).selectinload(TableMatch.tournament)
        )
    )

    if stats_filter.start_date:
        stmt = stmt.where(TableMatch.date >= stats_filter.start_date)
    if stats_filter.end_date:
        stmt = stmt.where(TableMatch.date <= stats_filter.end_date)
    if stats_filter.tournament_ids:
        stmt = stmt.where(TableMatch.tournament_id.in_(stats_filter.tournament_ids))

    stats_records = await session.scalars(stmt)
    stats_list = list(stats_records.all())

    if stats_filter.detailed:
        return process_detailed_stats(player, stats_list)
    else:
        return process_general_stats(player, stats_list)


def process_general_stats(
    player: TablePlayer,
    stats_list: List[TableMatchStats],
) -> GeneralPlayerStats:
    result = GeneralPlayerStats(
        nickname=player.nickname,
        total_matches=len(stats_list),
    )

    for stat in stats_list:
        stats_data = stat.match_stats
        result.wins += stats_data.get("Result", 0)
        result.kills += stats_data.get("Kills", 0)
        result.deaths += stats_data.get("Deaths", 0)
        result.assists += stats_data.get("Assists", 0)
        result.headshots += stats_data.get("Headshots", 0)
        result.adr += stats_data.get("ADR", 0)
        result.adr += stats_data.get("K/R Ratio", 0)

    if stats_list:
        result.adr /= len(stats_list)
        result.kpr /= len(stats_list)
        result.win_rate = result.wins / result.total_matches * 100
        result.kd_ratio = result.kills / result.deaths
        result.headshots_rate = result.headshots / result.kills * 100

    return result


def process_detailed_stats(
    player: TablePlayer,
    stats_list: List[TableMatchStats],
) -> DetailedPlayerStats:
    result = DetailedPlayerStats(
        nickname=player.nickname,
        total_matches=len(stats_list),
    )

    return result
