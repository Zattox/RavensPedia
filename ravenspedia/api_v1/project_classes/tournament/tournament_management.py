from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import (
    TableTournament,
    TableTeam,
    TeamTournamentAssociation,
    PlayerTournamentAssociation,
)
from .crud import table_to_response_form
from .schemes import ResponseTournament


async def add_team_in_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> ResponseTournament:
    if team in tournament.teams:
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
    if team not in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the tournament {tournament.name}",
        )

    await session.execute(
        delete(TeamTournamentAssociation).where(
            TeamTournamentAssociation.team_id == team.id,
            TeamTournamentAssociation.tournament_id == tournament.id,
        )
    )

    player_ids = [player.id for player in team.players]
    if player_ids:
        await session.execute(
            delete(PlayerTournamentAssociation).where(
                PlayerTournamentAssociation.tournament_id == tournament.id,
                PlayerTournamentAssociation.player_id.in_(player_ids),
            )
        )

    await session.commit()
    await session.refresh(tournament, ["matches", "teams", "players"])

    return table_to_response_form(tournament=tournament)
