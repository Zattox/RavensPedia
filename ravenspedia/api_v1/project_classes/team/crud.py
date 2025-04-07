from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import (
    TableTeam,
    TableTournamentResult,
    MapName,
    TableTeamMapStats,
)
from .dependencies import get_team_by_name
from .schemes import TeamCreate, TeamGeneralInfoUpdate
from .team_management import calculate_team_faceit_elo
from ..team_stats.crud import delete_team_map_stats


async def get_teams(session: AsyncSession) -> list[TableTeam]:
    """
    Retrieve all teams from the database.
    """
    # Query all teams and eagerly load related data, ordered by ID
    stmt = (
        select(TableTeam)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.team
            ),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.tournament
            ),
        )
        .order_by(TableTeam.id)
    )
    teams = await session.scalars(stmt)
    return list(teams)


async def get_team(
    session: AsyncSession,
    team_name: str,
) -> TableTeam | None:
    """
    Retrieve a team by its name.
    """
    team = await get_team_by_name(team_name=team_name, session=session)
    return team


async def create_team(
    session: AsyncSession,
    team_in: TeamCreate,
) -> TableTeam:
    """
    Create a new team in the database.
    """
    # Convert the input data into a TableTeam object
    team: TableTeam = TableTeam(**team_in.model_dump())

    try:
        session.add(team)
        # Create map stats for each map and associate them with the team
        for map_name in MapName:
            new_stat = TableTeamMapStats(team_id=team.id, map=map_name)
            session.add(new_stat)
            team.map_stats.append(new_stat)
        await session.commit()
    except IntegrityError:
        # Rollback the session if a team with the same name already exists
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team_in.name} already exists",
        )

    # Refresh the team object with related data
    await session.refresh(
        team,
        attribute_names=["players", "matches", "tournaments", "tournament_results"],
    )
    return team


async def delete_team(
    session: AsyncSession,
    team: TableTeam,
) -> None:
    """
    Delete a team from the database.
    """
    from .team_management import delete_player_from_team

    # Remove all players from the team
    for player in list(team.players):
        await delete_player_from_team(session=session, team=team, player=player)

    # Delete all map stats associated with the team
    for map_stats in list(team.map_stats):
        await delete_team_map_stats(session=session, team=team, map_stats=map_stats)

    # Delete the team from the database
    await session.delete(team)
    await session.commit()


async def update_general_team_info(
    session: AsyncSession,
    team: TableTeam,
    team_update: TeamGeneralInfoUpdate,
) -> TableTeam:
    """
    Update a team's general information (name, description).
    """
    # Update the team's fields with the provided data
    for class_field, value in team_update.model_dump(exclude_unset=True).items():
        setattr(team, class_field, value)
    await session.commit()
    return team


async def update_team_faceit_elo(
    session: AsyncSession,
) -> None:
    """
    Update the Faceit Elo for all teams in the database.
    """
    # Query all teams and eagerly load related data
    stmt = (
        select(TableTeam)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
            selectinload(TableTeam.tournament_results).selectinload(
                TableTournamentResult.team
            ),
        )
        .order_by(TableTeam.id)
    )
    teams = await session.scalars(stmt)

    # Recalculate the Faceit Elo for each team
    for team in teams:
        await calculate_team_faceit_elo(team, session)
    await session.commit()
