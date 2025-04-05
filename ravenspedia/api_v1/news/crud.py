from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.news.schemes import NewsCreate, NewsGeneralInfoUpdate
from ravenspedia.core import db_helper, TableNews


# Fetch all news articles, sorted by creation date (newest first).
async def get_news(
    session: AsyncSession,
) -> list[TableNews]:
    statement = select(TableNews).order_by(TableNews.created_at.desc())
    news = await session.scalars(statement)
    return list(news)


# Fetch a single news article by its ID.
async def get_news_by_id(
    news_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableNews:
    news = await session.scalar(select(TableNews).where(TableNews.id == news_id))
    if news is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"News {news_id} not found",
        )
    return news


# Create a new news article in the database.
async def create_news(
    session: AsyncSession,
    news_in: NewsCreate,
) -> TableNews:
    news: TableNews = TableNews(**news_in.model_dump())
    try:
        session.add(news)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A news with such data already exists",
        )
    return news


# Update general information of an existing news article.
async def update_general_news_info(
    session: AsyncSession,
    news: TableNews,
    news_update: NewsGeneralInfoUpdate,
) -> TableNews:
    # Update fields that are provided in the update data
    for field, value in news_update.model_dump(exclude_unset=True).items():
        setattr(news, field, value)
    await session.commit()
    return news


# Delete a news article from the database
async def delete_news(
    session: AsyncSession,
    news: TableNews,
) -> None:
    await session.delete(news)
    await session.commit()
