from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from .schemes import ResponsePlayer, PlayerCreate, PlayerGeneralInfoUpdate
from ravenspedia.core import db_helper, TablePlayer

router = APIRouter(tags=["Players"])


# A view to get all the players from the database
@router.get(
    "/",
    response_model=list[ResponsePlayer],
    status_code=status.HTTP_200_OK,
)
async def get_players(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_players(session=session)


# A view for getting a player by its id from the database
@router.get(
    "/{player_id}/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_200_OK,
)
async def get_player(
    player_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponsePlayer:
    return await crud.get_player(
        player_id=player_id,
        session=session,
    )


# A view for create a player in the database
@router.post(
    "/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_201_CREATED,
)
async def create_player(
    player_in: PlayerCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_player(
        session=session,
        player_in=player_in,
    )


# A view for partial or full update a player in the database
@router.patch(
    "/{player_id}/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_200_OK,
)
async def update_general_player_info(
    player_update: PlayerGeneralInfoUpdate,
    player: TablePlayer = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_general_player_info(
        session=session,
        player=player,
        player_update=player_update,
    )


# A view for delete a player from the database
@router.delete(
    "/{player_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_player(
    player: TablePlayer = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_player(session=session, player=player)
