from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableTournament, TableMatchStats
from .dependencies import get_match_by_id
from .schemes import MatchCreate, MatchGeneralInfoUpdate
from ..match_stats.helpers import sync_player_tournaments
from ..tournament.dependencies import get_tournament_by_name


async def get_matches(session: AsyncSession) -> list[TableMatch]:
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        )
        .order_by(TableMatch.id)
    )
    matches = await session.scalars(stmt)
    return list(matches)


async def get_match(
    session: AsyncSession,
    match_id: int,
) -> TableMatch | None:
    table_match: TableMatch = await get_match_by_id(
        match_id=match_id,
        session=session,
    )
    return table_match


async def create_match(
    session: AsyncSession,
    match_in: MatchCreate,
) -> TableMatch:
    tournament_of_match: TableTournament = await get_tournament_by_name(
        tournament_name=match_in.tournament,
        session=session,
    )

    match = TableMatch(
        best_of=match_in.best_of,
        tournament_id=tournament_of_match.id,
        tournament=tournament_of_match,
        date=match_in.date,
        description=match_in.description,
        max_number_of_teams=match_in.max_number_of_teams,
        max_number_of_players=match_in.max_number_of_players,
    )

    session.add(match)
    await session.commit()  # Make changes to the database

    return match


async def delete_match(
    session: AsyncSession,
    match: TableMatch,
) -> None:
    players = {stat.player for stat in match.stats}
    for team in match.teams:
        players.update(team.players)

    for player in players:
        await sync_player_tournaments(session, player)

    await session.delete(match)
    await session.commit()  # Make changes to the database


async def update_general_match_info(
    session: AsyncSession,
    match: TableMatch,
    match_update: MatchGeneralInfoUpdate,
) -> TableMatch:
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
    return match
