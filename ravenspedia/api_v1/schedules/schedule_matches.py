from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def get_completed_matches(
    session: AsyncSession,
) -> list[TableMatch]:
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
        .order_by(TableMatch.date.desc())
    )
    response = await session.execute(stmt)
    matches = response.scalars().all()
    return list(matches)


async def get_upcoming_matches(
    session: AsyncSession,
) -> list[TableMatch]:
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
        .filter(TableMatch.date >= datetime.now())
        .order_by(TableMatch.date.asc())
    )

    response = await session.execute(stmt)
    matches = response.scalars().all()
    return list(matches)


async def get_in_progress_matches(
    session: AsyncSession,
) -> list[TableMatch]:
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
        .filter(TableMatch.date <= current_time)
    )

    response = await session.execute(stmt)
    matches = response.scalars().all()

    return list(matches)
