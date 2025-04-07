from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import (
    TableTournament,
    TableTeam,
    TeamTournamentAssociation,
    PlayerTournamentAssociation,
    TableTournamentResult,
)
from .schemes import TournamentResult


async def add_team_in_tournament(
    session: AsyncSession,
    team: TableTeam,
    tournament: TableTournament,
) -> TableTournament:
    """
    Add a team to a tournament, including its players.
    """
    # Check: the team is already participating in the tournament
    if team in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already exists",
        )

    # Check: the maximum number of teams has been reached
    if len(tournament.teams) == tournament.max_count_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the tournament",
        )

    # Add the team and all its players to the tournament
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
    """
    Remove a team from a tournament, including its players.
    """
    # Check: the team is not participating in the tournament
    if team not in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the tournament {tournament.name}",
        )

    # Remove the association between the team and the tournament
    await session.execute(
        delete(TeamTournamentAssociation).where(
            TeamTournamentAssociation.team_id == team.id,
            TeamTournamentAssociation.tournament_id == tournament.id,
        )
    )

    # Remove all players of the team from the tournament
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
    """
    Add a result to a tournament.
    """
    # Check: the place is already taken in the tournament results
    if any(r.place == result.place for r in tournament.results):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Place {result.place} is already taken in the tournament results",
        )

    # Check: cannot add more results than the maximum number of teams
    if len(tournament.results) >= tournament.max_count_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add more results than max_count_of_teams ({tournament.max_count_of_teams})",
        )

    # Create and add a new result
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
    """
    Delete the last result (highest place) from a tournament.
    """
    # Check: there are no results to delete
    if not tournament.results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No results to delete",
        )

    # Find and delete the result with the highest place
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
    """
    Assign a team to a specific place in a tournament's results.
    """
    # Check: the team is not participating in the tournament
    if team not in tournament.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} is not participating in the tournament",
        )

    # Find the result by place
    result = next((r for r in tournament.results if r.place == place), None)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result for place {place} not found",
        )

    # Check: the team already has a result in the tournament
    if any(r.team == team for r in tournament.results if r.place != place):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already has a result in this tournament",
        )

    # Assign the team to the specified place
    result.team = team
    await session.commit()
    await session.refresh(tournament, ["results"])
    return tournament


async def remove_team_from_result(
    session: AsyncSession,
    tournament: TableTournament,
    place: int,
) -> TableTournament:
    """
    Remove a team from a specific place in a tournament's results.
    """
    # Find the result by place
    result = next((r for r in tournament.results if r.place == place), None)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Result for place {place} not found",
        )

    # Remove the team from the result
    result.team = None
    await session.commit()
    await session.refresh(tournament, ["results"])
    return tournament
