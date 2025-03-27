from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ravenspedia.api_v1.auth.dependencies import get_current_admin_user
from ravenspedia.api_v1.project_classes import ResponseMatch
from ravenspedia.api_v1.project_classes.match import match_management
from ravenspedia.api_v1.project_classes.match.dependencies import get_match_by_id
from ravenspedia.api_v1.project_classes.match.views import table_to_response_form
from ravenspedia.api_v1.project_classes.match_stats import match_stats_faceit_management
from ravenspedia.api_v1.project_classes.match_stats.match_stats_manual import (
    add_manual_match_stats,
)
from ravenspedia.api_v1.project_classes.match_stats.schemes import MatchStatsInput
from ravenspedia.core import TableMatch, db_helper, TableUser

router = APIRouter(tags=["Matches Stats Manager"])


@router.patch(
    "/{match_id}/add_faceit_stats/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_match_stats_from_faceit(
    faceit_url: str,
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await match_stats_faceit_management.add_match_stats_from_faceit(
        session=session,
        match=match,
        faceit_url=faceit_url,
    )
    return table_to_response_form(match=match)


@router.delete(
    "/{match_id}/delete_match_stats/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_match_stats(
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await match_management.delete_match_stats(
        session=session,
        match=match,
    )
    return table_to_response_form(match=match)


@router.post(
    "/{match_id}/add_stats_manual/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_manual_stats(
    match_id: int,
    stats_input: MatchStatsInput,
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await add_manual_match_stats(
        session=session,
        stats_input=stats_input,
        match_id=match_id,
    )
    return table_to_response_form(match=match)
