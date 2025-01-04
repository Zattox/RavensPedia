from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.project_models import db_helper
from .schemes import MatchInfo, MatchInfoCreate

router = APIRouter(tags=["Matches Info"])


# A view for create a match_info in the database
@router.post("/", response_model=MatchInfo, status_code=status.HTTP_201_CREATED)
async def create_match_info(
    faceit_match_id: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_match_info(
        session=session, faceit_match_id=faceit_match_id
    )
