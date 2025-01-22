from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes import ResponseMatch, ResponseTournament
from ravenspedia.api_v1.schedules import schedule_matches, schedule_tournaments
from ravenspedia.core import db_helper

router = APIRouter(tags=["Schedules"])


@router.get(
    "/matches/get_last_completed/",
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
    "/matches/get_upcoming_scheduled/",
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
    "/matches/get_in_progress/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_in_progress_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_matches.get_in_progress_matches(
        session=session,
    )


@router.get(
    "/tournaments/get_last_completed/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_last_completed_tournaments(
    num_tournaments: int = 10,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_tournaments.get_last_x_completed_tournaments(
        session=session,
        num_tournaments=num_tournaments,
    )


@router.get(
    "/tournaments/get_upcoming_scheduled/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_scheduled_tournaments(
    num_tournaments: int = 10,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_tournaments.get_upcoming_tournaments(
        session=session,
        num_tournaments=num_tournaments,
    )


@router.get(
    "/tournaments/get_in_progress/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_in_progress_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await schedule_tournaments.get_in_progress_tournaments(
        session=session,
    )
