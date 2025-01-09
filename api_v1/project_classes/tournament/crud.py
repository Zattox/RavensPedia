from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core import Tournament as TableTournament
from .schemes import Tournament as ResponseTournament
from .dependencies import get_tournament_by_id


def table_to_response_form(
    table_tournament: TableTournament,
) -> ResponseTournament:
    return ResponseTournament(
        id=table_tournament.id,
        tournament_name=table_tournament.tournament_name,
        description=table_tournament.description,
        prize=table_tournament.prize,
        matches_id=[match.id for match in table_tournament.matches],
        teams=[team.team_name for team in table_tournament.teams],
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
    table_match: TableTournament = await get_tournament_by_id(
        tournament_id=tournament_id,
        session=session,
    )
    return table_to_response_form(table_match)


# # A function for create a Tournament in the database
# async def create_tournament(
#     session: AsyncSession,
#     tournament_name: str,
#     prize: str | None = None,
#     description: str | None = None,
# ) -> ResponseTournament:
#     # Turning it into a Tournament class without Mapped fields
#     tournament = Tournament(
#         tournament_name=tournament_name,
#         prize=prize,
#         description=description,
#     )
#     session.add(tournament)
#     await session.commit()  # Make changes to the database
#     # It is necessary if there are changes on the database side
#     # await session.refresh(tournament)
#     return tournament


# # A function for partial update a Tournament in the database
# async def update_tournament_partial(
#     session: AsyncSession,
#     tournament: Tournament,
#     tournament_update: TournamentUpdatePartial,
# ) -> Tournament:
#     for name, value in tournament_update.model_dump(exclude_unset=True).items():
#         setattr(tournament, name, value)
#     await session.commit()  # Make changes to the database
#     return tournament


# A function for delete a Tournament from the database
async def delete_tournament(
    session: AsyncSession,
    tournament: TableTournament,
) -> None:
    await session.delete(tournament)
    await session.commit()  # Make changes to the database
