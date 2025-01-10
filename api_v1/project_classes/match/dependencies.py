from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from core import db_helper, TableMatch


# A function for get a match from the database by id
async def get_match_by_id(
    match_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableMatch:
    match = await session.scalar(
        select(TableMatch)
        .where(TableMatch.id == match_id)
        .options(
            selectinload(TableMatch.players),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} not found",
        )

    return match
