from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import db_helper, TableTeam, TableMatch, TableTournamentResult


# A function for get a Team from the database by id
async def get_team_by_id(
    team_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTeam:
    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.id == team_id)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.map_stats),
            selectinload(TableTeam.tournament_results).selectinload(TableTournamentResult.team),
            selectinload(TableTeam.tournament_results).selectinload(TableTournamentResult.tournament),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if table_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_id} not found",
        )

    return table_team


# A function for get a Team from the database by id
async def get_team_by_name(
    team_name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTeam | None:
    if team_name is None:
        return None

    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.name == team_name)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches).selectinload(TableMatch.result),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.map_stats),
            selectinload(TableTeam.tournament_results).selectinload(TableTournamentResult.team),
            selectinload(TableTeam.tournament_results).selectinload(TableTournamentResult.tournament),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if table_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team {team_name} not found",
        )

    return table_team
