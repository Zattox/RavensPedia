from datetime import datetime

from fastapi import status, HTTPException
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
    setattr(match, "status", new_status)
    await session.commit()

    return match


async def manual_update_tournament_status(
    tournament: TableTournament,
    new_status: TournamentStatus,
    session: AsyncSession,
) -> TableTournament:
    setattr(tournament, "status", new_status)
    await session.commit()

    return tournament


async def auto_update_matches_statuses(
    session: AsyncSession,
) -> dict:
    current_time = datetime.now()

    await session.execute(
        update(TableMatch)
        .where(TableMatch.date > current_time)
        .values(status=MatchStatus.SCHEDULED)
    )

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


async def auto_update_tournaments_statuses(
    session: AsyncSession,
) -> dict:
    current_time = datetime.now()

    await session.execute(
        update(TableTournament)
        .where(TableTournament.end_date <= current_time)
        .values(status=TournamentStatus.COMPLETED)
    )

    await session.execute(
        update(TableTournament)
        .where(
            TableTournament.start_date <= current_time,
            TableTournament.end_date >= current_time,
        )
        .values(status=TournamentStatus.IN_PROGRESS)
    )

    await session.execute(
        update(TableTournament)
        .where(TableTournament.start_date > current_time)
        .values(status=TournamentStatus.SCHEDULED)
    )

    await session.commit()
    return {"message": "Tournaments statuses updated successfully"}
