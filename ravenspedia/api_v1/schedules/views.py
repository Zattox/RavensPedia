from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes import ResponseMatch
from ravenspedia.api_v1.schedules import schedule_matches
from ravenspedia.core import db_helper

router = APIRouter(tags=["Schedules"])


@router.get(
    "/get_last_completed_matches/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_last_completed_matches(
    num_matches: int = 50,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_matches.get_last_x_completed_matches(
        session=session,
        num_matches=num_matches,
    )


@router.get(
    "/get_upcoming_scheduled_matches/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_scheduled_matches(
    num_matches: int = 50,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_matches.get_upcoming_matches(
        session=session,
        num_matches=num_matches,
    )


@router.get(
    "/get_in_progress_matches/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_in_progress_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_matches.get_in_progress_matches(
        session=session,
    )
