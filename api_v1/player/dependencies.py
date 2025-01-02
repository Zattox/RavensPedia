from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from api_v1.player import crud
from core.models import db_helper


# A function for get a player from the database by id
async def get_player_by_id(
    player_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    player = await crud.get_player(session=session, player_id=player_id)
    # If such an id does not exist, then throw an exception.
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"player {player_id} not found",
        )
    return player
