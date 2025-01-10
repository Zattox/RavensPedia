from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import TableTournament
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate
from .dependencies import get_tournament_by_id


def table_to_response_form(
    table_tournament: TableTournament,
) -> ResponseTournament:
    return ResponseTournament(
        id=table_tournament.id,
        tournament_name=table_tournament.name,
        description=table_tournament.description,
        prize=table_tournament.prize,
        matches_id=[match.id for match in table_tournament.matches],
        teams=[team.name for team in table_tournament.teams],
        players=[player.nickname for player in table_tournament.players],
    )


# A function to get all the Tournaments from the database
async def get_tournaments(session: AsyncSession) -> list[ResponseTournament]:
    stmt = (
        select(TableTournament)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.teams),
            selectinload(TableTournament.matches),
        )
        .order_by(TableTournament.id)
    )
    tournaments = await session.scalars(stmt)
    result = []
    for tournament in list(tournaments):
        result.append(table_to_response_form(tournament))
    return result


# A function for getting a Tournament by its id from the database
async def get_tournament(
    session: AsyncSession,
    tournament_id: int,
) -> ResponseTournament | None:
    tournament: TableTournament = await get_tournament_by_id(
        tournament_id=tournament_id,
        session=session,
    )
    return table_to_response_form(tournament)


# A function for create a Tournament in the database
async def create_tournament(
    session: AsyncSession,
    tournament_in: TournamentCreate,
) -> ResponseTournament:
    # Turning it into a Tournament class without Mapped fields
    tournament = TableTournament(
        name=tournament_in.name,
        prize=tournament_in.prize,
        description=tournament_in.description,
    )
    session.add(tournament)
    await session.commit()
    return ResponseTournament(
        tournament_name=tournament.name,
        description=tournament.description,
        prize=tournament.prize,
        matches_id=[],
        players=[],
        teams=[],
        id=tournament.id,
    )


# A function for delete a Tournament from the database
async def delete_tournament(
    session: AsyncSession,
    tournament: TableTournament,
) -> None:
    await session.delete(tournament)
    await session.commit()  # Make changes to the database


# A function for partial update a Tournament in the database
async def update_general_tournament_info(
    session: AsyncSession,
    tournament: TableTournament,
    tournament_update: TournamentGeneralInfoUpdate,
) -> ResponseTournament:
    for class_field, value in tournament_update.model_dump(exclude_unset=True).items():
        setattr(tournament, class_field, value)
    await session.commit()  # Make changes to the database
    return table_to_response_form(tournament)
