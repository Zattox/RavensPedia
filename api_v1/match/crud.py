from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.match.scheme import MatchCreate, MatchUpdatePartial
from core.models import Match


async def get_matches(
    session: AsyncSession,
) -> list[Match]:
    stat = select(Match).order_by(Match.id)
    result: Result = await session.execute(stat)
    matches = result.scalars().all()
    return list(matches)


async def get_match(
    session: AsyncSession,
    match_id: int,
) -> Match | None:
    return await session.get(Match, match_id)


async def create_match(
    session: AsyncSession,
    match_in: MatchCreate,
) -> Match:
    match = Match(**match_in.model_dump())
    session.add(match)
    await session.commit()
    # await session.refresh(match)
    return match


async def update_match_partial(
    session: AsyncSession,
    match: Match,
    match_update: MatchUpdatePartial,
) -> Match:
    for name, value in match_update.model_dump(exclude_unset=True).items():
        setattr(match, name, value)
    await session.commit()
    return match


async def delete_match(
    session: AsyncSession,
    match: Match,
) -> None:
    await session.delete(match)
    await session.commit()
