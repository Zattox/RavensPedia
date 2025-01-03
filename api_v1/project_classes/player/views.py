from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core.project_models import db_helper
from .scheme import Player, PlayerCreate, PlayerUpdatePartial

router = APIRouter(tags=["Players"])


# A view to get all the players from the database
@router.get("/", response_model=list[Player])
async def get_players(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_players(session=session)


# A view for getting a player by its id from the database
@router.get("/{player_id}/", response_model=Player)
async def get_player(
    player: Player = Depends(dependencies.get_player_by_id),
):
    return player


# A view for create a player in the database
@router.post("/", response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_in: PlayerCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_player(session=session, player_in=player_in)


# A view for partial or full update a player in the database
@router.patch("/{player_id}/")
async def update_player(
    player_update: PlayerUpdatePartial,
    player: Player = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_player_partial(
        session=session,
        player=player,
        player_update=player_update,
    )


# A view for delete a player from the database
@router.delete("/{player_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(
    player: Player = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_player(session=session, player=player)
