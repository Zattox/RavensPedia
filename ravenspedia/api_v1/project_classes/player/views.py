from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth.dependencies import get_current_admin_user
from ravenspedia.core import db_helper, TablePlayer, TableUser, PlayerStats
from . import crud, dependencies
from .schemes import ResponsePlayer, PlayerCreate, PlayerGeneralInfoUpdate

router = APIRouter(tags=["Players"])


def table_to_response_form(
    player: TablePlayer,
) -> ResponsePlayer:
    """
    Convert a TablePlayer object to a ResponsePlayer schema for API responses.
    """
    result = ResponsePlayer(
        steam_id=player.steam_id,
        faceit_id=player.faceit_id,
        faceit_elo=player.faceit_elo,
        nickname=player.nickname,
        name=player.name,
        surname=player.surname,
        stats=[],
    )

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


@router.get(
    "/{player_nickname}/get_faceit_profile/",  # Updated path to include player_nickname
    status_code=status.HTTP_200_OK,
)
async def get_faceit_profile(
    player: TablePlayer = Depends(dependencies.get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    """
    Retrieve a player's Faceit profile using their steam_id.
    """
    response = await crud.get_faceit_profile(player=player)
    return response


@router.get(
    "/",
    response_model=list[ResponsePlayer],
    status_code=status.HTTP_200_OK,
)
async def get_players(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponsePlayer]:
    """
    Retrieve all players from the database.
    """
    players = await crud.get_players(session=session)
    result = [table_to_response_form(player) for player in players]
    return result


@router.get(
    "/{player_nickname}/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_200_OK,
)
async def get_player(
    player_nickname: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponsePlayer:
    """
    Retrieve a player by their nickname.
    """
    player = await crud.get_player(
        player_nickname=player_nickname,
        session=session,
    )
    return table_to_response_form(player)


@router.post(
    "/",
    response_model=ResponsePlayer,
    status_code=status.HTTP_201_CREATED,
)
async def create_player(
    player_in: PlayerCreate,
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponsePlayer:
    """
    Create a new player in the database (admin only).
    """
    player = await crud.create_player(
        session=session,
        player_in=player_in,
    )
    return table_to_response_form(player)


@router.patch(
    "/update_faceit_elo/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_faceit_elo(
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    Update the Faceit ELO for all players in the database (admin only).
    """
    await crud.update_faceit_elo(session=session)


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
) -> ResponsePlayer:
    """
    Update a player's general information (admin only).
    """
    new_player = await crud.update_general_player_info(
        session=session,
        player=player,
        player_update=player_update,
    )
    return table_to_response_form(new_player)


@router.delete(
    "/{player_nickname}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_player(
    admin: TableUser = Depends(get_current_admin_user),
    player: TablePlayer = Depends(dependencies.get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    """
    Delete a player from the database (admin only).
    """
    await crud.delete_player(session=session, player=player)
