from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .schemes import ResponseMatch, MatchCreate, MatchGeneralInfoUpdate
from .dependencies import get_match_by_id
from ravenspedia.core import TableMatch, TableTournament
from ..tournament.dependencies import get_tournament_by_name


def table_to_response_form(
    match: TableMatch,
    is_create: bool = False,
) -> ResponseMatch:
    result = ResponseMatch(
        id=match.id,
        tournament=match.tournament.name,
        description=match.description,
        date=match.date,
        max_number_of_players=match.max_number_of_players,
        max_number_of_teams=match.max_number_of_teams,
    )

    if not is_create:
        result.teams = [team.name for team in match.teams]
        result.players = [player.nickname for player in match.players]

    return result


async def get_matches(session: AsyncSession) -> list[ResponseMatch]:
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.players),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
        )
        .order_by(TableMatch.id)
    )
    matches = await session.scalars(stmt)
    result = [table_to_response_form(match) for match in list(matches)]
    return result


async def get_match(
    session: AsyncSession,
    match_id: int,
) -> ResponseMatch | None:
    table_match: TableMatch = await get_match_by_id(
        match_id=match_id,
        session=session,
    )
    return table_to_response_form(table_match)


async def create_match(
    session: AsyncSession,
    match_in: MatchCreate,
) -> ResponseMatch:
    tournament_of_match: TableTournament = await get_tournament_by_name(
        tournament_name=match_in.tournament,
        session=session,
    )

    match = TableMatch(
        tournament_id=tournament_of_match.id,
        tournament=tournament_of_match,
        date=match_in.date,
        description=match_in.description,
        max_number_of_teams=match_in.max_number_of_teams,
        max_number_of_players=match_in.max_number_of_players,
    )

    session.add(match)
    await session.commit()  # Make changes to the database

    return table_to_response_form(match=match, is_create=True)


# A function for delete a Match from the database
async def delete_match(
    session: AsyncSession,
    match: TableMatch,
) -> None:
    await session.delete(match)
    await session.commit()  # Make changes to the database


async def update_general_match_info(
    session: AsyncSession,
    match: TableMatch,
    match_update: MatchGeneralInfoUpdate,
) -> ResponseMatch:
    for class_field, value in match_update.model_dump(exclude_unset=True).items():
        if class_field == "tournament":
            tournament_of_match: TableTournament = await get_tournament_by_name(
                tournament_name=value,
                session=session,
            )
            setattr(match, "tournament_id", tournament_of_match.id)
            match.tournament = tournament_of_match
        else:
            setattr(match, class_field, value)

    await session.commit()  # Make changes to the database
    return table_to_response_form(match=match)
