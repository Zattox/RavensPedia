from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import TableMatch, TableMatchStats, MatchStatus
from .helpers import sync_player_tournaments
from .schemes import MatchStatsInput
from .. import get_player_by_nickname


async def add_manual_match_stats(
    session: AsyncSession,
    stats_input: MatchStatsInput,
    match: TableMatch,
) -> TableMatch:
    # Update the match status to COMPLETED if it isn't already
    if match.status != MatchStatus.COMPLETED:
        match = await manual_update_match_status(
            match=match,
            new_status=MatchStatus.COMPLETED,
            session=session,
        )

    # Find the player in the database
    player = await get_player_by_nickname(
        player_nickname=stats_input.nickname,
        session=session,
    )

    # Prepare the stats data
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

    # Create and add the new stats entry
    round_player_stats = TableMatchStats(
        player=player,
        match=match,
        match_stats=stats_data,
    )
    session.add(round_player_stats)

    # Commit the stats to the database
    await session.flush()
    await session.commit()

    # Now sync the player's tournaments
    await sync_player_tournaments(session=session, player=player)

    return match


async def delete_last_statistic_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    """
    Delete the last statistic from a match.
    """
    # If the stats list is empty, return the match as is
    if not match.stats:
        return match

    # Remove the last stat entry
    match.stats.pop()
    await session.commit()
    await session.refresh(match)
    return match
