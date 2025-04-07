from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableTeam, TableTeamMapStats, MapName


async def get_team_map_stats(
    session: AsyncSession,
    team: TableTeam,
) -> List[TableTeamMapStats]:
    """
    Retrieve and calculate map statistics for a team based on its matches.
    """
    # Get all matches and their results for the team
    matches = team.matches
    map_results = [info for match in matches for info in match.result]

    # Initialize a dictionary to store stats for each map
    stats_dict = {
        map_name: {
            "matches_played": 0,
            "matches_won": 0,
            "win_rate": 0.0,
        }
        for map_name in MapName
    }

    # Calculate matches played and won for each map based on match results
    for result in map_results:
        map_name = result.map
        stats_dict[map_name]["matches_played"] += 1
        # Check if the team won the match on this map
        if (
            result.first_team == team.name
            and result.total_score_first_team > result.total_score_second_team
        ) or (
            result.second_team == team.name
            and result.total_score_second_team > result.total_score_first_team
        ):
            stats_dict[map_name]["matches_won"] += 1

    # Calculate the win rate for each map
    for map_name, stat in stats_dict.items():
        if stat["matches_played"] > 0:
            stat["win_rate"] = (stat["matches_won"] / stat["matches_played"]) * 100

    # Update the existing map stats in the database
    for map_name, stat in stats_dict.items():
        existing_stat = await session.scalar(
            select(TableTeamMapStats).where(
                TableTeamMapStats.team_id == team.id,
                TableTeamMapStats.map == map_name,
            )
        )
        # Update the fields of the existing map stats
        setattr(existing_stat, "matches_played", stat["matches_played"])
        setattr(existing_stat, "matches_won", stat["matches_won"])
        setattr(existing_stat, "win_rate", stat["win_rate"])

    await session.commit()

    return team.map_stats


async def delete_team_map_stats(
    session: AsyncSession,
    team: TableTeam,
    map_stats: TableTeamMapStats,
):
    """
    Delete a specific map stats entry from a team.
    """
    # Check if the map stats entry belongs to the team
    if map_stats not in team.map_stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The map_stats is no longer exists in the team {team.name}",
        )

    # Remove the map stats entry from the team and clear its team association
    team.map_stats.remove(map_stats)
    map_stats.team_id = None
    map_stats.team = None

    await session.commit()

    return team
