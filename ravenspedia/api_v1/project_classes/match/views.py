from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.match_stats import match_stats_faceit_management
from ravenspedia.core import db_helper, TableMatch, TableTeam, TableUser
from ravenspedia.core.faceit_models.general_player_stats import GeneralPlayerStats
from . import crud, dependencies, match_management
from .dependencies import get_match_by_id
from .schemes import ResponseMatch, MatchCreate, MatchGeneralInfoUpdate
from ..team.dependencies import get_team_by_name
from ...auth.dependencies import get_current_admin_user

router = APIRouter(tags=["Matches"])
manager_match_router = APIRouter(tags=["Matches Manager"])


def table_to_response_form(
    match: TableMatch,
    is_create: bool = False,
) -> ResponseMatch:
    result = ResponseMatch(
        tournament=match.tournament.name,
        description=match.description,
        date=match.date,
        max_number_of_players=match.max_number_of_players,
        max_number_of_teams=match.max_number_of_teams,
        best_of=match.best_of,
        status=match.status,
        stats=[],
    )

    if not is_create:
        result.teams = [team.name for team in match.teams]
        result.players = list({elem.player.nickname for elem in match.stats})
        result.stats = [GeneralPlayerStats(**elem.match_stats) for elem in match.stats]

    return result


# A view to get all the matches from the database
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


# A view for getting a match by its id from the database
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


# A view for create a match in the database
@router.post(
    "/",
    response_model=ResponseMatch,
    status_code=status.HTTP_201_CREATED,
)
async def create_match(
    match_in: MatchCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await crud.create_match(
        session=session,
        match_in=match_in,
    )
    return table_to_response_form(match=match, is_create=True)


# A view for partial or full update a match in the database
@router.patch(
    "/{match_id}/",
    response_model=ResponseMatch,
    status_code=status.HTTP_200_OK,
)
async def update_general_match_info(
    match_update: MatchGeneralInfoUpdate,
    match: TableMatch = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await crud.update_general_match_info(
        session=session,
        match=match,
        match_update=match_update,
    )
    return table_to_response_form(match=match)


# A view for delete a match from the database
@router.delete(
    "/{match_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_match(
    match: TableMatch = Depends(dependencies.get_match_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> None:
    await crud.delete_match(
        session=session,
        match=match,
    )


@manager_match_router.patch(
    "/{match_id}/add_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def add_team_in_match(
    match: TableMatch = Depends(get_match_by_id),
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await match_management.add_team_in_match(
        session=session,
        match=match,
        team=team,
    )
    return table_to_response_form(match=match)


@manager_match_router.delete(
    "/{match_id}/delete_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseMatch,
)
async def delete_team_from_match(
    match: TableMatch = Depends(get_match_by_id),
    team: TableTeam = Depends(get_team_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
    admin: TableUser = Depends(get_current_admin_user),
) -> ResponseMatch:
    match = await match_management.delete_team_from_match(
        session=session,
        match=match,
        team=team,
    )
    return table_to_response_form(match=match)


@manager_match_router.patch(
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


@manager_match_router.delete(
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
