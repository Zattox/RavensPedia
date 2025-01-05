from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.faceit_models import MatchInfo


# A function for create a MatchInfo in the database
async def create_match_info(
    session: AsyncSession,
    match_info_create: MatchInfo,
) -> MatchInfo:
    session.add(match_info_create)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(match_info_create)
    return match_info_create


# A function for getting a Match by its id from the database
async def get_match_info(
    session: AsyncSession,
    match_info_id: int,
) -> MatchInfo | None:
    return await session.get(MatchInfo, match_info_id)


async def get_matches_info(session: AsyncSession) -> list[MatchInfo]:
    statement = select(MatchInfo).order_by(MatchInfo.faceit_match_id)
    result: Result = await session.execute(statement)
    matches = result.scalars().all()
    return list(matches)


# A function for delete a Match from the database
async def delete_match_info(
    session: AsyncSession,
    match_info: MatchInfo,
) -> None:
    await session.delete(match_info)
    await session.commit()  # Make changes to the database
