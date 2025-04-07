from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatchStats, TableMatch, TablePlayer
from .schemes import (
    PlayerStatsFilter,
    GeneralPlayerStats,
    DetailedPlayerStats,
    GENERAL_STATS_MAPPING,
    DETAILED_STATS_MAPPING,
)


async def get_player_stats(
    player: TablePlayer,
    stats_filter: PlayerStatsFilter,
    session: AsyncSession,
) -> GeneralPlayerStats | DetailedPlayerStats:
    """
    Retrieve a player's statistics based on the provided filter.
    """
    # Build the query to fetch match stats for the player
    stmt = (
        select(TableMatchStats)
        .join(TableMatchStats.match)
        .where(TableMatchStats.player_id == player.id)
        .options(
            selectinload(TableMatchStats.match).selectinload(TableMatch.tournament)
        )
    )

    # Apply filters if provided
    if stats_filter.start_date:
        stmt = stmt.where(TableMatch.date >= stats_filter.start_date)
    if stats_filter.end_date:
        stmt = stmt.where(TableMatch.date <= stats_filter.end_date)
    if stats_filter.tournament_ids:
        stmt = stmt.where(TableMatch.tournament_id.in_(stats_filter.tournament_ids))

    # Execute the query and fetch the stats
    stats_records = await session.scalars(stmt)
    stats_list = list(stats_records.all())

    # Process the stats based on the detailed flag
    if stats_filter.detailed:
        return process_detailed_stats(player, stats_list)
    else:
        return process_general_stats(player, stats_list)


def process_general_stats(
    player: TablePlayer,
    stats_list: List[TableMatchStats],
) -> GeneralPlayerStats:
    """
    Process a player's general statistics from a list of match stats.
    """
    # Initialize the result with the player's nickname and total matches
    result = GeneralPlayerStats(
        nickname=player.nickname,
        total_matches=len(stats_list),
    )

    # Aggregate stats from each match
    for stat in stats_list:
        stats_data = stat.match_stats
        for stats_field, result_field in GENERAL_STATS_MAPPING.items():
            value = stats_data.get(stats_field, 0)
            current_value = getattr(result, result_field)
            if value is None:
                value = 0
            if current_value is None:
                current_value = 0
            setattr(result, result_field, current_value + value)

    # Calculate averages and ratios if there are stats
    if stats_list:
        result.adr /= len(stats_list)
        result.kpr /= len(stats_list)
        result.win_rate = (
            (result.wins / result.total_matches) * 100 if result.total_matches else 0
        )
        result.kd_ratio = result.kills / result.deaths if result.deaths else 0
        result.headshots_rate = (
            (result.headshots / result.kills) * 100 if result.kills else 0
        )

    return result


def process_detailed_stats(
    player: TablePlayer,
    stats_list: List[TableMatchStats],
) -> DetailedPlayerStats:
    """
    Process a player's detailed statistics from a list of match stats.
    """
    # Initialize the result with the player's nickname and total matches
    result = DetailedPlayerStats(
        nickname=player.nickname,
        total_matches=len(stats_list),
    )

    # Aggregate stats from each match
    for stat in stats_list:
        stats_data = stat.match_stats
        for stats_field, result_field in DETAILED_STATS_MAPPING.items():
            value = stats_data.get(stats_field, 0)
            current_value = getattr(result, result_field)
            if value is None:
                value = 0
            if current_value is None:
                current_value = 0
            setattr(result, result_field, current_value + value)

    # Calculate averages, ratios, and percentages if there are stats
    if stats_list:
        result.adr = (
            sum(stat.match_stats.get("ADR", 0) for stat in stats_list)
            / result.total_matches
        )
        result.kd = result.kills / result.deaths if result.deaths else 0
        result.kpr = (
            sum(stat.match_stats.get("K/R Ratio", 0) for stat in stats_list)
            / result.total_matches
        )

        result.headshots_percentage = (
            (result.headshots / result.kills) * 100 if result.kills else 0
        )

        result.match_1v1_win_rate = (
            (result.wins_1v1 / result.count_1v1) * 100 if result.count_1v1 else 0
        )
        result.match_1v2_win_rate = (
            (result.wins_1v2 / result.count_1v2) * 100 if result.count_1v2 else 0
        )

        result.match_entry_rate = (
            (result.entry_count / result.total_matches) if result.total_matches else 0
        )
        result.match_entry_success_rate = (
            (result.entry_wins / result.entry_count) * 100 if result.entry_count else 0
        )

        result.utility_usage_per_round = (
            sum(
                stat.match_stats.get("Utility Usage per Round", 0)
                for stat in stats_list
            )
            / result.total_matches
        )
        result.utility_damage_per_round_in_a_match = (
            sum(
                stat.match_stats.get("Utility Damage per Round in a Match", 0)
                for stat in stats_list
            )
            / result.total_matches
        )
        result.utility_successes_rate_per_match = (
            (result.utility_successes / result.utility_count) * 100
            if result.utility_count
            else 0
        )
        result.flash_success_rate_per_match = (
            (result.flash_successes / result.flash_count) * 100
            if result.flash_count
            else 0
        )
        result.flashes_per_round_in_a_match = (
            sum(
                stat.match_stats.get("Flashes per Round in a Match", 0)
                for stat in stats_list
            )
            / result.total_matches
        )
        result.enemies_flashed_per_round_in_a_match = (
            sum(
                stat.match_stats.get("Enemies Flashed per Round in a Match", 0)
                for stat in stats_list
            )
            / result.total_matches
        )

    return result
