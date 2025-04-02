from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableMatchStats, TablePlayer, TableTeam


async def sync_player_tournaments(session: AsyncSession, player: TablePlayer) -> None:
    stmt = (
        select(TablePlayer)
        .options(selectinload(TablePlayer.tournaments))
        .where(TablePlayer.id == player.id)
    )
    result = await session.execute(stmt)
    player_with_tournaments = result.scalars().first()

    matches = await session.execute(
        select(TableMatch).where(
            (TableMatch.stats.any(TableMatchStats.player_id == player.id)) |
            (TableMatch.teams.any(TableTeam.players.any(TablePlayer.id == player.id)))
        )
    )
    tournaments = {match.tournament for match in matches.scalars().all() if match.tournament}

    if player_with_tournaments:
        player_with_tournaments.tournaments = list(tournaments)
    else:
        player.tournaments = list(tournaments)