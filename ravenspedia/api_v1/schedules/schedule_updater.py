from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableMatch, TableTournament
from ravenspedia.core.project_models.table_match import MatchStatus
from ravenspedia.core.project_models.table_tournament import TournamentStatus


async def manual_update_match_status(
    match: TableMatch,
    new_status: MatchStatus,
    session: AsyncSession,
) -> TableMatch:
    """Manually update the status of a given match and commit the change to the database."""
    setattr(match, "status", new_status)
    await session.commit()
    return match


async def manual_update_tournament_status(
    tournament: TableTournament,
    new_status: TournamentStatus,
    session: AsyncSession,
) -> TableTournament:
    """Manually update the status of a given tournament and commit the change to the database."""
    setattr(tournament, "status", new_status)
    await session.commit()
    return tournament


async def auto_update_matches_statuses(session: AsyncSession) -> dict:
    """Automatically update match statuses based on their dates relative to the current time."""
    current_time = datetime.now()

    # Update future matches to SCHEDULED
    await session.execute(
        update(TableMatch)
        .where(TableMatch.date > current_time)
        .values(status=MatchStatus.SCHEDULED)
    )

    # Update past or current scheduled matches to IN_PROGRESS
    await session.execute(
        update(TableMatch)
        .where(
            TableMatch.date <= current_time,
            TableMatch.status == MatchStatus.SCHEDULED,
        )
        .values(status=MatchStatus.IN_PROGRESS)
    )

    await session.commit()
    return {"message": "Matches statuses updated successfully"}


async def auto_update_tournaments_statuses(session: AsyncSession) -> dict:
    """Automatically update tournament statuses based on their start and end dates."""
    current_time = datetime.now()

    # Update past tournaments to COMPLETED
    await session.execute(
        update(TableTournament)
        .where(TableTournament.end_date <= current_time)
        .values(status=TournamentStatus.COMPLETED)
    )

    # Update current tournaments to IN_PROGRESS
    await session.execute(
        update(TableTournament)
        .where(
            TableTournament.start_date <= current_time,
            TableTournament.end_date >= current_time,
        )
        .values(status=TournamentStatus.IN_PROGRESS)
    )

    # Update future tournaments to SCHEDULED
    await session.execute(
        update(TableTournament)
        .where(TableTournament.start_date > current_time)
        .values(status=TournamentStatus.SCHEDULED)
    )

    await session.commit()
    return {"message": "Tournaments statuses updated successfully"}
