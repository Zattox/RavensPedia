from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.api_v1.project_classes import ResponseMatch
from ravenspedia.api_v1.project_classes.match.crud import table_to_response_form
from ravenspedia.core import TableMatch, TableMatchStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def get_last_x_completed_matches(
    session: AsyncSession,
    num_matches: int,
) -> list[ResponseMatch]:
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        )
        .filter(TableMatch.status == MatchStatus.COMPLETED)
        .order_by(TableMatch.date.desc())
        .limit(num_matches)
    )
    response = await session.execute(stmt)
    matches = response.scalars().all()

    result = [table_to_response_form(match) for match in matches]
    return result


async def get_upcoming_matches(
    session: AsyncSession,
    num_matches: int,
) -> list[ResponseMatch]:
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        )
        .filter(TableMatch.status == MatchStatus.SCHEDULED)
        .filter(TableMatch.date >= datetime.now())
        .order_by(TableMatch.date.asc())
        .limit(num_matches)
    )

    response = await session.execute(stmt)
    matches = response.scalars().all()

    result = [table_to_response_form(match) for match in matches]
    return result


async def get_in_progress_matches(
    session: AsyncSession,
) -> list[ResponseMatch]:
    current_time = datetime.now()
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        )
        .filter(TableMatch.status == MatchStatus.IN_PROGRESS)
        .filter(TableMatch.date <= current_time)
    )

    response = await session.execute(stmt)
    matches = response.scalars().all()

    result = [table_to_response_form(match) for match in matches]
    return result
