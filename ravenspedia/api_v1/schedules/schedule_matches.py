from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def get_completed_matches(session: AsyncSession) -> list[TableMatch]:
    """Retrieve all completed matches, ordered by date in descending order."""
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        )
        .filter(TableMatch.status == MatchStatus.COMPLETED)
        .order_by(TableMatch.date.desc())  # Sort by date, latest first
    )
    response = await session.execute(stmt)
    matches = response.scalars().all()
    return list(matches)


async def get_upcoming_matches(session: AsyncSession) -> list[TableMatch]:
    """Retrieve upcoming scheduled matches with future dates, ordered by date ascending."""
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        )
        .filter(TableMatch.status == MatchStatus.SCHEDULED)
        .order_by(TableMatch.date.asc())  # Sort by date, earliest first
    )
    response = await session.execute(stmt)
    matches = response.scalars().all()
    return list(matches)


# Retrieve in-progress matches
async def get_in_progress_matches(session: AsyncSession) -> list[TableMatch]:
    """Retrieve matches currently in progress, filtered by current time."""
    current_time = datetime.now()
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        )
        .filter(TableMatch.status == MatchStatus.IN_PROGRESS)
        .order_by(TableMatch.date.asc())  # Sort by date, earliest first
    )
    response = await session.execute(stmt)
    matches = response.scalars().all()
    return list(matches)
