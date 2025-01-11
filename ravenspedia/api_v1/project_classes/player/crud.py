from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TablePlayer
from .schemes import ResponsePlayer, PlayerCreate, PlayerGeneralInfoUpdate
from .dependencies import get_player_by_id


def table_to_response_form(
    player: TablePlayer,
    is_create: bool = False,
) -> ResponsePlayer:
    result = ResponsePlayer(
        id=player.id,
        nickname=player.nickname,
        name=player.name,
        surname=player.surname,
    )

    if not is_create:
        result.matches_id = [match.id for match in player.matches]
        result.tournaments = [tournament.name for tournament in player.tournaments]
        if player.team is not None:
            result.team = player.team.name

    return result


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
    result = [table_to_response_form(player=player) for player in list(players)]
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
    return table_to_response_form(player=player)


# A function for create a Player in the database
async def create_player(
    session: AsyncSession,
    player_in: PlayerCreate,
) -> ResponsePlayer:
    # Turning it into a Player class without Mapped fields
    player = TablePlayer(
        nickname=player_in.nickname,
        name=player_in.name,
        surname=player_in.surname,
    )

    try:
        session.add(player)
        await session.commit()  # Make changes to the database
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player {player_in.nickname} already exists",
        )

    return table_to_response_form(player=player, is_create=True)


# A function for partial update a Player in the database
async def update_general_player_info(
    session: AsyncSession,
    player: TablePlayer,
    player_update: PlayerGeneralInfoUpdate,
) -> ResponsePlayer:
    for class_field, value in player_update.model_dump(exclude_unset=True).items():
        setattr(player, class_field, value)
    await session.commit()  # Make changes to the database
    return table_to_response_form(player=player)


# A function for delete a Player from the database
async def delete_player(
    session: AsyncSession,
    player: TablePlayer,
) -> None:
    await session.delete(player)
    await session.commit()  # Make changes to the database
