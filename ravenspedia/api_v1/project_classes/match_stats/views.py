from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.auth.dependencies import get_current_admin_user
from ravenspedia.api_v1.project_classes import ResponseMatch
from ravenspedia.core import TableMatch, db_helper, TableUser
from . import match_stats_faceit_management, match_info
from .match_stats_manual import add_manual_match_stats, delete_last_statistic_from_match
from .schemes import MatchStatsInput, MapPickBanInfo, MapResultInfo
from ..match import match_management
from ..match.dependencies import get_match_by_id
from ..match.views import table_to_response_form

router = APIRouter(tags=["Matches Stats Manager"])
info_router = APIRouter(tags=["Matches Info Manager"])


# Add Faceit stats to a match (admin only).
@router.patch(
    "/{match_id}/add_faceit_stats/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_match_stats_from_faceit(
    faceit_url: str,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_stats_faceit_management.add_match_stats_from_faceit(
        session=session,
        match=match,
        faceit_url=faceit_url,
    )
    return table_to_response_form(match=match)


# Delete all stats from a match (admin only).
@router.delete(
    "/{match_id}/delete_match_stats/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_match_stats(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_management.delete_match_stats(
        session=session,
        match=match,
    )
    return table_to_response_form(match=match)


# Add manual stats to a match (admin only).
@router.patch(
    "/{match_id}/add_stats_manual/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_manual_stats(
    stats_input: MatchStatsInput,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await add_manual_match_stats(
        session=session,
        stats_input=stats_input,
        match=match,
    )
    return table_to_response_form(match=match)


# Delete the last stat from a match (admin only).
@router.delete(
    "/{match_id}/delete_last_stat_from_match/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_last_stat_from_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await delete_last_statistic_from_match(
        session=session,
        match=match,
    )
    return table_to_response_form(match=match)


# Add pick/ban info to a match (admin only).
@info_router.patch(
    "/{match_id}/add_pick_ban_info_in_match/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_pick_ban_info_in_match(
    info: MapPickBanInfo,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_info.add_pick_ban_info_in_match(
        session=session,
        info=info,
        match=match,
    )
    return table_to_response_form(match=match)


# Delete the last pick/ban info from a match (admin only).
@info_router.delete(
    "/{match_id}/delete_last_pick_ban_info_from_match/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_last_pick_ban_info_from_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_info.delete_last_pick_ban_info_from_match(
        session=session,
        match=match,
    )
    return table_to_response_form(match=match)


# Add map result info to a match (admin only).
@info_router.patch(
    "/{match_id}/add_map_result_info_in_match/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_map_result_info_in_match(
    info: MapResultInfo,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_info.add_map_result_info_in_match(
        session=session,
        info=info,
        match=match,
    )
    return table_to_response_form(match=match)


# Delete the last map result info from a match (admin only).
@info_router.delete(
    "/{match_id}/delete_last_map_result_info_from_match/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_last_map_result_info_from_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_info.delete_last_map_result_info_from_match(
        session=session,
        match=match,
    )
    return table_to_response_form(match=match)
