from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableMatch, TableTeam, TableMatchStats


async def add_team_in_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> TableMatch:

    if team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already exists",
        )

    if len(match.teams) == match.max_number_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the match",
        )

    match.teams.append(team)
    if not match.tournament in team.tournaments:
        team.tournaments.append(match.tournament)

    await session.commit()

    return match


async def delete_team_from_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> TableMatch:

    if not team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the match",
        )

    match.teams.remove(team)

    await session.commit()

    return match


async def delete_match_stats(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    await session.execute(
        delete(TableMatchStats).where(TableMatchStats.match_id == match.id)
    )
    await session.commit()
    await session.refresh(match)

    return match
