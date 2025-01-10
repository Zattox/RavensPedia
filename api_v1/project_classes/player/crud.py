from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import TablePlayer
from .schemes import ResponsePlayer
from .dependencies import get_player_by_id


def table_to_response_form(player: TablePlayer) -> ResponsePlayer:
    team = "None"
    if player.team_id != -1:
        team = player.team.name
    return ResponsePlayer(
        nickname=player.nickname,
        name=player.name,
        surname=player.surname,
        team=team,
        matches_id=[match.id for match in player.matches],
        tournaments=[tournament.name for tournament in player.tournaments],
        id=player.id,
    )


# A function to get all the Players from the database
async def get_players(session: AsyncSession) -> list[ResponsePlayer]:
    statement = (
        select(TablePlayer)
        .options(
            selectinload(TablePlayer.matches),
            selectinload(TablePlayer.tournaments),
            selectinload(TablePlayer.team),
        )
        .order_by(TablePlayer.id)
    )
    players = await session.scalars(statement)
    result = []
    for player in list(players):
        result.append(table_to_response_form(player))
    return result


# A function for getting a Player by its id from the database
async def get_player(
    session: AsyncSession,
    player_id: int,
) -> ResponsePlayer | None:
    player = await get_player_by_id(
        session=session,
        player_id=player_id,
    )
    return table_to_response_form(player)


# A function for create a Player in the database
async def create_player(
    session: AsyncSession,
    nickname: str,
    team_id: int,
    name: str | None = None,
    surname: str | None = None,
) -> ResponsePlayer:
    # Turning it into a Player class without Mapped fields
    player = TablePlayer(
        nickname=nickname,
        name=name,
        surname=surname,
        team_id=team_id,
    )
    session.add(player)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(player)
    return ResponsePlayer(
        nickname=player.nickname,
        name=player.name,
        surname=player.surname,
        team="None",
        matches_id=[],
        tournaments=[],
        id=player.id,
    )


# A function for partial update a Player in the database
async def update_general_player_info(
    session: AsyncSession,
    player: TablePlayer,
    new_nickname: str | None = None,
    new_name: str | None = None,
    new_surname: str | None = None,
) -> ResponsePlayer:
    if new_nickname is not None:
        setattr(player, "nickname", new_nickname)
    if new_name is not None:
        setattr(player, "name", new_name)
    if new_surname is not None:
        setattr(player, "surname", new_surname)
    await session.commit()  # Make changes to the database
    return player


# A function for delete a Player from the database
async def delete_player(
    session: AsyncSession,
    player: TablePlayer,
) -> None:
    await session.delete(player)
    await session.commit()  # Make changes to the database
