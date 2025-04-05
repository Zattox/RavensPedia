from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth.dependencies import get_current_admin_user
from ravenspedia.api_v1.project_classes import ResponseMatch, ResponseTournament
from ravenspedia.core import (
    db_helper,
    TableUser,
    TableMatch,
    MatchStatus,
    TableTournament,
    TournamentStatus,
)
from . import schedule_matches, schedule_tournaments, schedule_updater
from ..project_classes.match.dependencies import get_match_by_id
from ..project_classes.match.views import table_to_response_form as match_response_form
from ..project_classes.tournament.dependencies import get_tournament_by_name
from ..project_classes.tournament.views import (
    table_to_response_form as tournament_response_form,
)

router = APIRouter(tags=["Schedules"])


# Endpoint to retrieve completed matches
@router.get(
    "/matches/get_last_completed/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_last_completed_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseMatch]:
    matches = await schedule_matches.get_completed_matches(
        session=session,
    )
    result = [match_response_form(match) for match in matches]
    return result


# Endpoint to retrieve upcoming scheduled matches
@router.get(
    "/matches/get_upcoming_scheduled/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_scheduled_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseMatch]:
    matches = await schedule_matches.get_upcoming_matches(
        session=session,
    )
    result = [match_response_form(match) for match in matches]
    return result


# Endpoint to retrieve in-progress matches
@router.get(
    "/matches/get_in_progress/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_in_progress_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseMatch]:
    matches = await schedule_matches.get_in_progress_matches(
        session=session,
    )
    result = [match_response_form(match) for match in matches]
    return result


# Endpoint to retrieve completed tournaments
@router.get(
    "/tournaments/get_completed/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_completed_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTournament]:
    tournaments = await schedule_tournaments.get_last_x_completed_tournaments(
        session=session,
    )
    result = [tournament_response_form(tournament) for tournament in tournaments]
    return result


# Endpoint to retrieve upcoming scheduled tournaments
@router.get(
    "/tournaments/get_upcoming_scheduled/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_scheduled_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTournament]:
    tournaments = await schedule_tournaments.get_upcoming_tournaments(
        session=session,
    )
    result = [tournament_response_form(tournament) for tournament in tournaments]
    return result


# Endpoint to retrieve in-progress tournaments
@router.get(
    "/tournaments/get_in_progress/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_in_progress_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTournament]:
    tournaments = await schedule_tournaments.get_in_progress_tournaments(
        session=session,
    )
    result = [tournament_response_form(tournament) for tournament in tournaments]
    return result


# Endpoint to automatically update match statuses (admin only)
@router.patch("/matches/update_statuses/", status_code=status.HTTP_200_OK)
async def auto_update_matches_statuses(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await schedule_updater.auto_update_matches_statuses(
        session=session,
    )


# Endpoint to automatically update tournament statuses (admin only)
@router.patch("/tournaments/update_statuses/", status_code=status.HTTP_200_OK)
async def auto_update_tournaments_statuses(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await schedule_updater.auto_update_tournaments_statuses(
        session=session,
    )


# Endpoint to manually update a match status (admin only)
@router.patch("/matches/{match_id}/update_status/", status_code=status.HTTP_200_OK)
async def manual_update_match_status(
    new_status: MatchStatus,
    match: TableMatch = Depends(get_match_by_id),
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    result = await schedule_updater.manual_update_match_status(
        match=match,
        new_status=new_status,
        session=session,
    )
    return {"message": f"Match {match.id} status updated to {new_status.value}"}


# Endpoint to manually update a tournament status (admin only)
@router.patch(
    "/tournaments/{tournament_name}/update_status/", status_code=status.HTTP_200_OK
)
async def manual_update_tournament_status(
    new_status: TournamentStatus,
    tournament: TableTournament = Depends(get_tournament_by_name),
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    result = await schedule_updater.manual_update_tournament_status(
        tournament=tournament,
        new_status=new_status,
        session=session,
    )
    return {
        "message": f"Tournament {tournament.name} status updated to {new_status.value}"
    }
