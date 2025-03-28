from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableTeam
from ravenspedia.core.project_models.table_match_info import MapName
from ravenspedia.core.project_models.table_team_stats import TableTeamMapStats
from .dependencies import get_team_by_id
from .schemes import TeamCreate, TeamGeneralInfoUpdate
from ..team_stats.crud import delete_team_map_stats


# A function to get all the Teams from the database
async def get_teams(session: AsyncSession) -> list[TableTeam]:
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
    return list(teams)


# A function for getting a Team by its id from the database
async def get_team(
    session: AsyncSession,
    team_id: int,
) -> TableTeam | None:
    team = await get_team_by_id(
        team_id=team_id,
        session=session,
    )
    return team


# A function for create a Team in the database
async def create_team(
    session: AsyncSession,
    team_in: TeamCreate,
) -> TableTeam:
    # Turning it into a Team class without Mapped fields
    team: TableTeam = TableTeam(**team_in.model_dump())

    try:
        session.add(team)
        for map_name in MapName:
            new_stat = TableTeamMapStats(
                team_id=team.id,
                map=map_name,
            )
            session.add(new_stat)
            team.map_stats.append(new_stat)
        await session.commit()  # Make changes to the database
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team_in.name} already exists",
        )

    return team


# A function for delete a Team from the database
async def delete_team(
    session: AsyncSession,
    team: TableTeam,
) -> None:
    from .team_management import delete_player_from_team

    for player in list(team.players):
        await delete_player_from_team(
            session=session,
            team=team,
            player=player,
        )

    for map_stats in list(team.map_stats):
        await delete_team_map_stats(
            session=session,
            team=team,
            map_stats=map_stats,
        )

    await session.delete(team)
    await session.commit()  # Make changes to the database


# A function for partial update a Team in the database
async def update_general_team_info(
    session: AsyncSession,
    team: TableTeam,
    team_update: TeamGeneralInfoUpdate,
) -> TableTeam:
    for class_field, value in team_update.model_dump(exclude_unset=True).items():
        setattr(team, class_field, value)
    await session.commit()  # Make changes to the database

    return team
