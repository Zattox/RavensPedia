from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import db_helper, TableTeam, TableMatch, TableTournamentResult


async def get_team_by_id(
    team_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTeam:
    """
    Retrieve a team from the database by its ID.
    """
    # Query the team with the given ID and eagerly load related data
    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.id == team_id)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.map_stats),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.team
            ),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.tournament
            ),
        ),
    )

    # Check if the team exists; if not, raise a 404 error
    if table_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_id} not found",
        )

    return table_team


async def get_team_by_name(
    team_name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTeam | None:
    """
    Retrieve a team from the database by its name.
    """
    # If the team name is None, return None (used in optional dependencies)
    if team_name is None:
        return None

    # Query the team with the given name and eagerly load related data
    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.name == team_name)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches).selectinload(TableMatch.result),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.map_stats),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.team
            ),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.tournament
            ),
        ),
    )

    # Check if the team exists; if not, raise a 404 error
    if table_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_name} not found",
        )

    return table_team
