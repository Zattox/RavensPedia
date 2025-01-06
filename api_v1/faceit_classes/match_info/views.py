from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies
from core.project_models import db_helper
from .schemes import MatchInfo, MatchInfoUpdate
from core.faceit_models.round_info import RoundInfo, RoundStats

router = APIRouter(tags=["Matches Info"])


# A view for create a match_info in the database
@router.post("/", response_model=MatchInfo, status_code=status.HTTP_201_CREATED)
async def create_match_info(
    data: list[RoundInfo] = Depends(dependencies.get_data_from_faceit),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_match_info(
        session=session,
        data=data,
    )


# A view to get all the matches from the database
@router.get("/", response_model=list[MatchInfo])
async def get_matches_info(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_matches_info(session=session)


# A view for getting a match by its id from the database
@router.get("/{match_info_id}/", response_model=MatchInfo)
async def get_match_info(
    match_info: MatchInfo = Depends(dependencies.get_match_info_by_id),
):
    return match_info


@router.put("/{match_info_id}/")
async def update_match_info(
    data: list[RoundInfo] = Depends(dependencies.get_data_from_faceit),
    match_info: MatchInfo = Depends(dependencies.get_match_info_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    match_info_update: MatchInfoUpdate = MatchInfoUpdate(
        faceit_match_id=data[0].match_id,
        rounds=data,
    )
    return await crud.update_match_info(
        session=session,
        match_info=match_info,
        match_info_update=match_info_update,
    )


# A view for delete a match from the database
@router.delete("/{match_info_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match_info(
    match_info: MatchInfo = Depends(dependencies.get_match_info_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_match_info(session=session, match_info=match_info)
