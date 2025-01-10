from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import table_to_response_form
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate

from core import TableMatch, TableTournament, TableTeam, TablePlayer


async def add_team_in_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> ResponseTournament:
    if team in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already exists",
        )

    if len(tournament.teams) == tournament.max_count_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the tournament",
        )

    tournament.teams.append(team)
    for player in team.players:
        tournament.players.append(player)

    await session.commit()

    return table_to_response_form(tournament=tournament)


async def delete_team_from_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> ResponseTournament:
    if not team in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the tournament {tournament.name}",
        )

    tournament.teams.remove(team)
    for player in team.players:
        tournament.players.remove(player)

    await session.commit()

    return table_to_response_form(tournament=tournament)
