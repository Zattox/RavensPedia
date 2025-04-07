import requests
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_player_by_nickname
from .schemes import PlayerCreate, PlayerGeneralInfoUpdate

from ravenspedia.core import TablePlayer
from ravenspedia.core.config import faceit_settings

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {faceit_settings.api_key}",
}


async def get_players(session: AsyncSession) -> list[TablePlayer]:
    """
    Retrieve all players from the database.
    """
    statement = (
        select(TablePlayer)
        .options(
            selectinload(TablePlayer.stats),
            selectinload(TablePlayer.tournaments),
            selectinload(TablePlayer.team),
        )
        .order_by(TablePlayer.id)
    )

    players = await session.scalars(statement)
    return list(players)


async def get_player(
    session: AsyncSession,
    player_nickname: str,
) -> TablePlayer | None:
    """
    Retrieve a player by their nickname.
    """
    player = await get_player_by_nickname(
        session=session,
        player_nickname=player_nickname,
    )
    return player


async def find_player_faceit_profile(
    steam_id: str,
) -> dict:
    """
    Fetch a player's Faceit profile using their Steam ID.
    """
    params = {
        "game": "cs2",
        "game_player_id": steam_id,
    }
    response = requests.get(
        f"{faceit_settings.base_url}/players",
        headers=headers,
        params=params,
    )

    if response.status_code == status.HTTP_200_OK:
        return {
            "player_id": response.json()["player_id"],
            "faceit_elo": response.json()["games"]["cs2"]["faceit_elo"],
        }
    else:
        return {
            "player_id": None,
            "faceit_elo": None,
        }


async def create_player(
    session: AsyncSession,
    player_in: PlayerCreate,
) -> TablePlayer:
    """
    Create a new player in the database.
    """
    # Turning it into a Player class without Mapped fields
    player: TablePlayer = TablePlayer(**player_in.model_dump())
    faceit_profile = await find_player_faceit_profile(player_in.steam_id)
    player.faceit_id = faceit_profile["player_id"]
    player.faceit_elo = faceit_profile["faceit_elo"]

    try:
        session.add(player)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A player with such data already exists",
        )

    await session.refresh(player, attribute_names=["tournaments", "stats", "team"])
    return player


async def update_general_player_info(
    session: AsyncSession,
    player: TablePlayer,
    player_update: PlayerGeneralInfoUpdate,
) -> TablePlayer:
    """
    Update a player's general information in the database.
    """
    for class_field, value in player_update.model_dump(exclude_unset=True).items():
        if class_field == "steam_id":
            faceit_profile = await find_player_faceit_profile(value)
            setattr(player, "faceit_id", faceit_profile["faceit_id"])
            setattr(player, "faceit_elo", faceit_profile["faceit_elo"])
        setattr(player, class_field, value)

    await session.commit()
    return player


async def delete_player(
    session: AsyncSession,
    player: TablePlayer,
) -> None:
    """
    Delete a player from the database.
    """
    await session.delete(player)
    await session.commit()


async def update_faceit_elo(
    session: AsyncSession,
) -> None:
    """
    Update the Faceit ELO for all players in the database.
    """
    statement = (
        select(TablePlayer)
        .options(
            selectinload(TablePlayer.stats),
            selectinload(TablePlayer.tournaments),
            selectinload(TablePlayer.team),
        )
        .order_by(TablePlayer.id)
    )

    players = await session.scalars(statement)
    for player in players:
        faceit_profile = await find_player_faceit_profile(steam_id=player.steam_id)
        setattr(player, "faceit_elo", faceit_profile["faceit_elo"])

    await session.commit()


async def get_faceit_profile(
    player: TablePlayer,
) -> dict:
    """
    Retrieve a player's Faceit profile using their Steam ID.
    """
    params = {
        "game": "cs2",
        "game_player_id": player.steam_id,
    }
    response = requests.get(
        f"{faceit_settings.base_url}/players",
        headers=headers,
        params=params,
    )

    if response.status_code == status.HTTP_200_OK:
        return response.json()

    return {
        "error": "Profile not found",
        "status_code": response.status_code,
    }
