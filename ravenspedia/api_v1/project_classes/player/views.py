from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TablePlayer, TableUser
from ravenspedia.core.faceit_models import PlayerStats
from . import crud, dependencies
from .schemes import ResponsePlayer, PlayerCreate, PlayerGeneralInfoUpdate
from ...auth.dependencies import get_current_admin_user

router = APIRouter(tags=["Players"])


def table_to_response_form(
    player: TablePlayer,
    is_create: bool = False,
) -> ResponsePlayer:
    result = ResponsePlayer(
        steam_id=player.steam_id,
        faceit_id=player.faceit_id,
        faceit_elo=player.faceit_elo,
        nickname=player.nickname,
        name=player.name,
        surname=player.surname,
        stats=[],
    )

    if not is_create:
        result.matches = [
            {
                "match_id": elem.match_stats["match_id"],
                "round_of_match": elem.match_stats["round_of_match"],
            }
            for elem in player.stats
        ]
        result.tournaments = [tournament.name for tournament in player.tournaments]
        if player.team is not None:
            result.team = player.team.name
        result.stats = [PlayerStats(**elem.match_stats) for elem in player.stats]

    return result


# A view to get all the players from the database
@router.get(
    "/",
    response_model=list[ResponsePlayer],
    status_code=status.HTTP_200_OK,
)
async def get_players(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    players = await crud.get_players(session=session)
    result = [table_to_response_form(player) for player in players]
    return result


# A view for getting a player by its id from the database
@router.get(
    "/{player_nickname}/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_200_OK,
)
async def get_player(
    player_nickname: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponsePlayer:
    player = await crud.get_player(
        player_nickname=player_nickname,
        session=session,
    )
    return table_to_response_form(player)


# A view for create a player in the database
@router.post(
    "/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_201_CREATED,
)
async def create_player(
    player_in: PlayerCreate,
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    player = await crud.create_player(
        session=session,
        player_in=player_in,
    )
    return table_to_response_form(player, is_create=True)

@router.patch(
    "/update_faceit_elo/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_faceit_elo(
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.update_faceit_elo(session=session)


# A view for partial or full update a player in the database
@router.patch(
    "/{player_nickname}/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_200_OK,
)
async def update_general_player_info(
    player_update: PlayerGeneralInfoUpdate,
    admin: TableUser = Depends(get_current_admin_user),
    player: TablePlayer = Depends(dependencies.get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    new_player = await crud.update_general_player_info(
        session=session,
        player=player,
        player_update=player_update,
    )
    return table_to_response_form(new_player)


# A view for delete a player from the database
@router.delete(
    "/{player_nickname}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_player(
    admin: TableUser = Depends(get_current_admin_user),
    player: TablePlayer = Depends(dependencies.get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_player(session=session, player=player)


