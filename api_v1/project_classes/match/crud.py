from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.project_models import Match
from api_v1.project_classes.match.schemes import MatchCreate, MatchUpdatePartial


# A function to get all the Matches from the database
async def get_matches(session: AsyncSession) -> list[Match]:
    statement = select(Match).order_by(Match.id)
    result: Result = await session.execute(statement)
    matches = result.scalars().all()
    return list(matches)


# A function for getting a Match by its id from the database
async def get_match(
    session: AsyncSession,
    match_id: int,
) -> Match | None:
    return await session.get(Match, match_id)


# A function for create a Match in the database
async def create_match(
    session: AsyncSession,
    match_in: MatchCreate,
) -> Match:
    # Turning it into a Match class without Mapped fields
    match = Match(**match_in.model_dump())
    session.add(match)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(match)
    return match


# A function for partial update a Match in the database
async def update_match_partial(
    session: AsyncSession,
    match: Match,
    match_update: MatchUpdatePartial,
) -> Match:
    for name, value in match_update.model_dump(exclude_unset=True).items():
        setattr(match, name, value)
    await session.commit()  # Make changes to the database
    return match


# A function for delete a Match from the database
async def delete_match(
    session: AsyncSession,
    match: Match,
) -> None:
    await session.delete(match)
    await session.commit()  # Make changes to the database
