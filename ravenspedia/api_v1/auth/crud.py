from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from ravenspedia.core import TableUser
from .schemas import UserCreate
from . import utils


async def register_user(
    user_in: UserCreate,
    session: AsyncSession,
) -> dict:
    user: TableUser = TableUser(
        email=user_in.email,
        password=utils.get_hash_password(user_in.password),
    )

    try:
        session.add(user)
        await session.commit()  # Make changes to the database
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_in.email} already exists",
        )

    return {"message": f"The user has been successfully registered!"}
