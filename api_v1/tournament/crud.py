from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tournament
from api_v1.tournament.scheme import TournamentCreate, TournamentUpdatePartial


# A function to get all the Tournaments from the database
async def get_tournaments(session: AsyncSession) -> list[Tournament]:
    statement = select(Tournament).order_by(Tournament.id)
    result: Result = await session.execute(statement)
    tournaments = result.scalars().all()
    return list(tournaments)


# A function for getting a Tournament by its id from the database
async def get_tournament(
    session: AsyncSession,
    tournament_id: int,
) -> Tournament | None:
    return await session.get(Tournament, tournament_id)


# A function for create a Tournament in the database
async def create_tournament(
    session: AsyncSession,
    tournament_in: TournamentCreate,
) -> Tournament:
    # Turning it into a Tournament class without Mapped fields
    tournament = Tournament(**tournament_in.model_dump())
    session.add(tournament)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(tournament)
    return tournament


# A function for partial update a Tournament in the database
async def update_tournament_partial(
    session: AsyncSession,
    tournament: Tournament,
    tournament_update: TournamentUpdatePartial,
) -> Tournament:
    for name, value in tournament_update.model_dump(exclude_unset=True).items():
        setattr(tournament, name, value)
    await session.commit()  # Make changes to the database
    return tournament


# A function for delete a Tournament from the database
async def delete_tournament(
    session: AsyncSession,
    tournament: Tournament,
) -> None:
    await session.delete(tournament)
    await session.commit()  # Make changes to the database
