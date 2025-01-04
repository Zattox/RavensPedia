from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core.project_models import db_helper
from .schemes import Team, TeamCreate, TeamUpdatePartial

router = APIRouter(tags=["Teams"])


# A view to get all the teams from the database
@router.get("/", response_model=list[Team])
async def get_teams(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_teams(session=session)


# A view for getting a team by its id from the database
@router.get("/{team_id}/", response_model=Team)
async def get_team(
    team: Team = Depends(dependencies.get_team_by_id),
):
    return team


# A view for create a team in the database
@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_team(session=session, team_in=team_in)


# A view for partial or full update a team in the database
@router.patch("/{team_id}/")
async def update_team(
    team_update: TeamUpdatePartial,
    team: Team = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_team_partial(
        session=session,
        team=team,
        team_update=team_update,
    )


# A view for delete a team from the database
@router.delete("/{team_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team: Team = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_team(session=session, team=team)
