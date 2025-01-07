from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from . import crud
from core import db_helper


# A function for get a Tournament from the database by id
async def get_tournament_by_id(
    tournament_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    tournament = await crud.get_tournament(session=session, tournament_id=tournament_id)
    # If such an id does not exist, then throw an exception.
    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tournament {tournament_id} not found",
        )
    return tournament
