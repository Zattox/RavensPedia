from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableTournament
from .dependencies import get_tournament_by_id, get_tournament_by_name
from .schemes import TournamentCreate, TournamentGeneralInfoUpdate


# A function to get all the Tournaments from the database
async def get_tournaments(session: AsyncSession) -> list[TableTournament]:
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        )
        .order_by(TableTournament.id)
    )
    tournaments = await session.scalars(stmt)
    return list(tournaments)


# A function for getting a Tournament by its id from the database
async def get_tournament(
    session: AsyncSession,
    tournament_name: str,
) -> TableTournament | None:
    tournament: TableTournament = await get_tournament_by_name(
        tournament_name=tournament_name,
        session=session,
    )
    return tournament


# A function for create a Tournament in the database
async def create_tournament(
    session: AsyncSession,
    tournament_in: TournamentCreate,
) -> TableTournament:
    # Turning it into a Tournament class without Mapped fields
    tournament: TableTournament = TableTournament(**tournament_in.model_dump())

    try:
        session.add(tournament)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tournament {tournament_in.name} already exists",
        )

    return tournament


# A function for delete a Tournament from the database
async def delete_tournament(
    session: AsyncSession,
    tournament: TableTournament,
) -> None:
    await session.delete(tournament)
    await session.commit()  # Make changes to the database


# A function for partial update a Tournament in the database
async def update_general_tournament_info(
    session: AsyncSession,
    tournament: TableTournament,
    tournament_update: TournamentGeneralInfoUpdate,
) -> TableTournament:

    for class_field, value in tournament_update.model_dump(exclude_unset=True).items():
        setattr(tournament, class_field, value)
    await session.commit()  # Make changes to the database

    return tournament
