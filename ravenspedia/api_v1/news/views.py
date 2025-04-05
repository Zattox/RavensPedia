from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemes import ResponseNews, NewsCreate, NewsGeneralInfoUpdate
from ravenspedia.core import db_helper, TableNews, TableUser
from ravenspedia.api_v1.auth.dependencies import get_current_admin_user

router = APIRouter(tags=["News"])


# Convert a TableNews object to ResponseNews schema for API output.
def table_to_response_form(
    news: TableNews,
) -> ResponseNews:
    return ResponseNews(
        id=news.id,
        title=news.title,
        content=news.content,
        created_at=news.created_at,
        author=news.author,
    )


# Endpoint to retrieve all news articles.
@router.get(
    "/",
    response_model=list[ResponseNews],
    status_code=status.HTTP_200_OK,
)
async def get_news(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await crud.get_news(session=session)
    return [table_to_response_form(cur) for cur in news]


# Endpoint to retrieve a single news article by ID.
@router.get(
    "/{news_id}/",
    response_model=ResponseNews,
    status_code=status.HTTP_200_OK,
)
async def get_news_by_id(
    news_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ResponseNews:
    news = await crud.get_news_by_id(news_id=news_id, session=session)
    return table_to_response_form(news)


# Endpoint to create a new news article (admin only).
@router.post(
    "/",
    response_model=ResponseNews,
    status_code=status.HTTP_201_CREATED,
)
async def create_news(
    news_in: NewsCreate,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await crud.create_news(session=session, news_in=news_in)
    return table_to_response_form(news)


# Endpoint to update a news article (admin only).
@router.patch(
    "/{news_id}/",
    response_model=ResponseNews,
    status_code=status.HTTP_200_OK,
)
async def update_general_news_info(
    news_id: int,
    news_update: NewsGeneralInfoUpdate,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    news = await crud.get_news_by_id(news_id=news_id, session=session)
    updated_news = await crud.update_general_news_info(
        session=session, news=news, news_update=news_update
    )
    return table_to_response_form(updated_news)


# Endpoint to delete a news article (admin only).
@router.delete(
    "/{news_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_news(
    news_id: int,
    admin: TableUser = Depends(get_current_admin_user),  # Ensure user is admin.
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    news = await crud.get_news_by_id(news_id=news_id, session=session)
    await crud.delete_news(session=session, news=news)
