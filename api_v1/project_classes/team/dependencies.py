from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.orm import selectinload

from . import crud
from core import db_helper
from core import Team as TableTeam


# A function for get a Team from the database by id
async def get_team_by_id(
    team_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableTeam:
    table_team = await session.scalar(
        select(TableTeam)
        .where(TableTeam.id == team_id)
        .options(
            selectinload(TableTeam.players),
            selectinload(TableTeam.matches),
            selectinload(TableTeam.tournaments),
        ),
    )
    # If such an id does not exist, then throw an exception.
    if table_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"team {team_id} not found",
        )
    return table_team
