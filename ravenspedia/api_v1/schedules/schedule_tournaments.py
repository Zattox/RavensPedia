from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableTournament
from ravenspedia.core.project_models.table_tournament import TournamentStatus


async def get_last_x_completed_tournaments(
    session: AsyncSession,
    num_tournaments: int,
) -> list[TableTournament]:
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        )
        .filter(TableTournament.status == TournamentStatus.COMPLETED)
        .order_by(TableTournament.end_date.desc())
        .limit(num_tournaments)
    )
    response = await session.execute(stmt)
    tournaments = response.scalars().all()

    return list(tournaments)


async def get_upcoming_tournaments(
    session: AsyncSession,
    num_tournaments: int,
) -> list[TableTournament]:
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        )
        .filter(TableTournament.status == TournamentStatus.SCHEDULED)
        .filter(TableTournament.start_date >= datetime.now())
        .order_by(TableTournament.end_date.asc())
        .limit(num_tournaments)
    )

    response = await session.execute(stmt)
    tournaments = response.scalars().all()

    return list(tournaments)


async def get_in_progress_tournaments(
    session: AsyncSession,
) -> list[TableTournament]:
    current_time = datetime.now()
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        )
        .filter(TableTournament.status == TournamentStatus.IN_PROGRESS)
        .filter(TableTournament.start_date <= current_time)
        .filter(TableTournament.end_date >= current_time)
    )

    response = await session.execute(stmt)
    tournaments = response.scalars().all()

    return list(tournaments)
