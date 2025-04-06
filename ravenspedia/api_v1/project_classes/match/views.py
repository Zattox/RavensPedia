from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import (
    db_helper,
    TableMatch,
    TableTeam,
    TableUser,
    GeneralPlayerStats,
)
from . import crud, dependencies, match_management
from .dependencies import get_match_by_id
from .schemes import ResponseMatch, MatchCreate, MatchGeneralInfoUpdate
from ..team import get_team_by_name
from ...auth.dependencies import get_current_admin_user

router = APIRouter(tags=["Matches"])
manager_match_router = APIRouter(tags=["Matches Manager"])


# Convert a TableMatch object to a ResponseMatch schema for API responses.
def table_to_response_form(
    match: TableMatch,
    is_create: bool = False,
) -> ResponseMatch:
    result = ResponseMatch(
        id=match.id,
        tournament=match.tournament.name,
        description=match.description,
        date=match.date,
        max_number_of_players=match.max_number_of_players,
        max_number_of_teams=match.max_number_of_teams,
        best_of=match.best_of,
        status=match.status,
        stats=[],
        veto=[],
        result=[],
    )

    if not is_create:
        # Populate additional fields if the match is not being created
        result.teams = [team.name for team in match.teams]
        result.players = list({elem.player.nickname for elem in match.stats})
        result.stats = [GeneralPlayerStats(**elem.match_stats) for elem in match.stats]
        result.veto = [elem for elem in match.veto]
        result.result = [elem for elem in match.result]

    return result


# Retrieve all matches from the database.
@router.get(
    "/",
    response_model=list[ResponseMatch],
    status_code=status.HTTP_200_OK,
)
async def get_matches(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseMatch]:
    matches = await crud.get_matches(session=session)
    result = [table_to_response_form(match=match) for match in matches]
    return result


# Retrieve a specific match by its ID.
@router.get(
    "/{match_id}/",
    response_model=ResponseMatch,
    status_code=status.HTTP_200_OK,
)
async def get_match(
    match_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await crud.get_match(
        match_id=match_id,
        session=session,
    )
    return table_to_response_form(match=match)


# Create a new match in the database (admin only).
@router.post(
    "/",
    response_model=ResponseMatch,
    status_code=status.HTTP_201_CREATED,
)
async def create_match(
    match_in: MatchCreate,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await crud.create_match(
        session=session,
        match_in=match_in,
    )
    return table_to_response_form(match=match, is_create=True)


# Update general information of a match (admin only).
@router.patch(
    "/{match_id}/",
    response_model=ResponseMatch,
    status_code=status.HTTP_200_OK,
)
async def update_general_match_info(
    match_update: MatchGeneralInfoUpdate,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await crud.update_general_match_info(
        session=session,
        match=match,
        match_update=match_update,
    )
    return table_to_response_form(match=match)


# Delete a match from the database (admin only).
@router.delete(
    "/{match_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_match(
        session=session,
        match=match,
    )


# Add a team to a match (admin only).
@manager_match_router.patch(
    "/{match_id}/add_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_team_in_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_management.add_team_in_match(
        session=session,
        match=match,
        team=team,
    )
    return table_to_response_form(match=match)


# Remove a team from a match (admin only).
@manager_match_router.delete(
    "/{match_id}/delete_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_team_from_match(
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin
    match: TableMatch = Depends(get_match_by_id),
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseMatch:
    match = await match_management.delete_team_from_match(
        session=session,
        match=match,
        team=team,
    )
    return table_to_response_form(match=match)
