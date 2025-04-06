from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableMatchStats, TablePlayer, TableTeam


async def sync_player_tournaments(
    session: AsyncSession,
    player: TablePlayer,
) -> None:
    # Refresh the player to ensure relationships are in sync
    await session.refresh(player, attribute_names=["tournaments", "stats", "team"])

    # Find all matches the player is associated with (via stats or team membership)
    matches_query = (
        select(TableMatch)
        .options(selectinload(TableMatch.tournament))
        .where(
            (TableMatch.stats.any(TableMatchStats.player_id == player.id))
            | (TableMatch.teams.any(TableTeam.players.any(TablePlayer.id == player.id)))
        )
    )
    matches = await session.execute(matches_query)
    match_list = matches.scalars().all()

    # Extract the tournaments from the matches
    tournaments = {match.tournament for match in match_list if match.tournament}

    # Update the player's tournaments list
    player.tournaments = list(tournaments)

    await session.commit()
