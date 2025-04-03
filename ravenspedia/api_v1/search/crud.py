from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ravenspedia.core import TablePlayer, TableTeam, TableTournament
from .schemes import SearchPlayer, SearchTeam, SearchTournament, SearchResult


async def search_entities(
    query: str,
    session: AsyncSession,
) -> SearchResult:
    query = query.lower()

    player_stmt = (select(TablePlayer)
    .options(selectinload(TablePlayer.team))
    .where(
        (TablePlayer.nickname.ilike(f"%{query}%"))
        | (TablePlayer.name.ilike(f"%{query}%"))
        | (TablePlayer.surname.ilike(f"%{query}%"))
    ))

    player_result = await session.execute(player_stmt)
    players = player_result.scalars().all()
    player_results = [
        SearchPlayer(
            nickname=player.nickname,
            name=player.name,
            surname=player.surname,
            team=player.team.name if player.team else None,
        )
        for player in players
    ]

    team_stmt = select(TableTeam).where(TableTeam.name.ilike(f"%{query}%"))
    team_result = await session.execute(team_stmt)
    teams = team_result.scalars().all()
    team_results = [
        SearchTeam(
            name=team.name,
            description=team.description,
        )
        for team in teams
    ]

    tournament_stmt = select(TableTournament).where(
        TableTournament.name.ilike(f"%{query}%")
    )
    tournament_result = await session.execute(tournament_stmt)
    tournaments = tournament_result.scalars().all()
    tournament_results = [
        SearchTournament(
            name=tournament.name,
            description=tournament.description,
        )
        for tournament in tournaments
    ]

    return SearchResult(
        players=player_results,
        teams=team_results,
        tournaments=tournament_results,
    )
