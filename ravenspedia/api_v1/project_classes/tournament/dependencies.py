from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from ravenspedia.core import db_helper, TableTournament


# A function for get a Tournament from the database by id
async def get_tournament_by_id(
    tournament_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTournament:
    table_tournament = await session.scalar(
        select(TableTournament)
        .where(TableTournament.id == tournament_id)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        ),
    )
    # If such an id does not exist, then throw an exception.
    if table_tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament {tournament_id} not found",
        )

    return table_tournament


async def get_tournament_by_name(
    tournament_name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTournament:
    table_tournament = await session.scalar(
        select(TableTournament)
        .where(TableTournament.name == tournament_name)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if table_tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament {tournament_name} not found",
        )

    return table_tournament
