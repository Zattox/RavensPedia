from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core import db_helper
from .crud import table_to_response_form
from .schemes import Tournament as ResponseTournament
from core import Tournament as TableTournament

router = APIRouter(tags=["Tournaments"])


# A view to get all the tournaments from the database
@router.get("/", response_model=list[ResponseTournament])
async def get_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_tournaments(session=session)


# A view for getting a tournament by its id from the database
@router.get("/{tournament_id}/", response_model=ResponseTournament)
async def get_tournament(
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
):
    return table_to_response_form(tournament)


# A view for create a tournament in the database
# @router.post("/", response_model=Tournament, status_code=status.HTTP_201_CREATED)
# async def create_tournament(
#     tournament_in: TournamentCreate,
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     return await crud.create_tournament(session=session, tournament_in=tournament_in)


# A view for partial or full update a tournament in the database
# @router.patch("/{tournament_id}/")
# async def update_tournament(
#     tournament_update: TournamentUpdatePartial,
#     tournament: Tournament = Depends(dependencies.get_tournament_by_id),
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     return await crud.update_tournament_partial(
#         session=session,
#         tournament=tournament,
#         tournament_update=tournament_update,
#     )


# A view for delete a tournament from the database
@router.delete("/{tournament_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_tournament(session=session, tournament=tournament)
