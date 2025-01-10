from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core import TableTeam
from .dependencies import get_team_by_id
from .schemes import ResponseTeam, TeamCreate, TeamGeneralInfoUpdate


def table_to_response_form(
    team: TableTeam,
    is_create: bool = False,
) -> ResponseTeam:
    result = ResponseTeam(
        id=team.id,
        name=team.name,
        description=team.description,
        max_number_of_players=team.max_number_of_players,
    )

    if not is_create:
        result.players = [player.nickname for player in team.players]
        result.matches_id = [match.id for match in team.matches]
        result.tournaments = [tournament.name for tournament in team.tournaments]

    return result


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
    result = [table_to_response_form(team=team) for team in list(teams)]
    return result


# A function for getting a Team by its id from the database
async def get_team(
    session: AsyncSession,
    team_id: int,
) -> ResponseTeam | None:
    team = await get_team_by_id(
        team_id=team_id,
        session=session,
    )
    return table_to_response_form(team=team)


# A function for create a Team in the database
async def create_team(
    session: AsyncSession,
    team_in: TeamCreate,
) -> ResponseTeam:
    # Turning it into a Team class without Mapped fields
    team: TableTeam = TableTeam(
        name=team_in.name,
        description=team_in.description,
        max_number_of_players=team_in.max_number_of_players,
    )

    try:
        session.add(team)
        await session.commit()  # Make changes to the database
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team_in.name} already exists",
        )

    return table_to_response_form(team=team, is_create=True)


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
    team_update: TeamGeneralInfoUpdate,
) -> ResponseTeam:
    for class_field, value in team_update.model_dump(exclude_unset=True).items():
        setattr(team, class_field, value)
    await session.commit()  # Make changes to the database
    return table_to_response_form(team)
