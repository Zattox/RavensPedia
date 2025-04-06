from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableMatch, TableTeam, TableMatchStats
from ..match_stats import sync_player_tournaments


async def add_team_in_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> TableMatch:
    """
    Add a team to a match, with validation checks.
    """
    # Check if the team is already in the match
    if team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already exists",
        )

    # Check if the match has reached its maximum number of teams
    if len(match.teams) == match.max_number_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the match",
        )

    # Check if the tournament has reached its maximum number of teams
    if (team not in match.tournament.teams) and (
        len(match.tournament.teams) == match.tournament.max_count_of_teams
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the tournament",
        )

    # Add the team to the match
    match.teams.append(team)
    if not match.tournament in team.tournaments:
        team.tournaments.append(match.tournament)

    # Sync player tournaments for all players in the team
    for player in team.players:
        await sync_player_tournaments(session, player)

    await session.commit()
    return match


async def delete_team_from_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> TableMatch:
    """
    Remove a team from a match.
    """
    # Check if the team is in the match
    if not team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the match",
        )

    # Remove the team from the match
    match.teams.remove(team)

    # Sync player tournaments for all players in the team
    for player in team.players:
        await sync_player_tournaments(session, player)

    await session.commit()
    return match


async def delete_match_stats(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    """
    Delete all statistics associated with a match.
    """
    # Delete all match stats from the database
    await session.execute(
        delete(TableMatchStats).where(TableMatchStats.match_id == match.id)
    )
    await session.commit()
    await session.refresh(match)
    return match
