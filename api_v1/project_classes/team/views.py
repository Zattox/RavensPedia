from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core import db_helper

from core import TableTeam
from .schemes import Team as ResponseTeam

router = APIRouter(tags=["Teams"])


# A view to get all the teams from the database
@router.get("/", response_model=list[ResponseTeam])
async def get_teams(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTeam]:
    result: list[ResponseTeam] = await crud.get_teams(session=session)
    return result


# A view for getting a team by its id from the database
@router.get("/{team_id}/", response_model=ResponseTeam)
async def get_team(
    team: TableTeam = Depends(dependencies.get_team_by_id),
) -> ResponseTeam:
    return team


# A view for create a team in the database
@router.post("/", response_model=ResponseTeam, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_name: str,
    description: str | None = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTeam:
    return await crud.create_team(
        session=session,
        team_name=team_name,
        description=description,
    )


# A view for partial or full update a team in the database
@router.patch("/{team_id}/")
async def update_general_team_info(
    new_team_name: str | None = None,
    new_description: str | None = None,
    team: TableTeam = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_general_team_info(
        session=session,
        team=team,
        new_team_name=new_team_name,
        new_description=new_description,
    )


# A view for delete a team from the database
@router.delete("/{team_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team: TableTeam = Depends(dependencies.get_team_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_team(session=session, team=team)
