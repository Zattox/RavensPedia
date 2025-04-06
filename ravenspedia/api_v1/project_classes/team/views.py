from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TableTeam, TablePlayer, TableUser
from . import crud, dependencies, team_management
from .schemes import ResponseTeam, TeamCreate, TeamGeneralInfoUpdate
from ..player.dependencies import get_player_by_nickname
from ...auth.dependencies import get_current_admin_user

router = APIRouter(tags=["Teams"])
manager_team_router = APIRouter(tags=["Teams Manager"])


def table_to_response_form(
    team: TableTeam,
) -> ResponseTeam:
    result = ResponseTeam(
        name=team.name,
        description=team.description,
        max_number_of_players=team.max_number_of_players,
        average_faceit_elo=team.average_faceit_elo,
    )

    result.players = [player.nickname for player in team.players]
    result.matches_id = [match.id for match in team.matches]
    result.tournaments = [tournament.name for tournament in team.tournaments]
    result.tournament_results = [
        {"place": result.place, "tournament_name": result.tournament.name}
        for result in team.tournament_results
    ]

    return result


# A view to get all the teams from the database
@router.get(
    "/",
    response_model=list[ResponseTeam],
    status_code=status.HTTP_200_OK,
)
async def get_teams(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTeam]:
    teams = await crud.get_teams(session=session)
    result = [table_to_response_form(team=team) for team in teams]
    return result


# A view for getting a team by its id from the database
@router.get(
    "/{team_name}/",
    response_model=ResponseTeam,
    status_code=status.HTTP_200_OK,
)
async def get_team(
    team_name: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    team = await crud.get_team(
        session=session,
        team_name=team_name,
    )
    return table_to_response_form(team=team)


# A view for create a team in the database
@router.post(
    "/",
    response_model=ResponseTeam,
    status_code=status.HTTP_201_CREATED,
)
async def create_team(
    team_in: TeamCreate,
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    team = await crud.create_team(
        session=session,
        team_in=team_in,
    )
    return table_to_response_form(team=team)


@router.patch(
    "/update_team_faceit_elo/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_faceit_elo(
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.update_team_faceit_elo(session=session)


# A view for partial or full update a team in the database
@router.patch(
    "/{team_name}/",
    response_model=ResponseTeam,
    status_code=status.HTTP_200_OK,
)
async def update_general_team_info(
    team_update: TeamGeneralInfoUpdate,
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(dependencies.get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    team = await crud.update_general_team_info(
        session=session,
        team=team,
        team_update=team_update,
    )
    return table_to_response_form(team=team)


# A view for delete a team from the database
@router.delete(
    "/{team_name}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_team(
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(dependencies.get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_team(session=session, team=team)


@manager_team_router.patch(
    "/{team_name}/add_player/{player_nickname}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTeam,
)
async def add_player_in_team(
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(dependencies.get_team_by_name),
    player: TablePlayer = Depends(get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    team = await team_management.add_player_in_team(
        team=team,
        player=player,
        session=session,
    )
    return table_to_response_form(team=team)


@manager_team_router.delete(
    "/{team_name}/delete_player/{player_nickname}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTeam,
)
async def delete_player_from_team(
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(dependencies.get_team_by_name),
    player: TablePlayer = Depends(get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    team = await team_management.delete_player_from_team(
        team=team,
        player=player,
        session=session,
    )
    return table_to_response_form(team=team)
