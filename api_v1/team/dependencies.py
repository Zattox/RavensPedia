from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from api_v1.team import crud
from core.models import db_helper


# A function for get a Team from the database by id
async def get_team_by_id(
    team_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    team = await crud.get_team(session=session, team_id=team_id)
    # If such an id does not exist, then throw an exception.
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"team {team_id} not found",
        )
    return team
