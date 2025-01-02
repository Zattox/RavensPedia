from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Player
from api_v1.player.scheme import PlayerCreate, PlayerUpdatePartial


# A function to get all the Players from the database
async def get_players(session: AsyncSession) -> list[Player]:
    statement = select(Player).order_by(Player.id)
    result: Result = await session.execute(statement)
    players = result.scalars().all()
    return list(players)


# A function for getting a Player by its id from the database
async def get_player(
    session: AsyncSession,
    player_id: int,
) -> Player | None:
    return await session.get(Player, player_id)


# A function for create a Player in the database
async def create_player(
    session: AsyncSession,
    player_in: PlayerCreate,
) -> Player:
    # Turning it into a Player class without Mapped fields
    player = Player(**player_in.model_dump())
    session.add(player)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(player)
    return player


# A function for partial update a Player in the database
async def update_player_partial(
    session: AsyncSession,
    player: Player,
    player_update: PlayerUpdatePartial,
) -> Player:
    for name, value in player_update.model_dump(exclude_unset=True).items():
        setattr(player, name, value)
    await session.commit()  # Make changes to the database
    return player


# A function for delete a Player from the database
async def delete_player(
    session: AsyncSession,
    player: Player,
) -> None:
    await session.delete(player)
    await session.commit()  # Make changes to the database
