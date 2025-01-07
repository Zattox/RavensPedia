from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core import db_helper
from .schemes import Match, MatchCreate, MatchUpdatePartial

router = APIRouter(tags=["Matches"])


# A view to get all the matches from the database
@router.get("/", response_model=list[Match])
async def get_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_matches(session=session)


# A view for getting a match by its id from the database
@router.get("/{match_id}/", response_model=Match)
async def get_match(
    match: Match = Depends(dependencies.get_match_by_id),
):
    return match


# A view for create a match in the database
@router.post("/", response_model=Match, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_in: MatchCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_match(session=session, match_in=match_in)


# A view for partial or full update a match in the database
@router.patch("/{match_id}/")
async def update_match(
    match_update: MatchUpdatePartial,
    match: Match = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_match_partial(
        session=session,
        match=match,
        match_update=match_update,
    )


# A view for delete a match from the database
@router.delete("/{match_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match: Match = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_match(session=session, match=match)
