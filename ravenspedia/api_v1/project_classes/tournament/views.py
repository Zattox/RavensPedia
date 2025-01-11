from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies, tournament_management
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate
from ravenspedia.core import db_helper, TableTournament, TableTeam
from ..team.dependencies import get_team_by_name

router = APIRouter(tags=["Tournaments"])
manager_tournament_router = APIRouter(tags=["Tournaments Manager"])


# A view to get all the tournaments from the database
@router.get(
    "/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTournament]:
    return await crud.get_tournaments(session=session)


# A view for getting a tournament by its id from the database
@router.get(
    "/{tournament_id}/",
    response_model=ResponseTournament,
    status_code=status.HTTP_200_OK,
)
async def get_tournament(
    tournament_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    return await crud.get_tournament(
        session=session,
        tournament_id=tournament_id,
    )


# A view for create a tournament in the database
@router.post(
    "/",
    response_model=ResponseTournament,
    status_code=status.HTTP_201_CREATED,
)
async def create_tournament(
    tournament_in: TournamentCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    return await crud.create_tournament(
        session=session,
        tournament_in=tournament_in,
    )


# A view for partial or full update a tournament in the database
@router.patch(
    "/{tournament_id}/",
    response_model=ResponseTournament,
    status_code=status.HTTP_200_OK,
)
async def update_general_tournament_info(
    tournament_update: TournamentGeneralInfoUpdate,
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    return await crud.update_general_tournament_info(
        session=session,
        tournament=tournament,
        tournament_update=tournament_update,
    )


# A view for delete a tournament from the database
@router.delete(
    "/{tournament_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tournament(
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_tournament(
        session=session,
        tournament=tournament,
    )


@manager_tournament_router.patch(
    "/{tournament_name}/add_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTournament,
)
async def add_team_in_tournament(
    team: TableTeam = Depends(get_team_by_name),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    return await tournament_management.add_team_in_tournament(
        team=team,
        tournament=tournament,
        session=session,
    )


@manager_tournament_router.delete(
    "/{tournament_name}/delete_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTournament,
)
async def delete_team_from_tournament(
    team: TableTeam = Depends(get_team_by_name),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    return await tournament_management.delete_team_from_tournament(
        team=team,
        tournament=tournament,
        session=session,
    )
