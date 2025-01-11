from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies, team_management
from .schemes import ResponseTeam, TeamCreate, TeamGeneralInfoUpdate
from ravenspedia.core import db_helper, TableTeam, TablePlayer
from ..player.dependencies import get_player_by_nickname

router = APIRouter(tags=["Teams"])
manager_team_router = APIRouter(tags=["Teams Manager"])


# A view to get all the teams from the database
@router.get(
    "/",
    response_model=list[ResponseTeam],
    status_code=status.HTTP_200_OK,
)
async def get_teams(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTeam]:
    return await crud.get_teams(session=session)


# A view for getting a team by its id from the database
@router.get(
    "/{team_id}/",
    response_model=ResponseTeam,
    status_code=status.HTTP_200_OK,
)
async def get_team(
    team_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    return await crud.get_team(
        session=session,
        team_id=team_id,
    )


# A view for create a team in the database
@router.post(
    "/",
    response_model=ResponseTeam,
    status_code=status.HTTP_201_CREATED,
)
async def create_team(
    team_in: TeamCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    return await crud.create_team(
        session=session,
        team_in=team_in,
    )


# A view for partial or full update a team in the database
@router.patch(
    "/{team_id}/",
    response_model=ResponseTeam,
    status_code=status.HTTP_201_CREATED,
)
async def update_general_team_info(
    team_update: TeamGeneralInfoUpdate,
    team: TableTeam = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_general_team_info(
        session=session,
        team=team,
        team_update=team_update,
    )


# A view for delete a team from the database
@router.delete(
    "/{team_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_team(
    team: TableTeam = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_team(session=session, team=team)


@manager_team_router.patch(
    "/{team_name}/add_player/{player_nickname}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTeam,
)
async def add_player_in_team(
    team: TableTeam = Depends(dependencies.get_team_by_name),
    player: TablePlayer = Depends(get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    return await team_management.add_player_in_team(
        team=team,
        player=player,
        session=session,
    )


@manager_team_router.delete(
    "/{team_name}/delete_player/{player_nickname}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTeam,
)
async def delete_player_from_team(
    team: TableTeam = Depends(dependencies.get_team_by_name),
    player: TablePlayer = Depends(get_player_by_nickname),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    return await team_management.delete_player_from_team(
        team=team,
        player=player,
        session=session,
    )
