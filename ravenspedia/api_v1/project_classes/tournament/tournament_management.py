from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.tournament.schemes import TournamentResult
from ravenspedia.core import (
    TableTournament,
    TableTeam,
    TeamTournamentAssociation,
    PlayerTournamentAssociation,
    TableTournamentResult,
)


async def add_team_in_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> TableTournament:
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

    return tournament


async def delete_team_from_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> TableTournament:
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

    return tournament


async def add_result_to_tournament(
    session: AsyncSession,
    tournament: TableTournament,
    result: TournamentResult,
) -> TableTournament:
    if any(r.place == result.place for r in tournament.results):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Place {result.place} is already taken in the tournament results",
        )

    if len(tournament.results) >= tournament.max_count_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add more results than max_count_of_teams ({tournament.max_count_of_teams})",
        )

    new_result = TableTournamentResult(
        place=result.place,
        prize=result.prize,
        tournament_id=tournament.id,
    )

    session.add(new_result)
    await session.commit()
    await session.refresh(tournament, ["results"])

    return tournament

async def delete_last_result(
    session: AsyncSession,
    tournament: TableTournament,
) -> TableTournament:
    if not tournament.results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No results to delete",
        )

    last_result = max(tournament.results, key=lambda x: x.place)

    await session.delete(last_result)
    await session.commit()
    await session.refresh(tournament, ["results"])

    return tournament

async def assign_team_to_result(
    session: AsyncSession,
    tournament: TableTournament,
    place: int,
    team: TableTeam,
) -> TableTournament:
    if team not in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} is not participating in the tournament",
        )

    result = next((r for r in tournament.results if r.place == place), None)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result for place {place} not found",
        )

    if any(r.team == team for r in tournament.results if r.place != place):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already has a result in this tournament",
        )

    result.team = team
    await session.commit()
    await session.refresh(tournament, ["results"])
    return tournament

async def remove_team_from_result(
    session: AsyncSession,
    tournament: TableTournament,
    place: int,
) -> TableTournament:
    result = next((r for r in tournament.results if r.place == place), None)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result for place {place} not found",
        )

    result.team = None
    await session.commit()
    await session.refresh(tournament, ["results"])

    return tournament
