from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core import db_helper
from .crud import table_to_response_form
from .schemes import ResponseTournament
from core import TableTournament

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
@router.post(
    "/", response_model=ResponseTournament, status_code=status.HTTP_201_CREATED
)
async def create_tournament(
    tournament_name: str,
    prize: str | None = None,
    description: str | None = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_tournament(
        session=session,
        tournament_name=tournament_name,
        prize=prize,
        description=description,
    )


# A view for partial or full update a tournament in the database
@router.patch("/{tournament_id}/")
async def update_tournament(
    new_tournament_name: str | None = None,
    new_prize: str | None = None,
    new_description: str | None = None,
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_general_tournament_info(
        session=session,
        tournament=tournament,
        new_tournament_name=new_tournament_name,
        new_prize=new_prize,
        new_description=new_description,
    )


# A view for delete a tournament from the database
@router.delete("/{tournament_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_tournament(session=session, tournament=tournament)
