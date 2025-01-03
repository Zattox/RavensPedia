from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path

from api_v1.project_classes.match import crud
from core.project_models import db_helper


# A function for get a match from the database by id
async def get_match_by_id(
    match_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    match = await crud.get_match(session=session, match_id=match_id)
    # If such an id does not exist, then throw an exception.
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} not found",
        )
    return match
