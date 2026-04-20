from typing import TypeVar

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .def_crud import models_to_schemas, model_to_schema
from ..mod_sch import Article, User, ArticleSchema, UserSchema

# If there were articles, pages and something like that for example, and I needed to declare this attr, I would use
# InstrumentedAttribute from sqlaclhemy.orm

async def get_articles_of_all_users_session(session: AsyncSession):
    stmt = select(User).options(selectinload(User.articles))
    users = list(await session.scalars(stmt))
    result = {}
    for user in users:
        result[f"{user.id} user articles are:"] = user.articles
    return result


async def get_articles_of_user_session(session: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id).options(selectinload(User.articles))
    user = await session.scalar(stmt)
    if user:
        items = getattr(user, User.articles.key)
        return await models_to_schemas(items, ArticleSchema)
    raise HTTPException(status_code=404, detail="User not found")


async def get_user_of_article_session(session: AsyncSession, article_id: int):
    stmt = select(Article).where(Article.id == article_id).options(selectinload(Article.user))
    article = await session.scalar(stmt)
    if article:
        return await model_to_schema(article.user, UserSchema)
    raise HTTPException(status_code=404, detail="Article not found")

