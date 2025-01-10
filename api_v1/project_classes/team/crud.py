from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import TableTeam
from .schemes import ResponseTeam


async def table_to_response_form(
    table_team: TableTeam,
) -> ResponseTeam:
    return ResponseTeam(
        team_name=table_team.name,
        description=table_team.description,
        players=[player.nickname for player in table_team.players],
        matches_id=[match.id for match in table_team.matches],
        tournaments=[tournament.name for tournament in table_team.tournaments],
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
        name=team_name,
        description=description,
    )
    session.add(table_team)
    await session.commit()  # Make changes to the database

    return ResponseTeam(
        team_name=table_team.name,
        description=table_team.description,
        players=[],
        matches_id=[],
        tournaments=[],
        id=table_team.id,
    )


# A function for delete a Team from the database
async def delete_team(
    session: AsyncSession,
    team: TableTeam,
) -> None:
    await session.delete(team)
    await session.commit()  # Make changes to the database


# A function for partial update a Team in the database
async def update_general_team_info(
    session: AsyncSession,
    team: TableTeam,
    new_team_name: str | None = None,
    new_description: str | None = None,
) -> ResponseTeam:
    if new_team_name is not None:
        setattr(team, "team_name", new_team_name)
    if new_description is not None:
        setattr(team, "description", new_description)
    await session.commit()  # Make changes to the database

    return await table_to_response_form(team)
