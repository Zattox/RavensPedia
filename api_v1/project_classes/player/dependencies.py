from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.orm import selectinload

from . import crud
from core import db_helper
from core import TablePlayer


# A function for get a Tournament from the database by id
async def get_player_by_id(
    player_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TablePlayer:
    table_tournament = await session.scalar(
        select(TablePlayer)
        .where(TablePlayer.id == player_id)
        .options(
            selectinload(TablePlayer.matches),
            selectinload(TablePlayer.tournaments),
            selectinload(TablePlayer.team),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if table_tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {player_id} not found",
        )

    return table_tournament
