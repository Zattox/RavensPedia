from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.faceit_models import MatchInfo
from core.faceit_models.round_info import RoundInfo


# A function for create a MatchInfo in the database
async def create_match_info(
    session: AsyncSession,
    data: list[RoundInfo],
) -> MatchInfo:
    match_info = MatchInfo(
        faceit_match_id=data[0].match_id,
        rounds=data,
    )
    session.add(match_info)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(match_info_create)
    return match_info


# A function for getting a Match by its id from the database
async def get_match_info(
    session: AsyncSession,
    match_info_id: int,
) -> MatchInfo | None:
    return await session.get(MatchInfo, match_info_id)


async def get_matches_info(session: AsyncSession) -> list[MatchInfo]:
    statement = select(MatchInfo).order_by(MatchInfo.id)
    result: Result = await session.execute(statement)
    matches = result.scalars().all()
    return list(matches)


async def update_match_info(
    session: AsyncSession,
    match_info: MatchInfo,
    match_info_update: MatchInfo,
) -> MatchInfo:
    for name, value in match_info_update.model_dump().items():
        setattr(match_info, name, value)
    await session.commit()  # Make changes to the database
    return match_info


# A function for delete a Match from the database
async def delete_match_info(
    session: AsyncSession,
    match_info: MatchInfo,
) -> None:
    await session.delete(match_info)
    await session.commit()  # Make changes to the database
