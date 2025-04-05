from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import db_helper
from .crud import search_entities
from .schemes import SearchResult

router = APIRouter(tags=["Search"])


# Define the search endpoint for GET requests
@router.get(
    "/",
    response_model=SearchResult,
    status_code=status.HTTP_200_OK,
)
async def search(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> SearchResult:
    return await search_entities(
        query=query,
        session=session,
    )
