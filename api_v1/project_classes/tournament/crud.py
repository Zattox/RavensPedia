from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import TableTournament
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate
from .dependencies import get_tournament_by_id


def table_to_response_form(
    table_tournament: TableTournament,
    is_create: bool = False,
) -> ResponseTournament:
    result = ResponseTournament(
        id=table_tournament.id,
        tournament_name=table_tournament.name,
        description=table_tournament.description,
        prize=table_tournament.prize,
    )

    if not is_create:
        result.matches_id = [match.id for match in table_tournament.matches]
        result.teams = [team.name for team in table_tournament.teams]
        result.players = [player.nickname for player in table_tournament.players]

    return result


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
    result = [
        table_to_response_form(table_tournament=tournament)
        for tournament in list(tournaments)
    ]
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
    return table_to_response_form(table_tournament=tournament)


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

    try:
        session.add(tournament)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tournament {tournament_in.name} already exists",
        )

    return table_to_response_form(table_tournament=tournament, is_create=True)


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
    return table_to_response_form(table_tournament=tournament)
