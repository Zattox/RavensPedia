from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core import db_helper
from .crud import table_to_response_form
from .schemes import ResponsePlayer
from core import TablePlayer

router = APIRouter(tags=["Players"])


# A view to get all the players from the database
@router.get("/", response_model=list[ResponsePlayer])
async def get_players(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_players(session=session)


# A view for getting a player by its id from the database
@router.get("/{player_id}/", response_model=ResponsePlayer)
async def get_player(
    player: TablePlayer = Depends(dependencies.get_player_by_id),
):
    return table_to_response_form(player)


# A view for create a player in the database
@router.post("/", response_model=ResponsePlayer, status_code=status.HTTP_201_CREATED)
async def create_player(
    nickname: str,
    team_id: int,
    name: str | None = None,
    surname: str | None = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_player(
        session=session,
        nickname=nickname,
        team_id=team_id,
        name=name,
        surname=surname,
    )


# A view for partial or full update a player in the database
@router.patch("/{player_id}/")
async def update_player(
    player: TablePlayer = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    new_nickname: str | None = None,
    new_name: str | None = None,
    new_surname: str | None = None,
):
    return await crud.update_general_player_info(
        session=session,
        player=player,
        new_nickname=new_nickname,
        new_name=new_name,
        new_surname=new_surname,
    )


# A view for delete a player from the database
@router.delete("/{player_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(
    player: TablePlayer = Depends(dependencies.get_player_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_player(session=session, player=player)
