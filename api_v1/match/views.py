from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from .scheme import Match, MatchCreate, MatchUpdatePartial
from core.models import db_helper

router = APIRouter(tags=["Matches"])


@router.get("/", response_model=list[Match])
async def get_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_matches(session=session)


@router.post("/", response_model=Match, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_in: MatchCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_match(session=session, match_in=match_in)


@router.get("/{match_id}/", response_model=Match)
async def get_match(
    match: Match = Depends(dependencies.get_match_by_id),
):
    return match


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


@router.delete("/{match_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    match: Match = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_match(session=session, match=match)
