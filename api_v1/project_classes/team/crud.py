import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core import Team as TableTeam

from .schemes import Team as ResponseTeam

from .schemes import StringIntPair


async def table_to_response_form(
    table_team: TableTeam,
) -> ResponseTeam:
    return ResponseTeam(
        team_name=table_team.team_name,
        description=table_team.description,
        players=[
            StringIntPair(name=player.nickname, id=player.id)
            for player in table_team.players
        ],
        matches_id=[match.id for match in table_team.matches],
        tournaments=[
            StringIntPair(name=tournament.tournament_name, id=tournament.id)
            for tournament in table_team.tournaments
        ],
        id=table_team.id,
    )


# A function to get all the Teams from the database
async def get_teams(session: AsyncSession) -> list[ResponseTeam]:
    stmt = (
        select(TableTeam)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
        )
        .order_by(TableTeam.id)
    )
    teams = await session.scalars(stmt)
    result = []
    for team in list(teams):
        result.append(await table_to_response_form(team))
    return result


# A function for getting a Team by its id from the database
async def get_team(
    session: AsyncSession,
    team_id: int,
) -> ResponseTeam | None:
    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.id == team_id)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
        ),
    )
    return await table_to_response_form(table_team)


# A function for create a Team in the database
async def create_team(
    session: AsyncSession,
    team_name: str,
    description: str | None = None,
) -> ResponseTeam:
    # Turning it into a Team class without Mapped fields
    table_team: TableTeam = TableTeam(
        team_name=team_name,
        description=description,
    )
    session.add(table_team)
    await session.commit()  # Make changes to the database

    return ResponseTeam(
        team_name=table_team.team_name,
        description=table_team.description,
        players=[],
        matches_id=[],
        tournaments=[],
        id=table_team.id,
    )


# # A function for partial update a Team in the database
# async def update_team_partial(
#     session: AsyncSession,
#     team: Team,
#     team_update: TeamUpdatePartial,
# ) -> Team:
#     for name, value in team_update.model_dump(exclude_unset=True).items():
#         setattr(team, name, value)
#     await session.commit()  # Make changes to the database
#     return team


# A function for delete a Team from the database
async def delete_team(
    session: AsyncSession,
    team: TableTeam,
) -> None:
    await session.delete(team)
    await session.commit()  # Make changes to the database
