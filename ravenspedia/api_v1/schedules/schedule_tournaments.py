from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableTournament, TableTournamentResult
from ravenspedia.core.project_models.table_tournament import TournamentStatus


async def get_last_x_completed_tournaments(
    session: AsyncSession,
) -> list[TableTournament]:
    """Retrieve completed tournaments, ordered by end date in descending order."""
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
        .filter(TableTournament.status == TournamentStatus.COMPLETED)
        .order_by(TableTournament.end_date.desc())  # Sort by end date, latest first
    )
    response = await session.execute(stmt)
    tournaments = response.scalars().all()
    return list(tournaments)


async def get_upcoming_tournaments(session: AsyncSession) -> list[TableTournament]:
    """Retrieve scheduled tournaments with future start dates, ordered by end date ascending."""
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
        .filter(TableTournament.status == TournamentStatus.SCHEDULED)
        .order_by(TableTournament.end_date.asc())  # Sort by end date, earliest first
    )
    response = await session.execute(stmt)
    tournaments = response.scalars().all()
    return list(tournaments)


async def get_in_progress_tournaments(session: AsyncSession) -> list[TableTournament]:
    """Retrieve tournaments currently in progress, filtered by current time range."""
    current_time = datetime.now()
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
        .filter(TableTournament.status == TournamentStatus.IN_PROGRESS)
        .order_by(
            TableTournament.start_date.asc()
        )  # Sort by start date, earliest first
    )
    response = await session.execute(stmt)
    tournaments = response.scalars().all()
    return list(tournaments)
