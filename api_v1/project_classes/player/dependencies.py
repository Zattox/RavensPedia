from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from core import db_helper, TablePlayer


# A function for get a Tournament from the database by id
async def get_player_by_id(
    player_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TablePlayer:
    player = await session.scalar(
        select(TablePlayer)
        .where(TablePlayer.id == player_id)
        .options(
            selectinload(TablePlayer.matches),
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


# A function for get a Team from the database by id
async def get_player_by_nickname(
    player_nickname: str | None,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TablePlayer | None:
    player = await session.scalar(
        select(TablePlayer)
        .where(TablePlayer.name == player_nickname)
        .options(
            selectinload(TablePlayer.team),
            selectinload(TablePlayer.matches),
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
