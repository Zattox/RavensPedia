from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.match import crud
from core.models import db_helper


async def get_match_by_id(
    match_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    match = await crud.get_match(session=session, match_id=match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} not found",
        )
    return match
