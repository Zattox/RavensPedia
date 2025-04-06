from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import TableMatch, TableTournament, TableMatchStats
from .dependencies import get_match_by_id
from .schemes import MatchCreate, MatchGeneralInfoUpdate
from ..match_stats import sync_player_tournaments
from ..tournament import get_tournament_by_name


async def get_matches(session: AsyncSession) -> list[TableMatch]:
    """
    Retrieve all matches from the database with related data.
    """
    stmt = (
        select(TableMatch)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams),
            selectinload(TableMatch.tournament),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        )
        .order_by(TableMatch.id)
    )
    matches = await session.scalars(stmt)
    return list(matches)


async def get_match(
    session: AsyncSession,
    match_id: int,
) -> TableMatch | None:
    """
    Retrieve a specific match by its ID.
    """
    table_match: TableMatch = await get_match_by_id(
        match_id=match_id,
        session=session,
    )
    return table_match


async def create_match(
    session: AsyncSession,
    match_in: MatchCreate,
) -> TableMatch:
    """
    Create a new match in the database.
    """
    tournament_of_match: TableTournament = await get_tournament_by_name(
        tournament_name=match_in.tournament,
        session=session,
    )

    # Validate the match date against the tournament's date range
    if not (
        tournament_of_match.start_date <= match_in.date <= tournament_of_match.end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Match date must be between tournament dates: "
            f"{tournament_of_match.start_date} - {tournament_of_match.end_date}",
        )

    # Validate max number of teams and players
    if match_in.max_number_of_teams <= 0 or match_in.max_number_of_players <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Max number of teams and max number of players must be positive",
        )

    match = TableMatch(
        best_of=match_in.best_of,
        tournament_id=tournament_of_match.id,
        tournament=tournament_of_match,
        date=match_in.date,
        description=match_in.description,
        max_number_of_teams=match_in.max_number_of_teams,
        max_number_of_players=match_in.max_number_of_players,
    )

    session.add(match)
    await session.commit()
    return match


async def delete_match(
    session: AsyncSession,
    match: TableMatch,
) -> None:
    """
    Delete a match from the database and sync player tournaments.
    """
    # Gather all players associated with the match (via stats or teams)
    players = {stat.player for stat in match.stats}
    for team in match.teams:
        players.update(team.players)

    # Sync tournaments for all affected players
    for player in players:
        await sync_player_tournaments(session, player)

    # Delete the match and commit
    await session.delete(match)
    await session.commit()


async def update_general_match_info(
    session: AsyncSession,
    match: TableMatch,
    match_update: MatchGeneralInfoUpdate,
) -> TableMatch:
    """
    Update general information of a match (e.g., tournament, date, description).
    """
    # Update fields dynamically based on the provided update data
    for class_field, value in match_update.model_dump(exclude_unset=True).items():
        if class_field == "tournament":
            tournament_of_match: TableTournament = await get_tournament_by_name(
                tournament_name=value,
                session=session,
            )
            setattr(match, "tournament_id", tournament_of_match.id)
            match.tournament = tournament_of_match
        elif class_field == "date":
            # Validate the match date against the tournament's date range
            if not (match.tournament.start_date <= value <= match.tournament.end_date):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Match date must be between tournament dates: "
                    f"{match.tournament.start_date} - {match.tournament.end_date}",
                )
            setattr(match, class_field, value)
        else:
            setattr(match, class_field, value)

    await session.commit()
    return match
