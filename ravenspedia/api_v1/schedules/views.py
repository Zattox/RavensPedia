from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth.dependencies import get_current_admin_user
from ravenspedia.api_v1.project_classes import ResponseMatch, ResponseTournament
from ravenspedia.api_v1.schedules import (
    schedule_matches,
    schedule_tournaments,
    schedule_updater,
)
from ravenspedia.core import db_helper, TableUser
from ravenspedia.core.project_models.table_match import MatchStatus
from ravenspedia.core.project_models.table_tournament import (
    TournamentStatus,
)

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


@router.post(
    "/matches/update_statuses/",
    status_code=status.HTTP_200_OK,
)
async def auto_update_matches_statuses(
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> dict:
    return await schedule_updater.auto_update_matches_statuses(session)


@router.post(
    "/tournaments/update_statuses/",
    status_code=status.HTTP_200_OK,
)
async def auto_update_tournaments_statuses(
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> dict:
    return await schedule_updater.auto_update_tournaments_statuses(session)


@router.patch(
    "/matches/{match_id}/status/",
    status_code=status.HTTP_200_OK,
)
async def manual_update_match_status(
    match_id: int,
    new_status: MatchStatus,
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> dict:
    return await schedule_updater.manual_update_match_status(
        match_id, new_status, session
    )


@router.patch(
    "/tournaments/{tournament_id}/status/",
    status_code=status.HTTP_200_OK,
)
async def manual_update_tournament_status(
    tournament_id: int,
    new_status: TournamentStatus,
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> dict:
    return await schedule_updater.manual_update_tournament_status(
        tournament_id, new_status, session
    )
