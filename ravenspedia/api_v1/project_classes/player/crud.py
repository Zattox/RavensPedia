import requests
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TablePlayer
from ravenspedia.core.config import faceit_settings
from .dependencies import get_player_by_id, get_player_by_nickname
from .schemes import PlayerCreate, PlayerGeneralInfoUpdate


# A function to get all the Players from the database
async def get_players(session: AsyncSession) -> list[TablePlayer]:
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


# A function for getting a Player by its id from the database
async def get_player(
    session: AsyncSession,
    player_nickname: str,
) -> TablePlayer | None:
    player = await get_player_by_nickname(
        session=session,
        player_nickname=player_nickname,
    )
    return player


async def find_player_faceit_profile(
    steam_id: str,
) -> dict:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.api_key}",
    }
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


# A function for create a Player in the database
async def create_player(
    session: AsyncSession,
    player_in: PlayerCreate,
) -> TablePlayer:
    # Turning it into a Player class without Mapped fields
    player: TablePlayer = TablePlayer(**player_in.model_dump())
    faceit_profile = await find_player_faceit_profile(player_in.steam_id)
    player.faceit_id = faceit_profile["player_id"]
    player.faceit_elo = faceit_profile["faceit_elo"]

    try:
        session.add(player)
        await session.commit()  # Make changes to the database
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A player with such data already exists",
        )

    return player


# A function for partial update a Player in the database
async def update_general_player_info(
    session: AsyncSession,
    player: TablePlayer,
    player_update: PlayerGeneralInfoUpdate,
) -> TablePlayer:
    for class_field, value in player_update.model_dump(exclude_unset=True).items():
        if class_field == "steam_id":
            faceit_profile = await find_player_faceit_profile(value)
            setattr(player, "faceit_id", faceit_profile["faceit_id"])
            setattr(player, "faceit_elo", faceit_profile["faceit_elo"])
        setattr(player, class_field, value)
    await session.commit()  # Make changes to the database
    return player


# A function for delete a Player from the database
async def delete_player(
    session: AsyncSession,
    player: TablePlayer,
) -> None:
    await session.delete(player)
    await session.commit()  # Make changes to the database


async def update_faceit_elo(
    session: AsyncSession,
) -> None:
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
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.api_key}",
    }
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
    return {"error": "Profile not found", "status_code": response.status_code}
