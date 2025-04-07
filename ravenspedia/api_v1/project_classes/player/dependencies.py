from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import db_helper, TablePlayer


async def get_player_by_id(
    player_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TablePlayer:
    """
    Retrieve a player from the database by their ID.
    """
    player = await session.scalar(
        select(TablePlayer)
        .where(TablePlayer.id == player_id)
        .options(
            selectinload(TablePlayer.stats),
            selectinload(TablePlayer.tournaments),
            selectinload(TablePlayer.team),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {player_id} not found",
        )

    return player


async def get_player_by_nickname(
    player_nickname: str | None,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TablePlayer | None:
    """
    Retrieve a player from the database by their nickname.
    """
    player = await session.scalar(
        select(TablePlayer)
        .where(TablePlayer.nickname == player_nickname)
        .options(
            selectinload(TablePlayer.team),
            selectinload(TablePlayer.stats),
            selectinload(TablePlayer.tournaments),
        ),
    )

    # If such an id does not exist, then throw an exception.
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player {player_nickname} not found",
        )

    return player
