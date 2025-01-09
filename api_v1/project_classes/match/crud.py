from datetime import datetime

from typing import Union
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import api_v1.project_classes.team.dependencies
from core import Match as TableMatch
from .dependencies import get_match_by_id
from .schemes import Match as ResponseMatch
from core import Tournament as TableTournament
from api_v1.project_classes.team.dependencies import get_team_by_name


def table_to_response_form(
    table_match: TableMatch,
) -> ResponseMatch:
    return ResponseMatch(
        id=table_match.id,
        tournament=table_match.tournament.tournament_name,
        description=table_match.description,
        date=table_match.date,
        teams=[team.team_name for team in table_match.teams],
        players=[player.nickname for player in table_match.players],
    )


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
    result = []
    for match in list(matches):
        result.append(table_to_response_form(match))
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
    tournament_name: str,
    date: datetime,
    description: Union[str | None] = None,
    team_name_1: Union[str | None] = None,
    team_name_2: Union[str | None] = None,
) -> ResponseMatch:
    tournament_of_match: TableTournament = await session.scalar(
        select(TableTournament)
        .where(TableTournament.tournament_name == tournament_name)
        .options(
            selectinload(TableTournament.players),
            selectinload(TableTournament.matches),
            selectinload(TableTournament.teams),
        ),
    )
    team1 = await get_team_by_name(team_name_1, session=session)
    team2 = await get_team_by_name(team_name_2, session=session)
    table_match = TableMatch(
        tournament_id=tournament_of_match.id,
        tournament=tournament_of_match,
        date=date,
        description=description,
    )
    if team1 is not None:
        table_match.teams.append(team1)
        for player in team1.players:
            table_match.players.append(player)
    if team2 is not None:
        table_match.teams.append(team2)
        for player in team2.players:
            table_match.players.append(player)

    session.add(table_match)
    await session.commit()  # Make changes to the database
    return table_to_response_form(table_match)


# A function for delete a Match from the database
async def delete_match(
    session: AsyncSession,
    match: TableMatch,
) -> None:
    await session.delete(match)
    await session.commit()  # Make changes to the database
