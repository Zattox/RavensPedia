from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper, TableTournament, TableTeam, TableUser
from . import crud, dependencies, tournament_management
from .schemes import ResponseTournament, TournamentCreate, TournamentGeneralInfoUpdate
from ..team.dependencies import get_team_by_name
from ...auth.dependencies import get_current_admin_user

router = APIRouter(tags=["Tournaments"])
manager_tournament_router = APIRouter(tags=["Tournaments Manager"])


def table_to_response_form(
    tournament: TableTournament,
    is_create: bool = False,
) -> ResponseTournament:
    result = ResponseTournament(
        name=tournament.name,
        description=tournament.description,
        prize=tournament.prize,
        max_count_of_teams=tournament.max_count_of_teams,
        status=tournament.status,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
    )

    if not is_create:
        result.matches_id = [match.id for match in tournament.matches]
        result.teams = [team.name for team in tournament.teams]
        result.players = [player.nickname for player in tournament.players]

    return result


# A view to get all the tournaments from the database
@router.get(
    "/",
    response_model=list[ResponseTournament],
    status_code=status.HTTP_200_OK,
)
async def get_tournaments(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ResponseTournament]:
    tournaments = await crud.get_tournaments(session=session)
    result = [
        table_to_response_form(tournament=tournament) for tournament in tournaments
    ]
    return result


# A view for getting a tournament by its id from the database
@router.get(
    "/{tournament_id}/",
    response_model=ResponseTournament,
    status_code=status.HTTP_200_OK,
)
async def get_tournament(
    tournament_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    tournament = await crud.get_tournament(
        session=session,
        tournament_id=tournament_id,
    )
    return table_to_response_form(tournament=tournament)


# A view for create a tournament in the database
@router.post(
    "/",
    response_model=ResponseTournament,
    status_code=status.HTTP_201_CREATED,
)
async def create_tournament(
    tournament_in: TournamentCreate,
    admin: TableUser = Depends(get_current_admin_user),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    tournament = await crud.create_tournament(
        session=session,
        tournament_in=tournament_in,
    )
    return table_to_response_form(tournament=tournament, is_create=True)


# A view for partial or full update a tournament in the database
@router.patch(
    "/{tournament_id}/",
    response_model=ResponseTournament,
    status_code=status.HTTP_200_OK,
)
async def update_general_tournament_info(
    tournament_update: TournamentGeneralInfoUpdate,
    admin: TableUser = Depends(get_current_admin_user),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    tournament = await crud.update_general_tournament_info(
        session=session,
        tournament=tournament,
        tournament_update=tournament_update,
    )
    return table_to_response_form(tournament=tournament)


# A view for delete a tournament from the database
@router.delete(
    "/{tournament_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_tournament(
    admin: TableUser = Depends(get_current_admin_user),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_tournament(
        session=session,
        tournament=tournament,
    )


@manager_tournament_router.patch(
    "/{tournament_name}/add_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTournament,
)
async def add_team_in_tournament(
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(get_team_by_name),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    tournament = await tournament_management.add_team_in_tournament(
        team=team,
        tournament=tournament,
        session=session,
    )
    return table_to_response_form(tournament)


@manager_tournament_router.delete(
    "/{tournament_name}/delete_team/{team_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTournament,
)
async def delete_team_from_tournament(
    admin: TableUser = Depends(get_current_admin_user),
    team: TableTeam = Depends(get_team_by_name),
    tournament: TableTournament = Depends(dependencies.get_tournament_by_name),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseTournament:
    tournament = await tournament_management.delete_team_from_tournament(
        team=team,
        tournament=tournament,
        session=session,
    )
    return table_to_response_form(tournament=tournament)
