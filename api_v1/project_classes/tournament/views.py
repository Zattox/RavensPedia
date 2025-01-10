from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate
from core import db_helper, TableTournament

router = APIRouter(tags=["Tournaments"])


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
    await crud.delete_tournament(session=session, tournament=tournament)
