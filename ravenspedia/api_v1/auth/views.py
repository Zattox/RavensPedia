from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper
from . import crud
from .schemas import UserCreate

router = APIRouter(tags=["Auth"])


@router.post("/register/")
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> dict:
    return await crud.register_user(
        user_in=user_in,
        session=session,
    )
