from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_tournament_by_name
from .schemes import TournamentCreate, TournamentGeneralInfoUpdate
from ravenspedia.core import TableTournament, TableTournamentResult, TournamentStatus


async def get_tournaments(session: AsyncSession) -> list[TableTournament]:
    """
    Retrieve all tournaments from the database with related data (players, teams, matches, results).
    """
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
            selectinload(TableTournament.results).selectinload(
                TableTournamentResult.team
            ),
        )
        .order_by(TableTournament.id)
    )
    tournaments = await session.scalars(stmt)
    return list(tournaments)


async def get_tournament(
    session: AsyncSession,
    tournament_name: str,
) -> TableTournament | None:
    """
    Retrieve a tournament by its name from the database.
    """
    tournament: TableTournament = await get_tournament_by_name(
        tournament_name=tournament_name,
        session=session,
    )
    return tournament


async def create_tournament(
    session: AsyncSession,
    tournament_in: TournamentCreate,
) -> TableTournament:
    """
    Create a new tournament in the database with the provided data.
    """
    current_time = datetime.now()

    # Determine the tournament status based on start and end dates
    if tournament_in.end_date < current_time:
        tournament_status = TournamentStatus.COMPLETED
    elif tournament_in.start_date > current_time:
        tournament_status = TournamentStatus.SCHEDULED
    else:
        tournament_status = TournamentStatus.IN_PROGRESS

    # Create a new tournament instance
    tournament: TableTournament = TableTournament(
        **tournament_in.model_dump(),
        status=tournament_status,
    )

    try:
        session.add(tournament)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tournament {tournament_in.name} already exists",
        )

    # Refresh the tournament with related data
    await session.refresh(
        tournament,
        attribute_names=["players", "teams", "matches", "results"],
    )
    return tournament


async def delete_tournament(
    session: AsyncSession,
    tournament: TableTournament,
) -> None:
    """
    Delete a tournament from the database.
    """
    await session.delete(tournament)
    await session.commit()


async def update_general_tournament_info(
    session: AsyncSession,
    tournament: TableTournament,
    tournament_update: TournamentGeneralInfoUpdate,
) -> TableTournament:
    """
    Update a tournament's general information (e.g., name, prize, description).
    """
    for class_field, value in tournament_update.model_dump(exclude_unset=True).items():
        setattr(tournament, class_field, value)
    await session.commit()

    return tournament
