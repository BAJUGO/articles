from fastapi import APIRouter
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..back_backend.pre_post import redis_dep

from ..mod_sch.models import User
from ..mod_sch.schemas import UserSchema, UserCreate, ArticleCreate

from ..all_cruds.def_crud import add_article_session
from ..all_cruds.cached_crud import get_users_cached, get_user_by_id_cached, get_article_by_id_cached, get_articles_cached
from ..all_cruds.rel_crud import (get_articles_of_user_session,
                                  get_user_of_article_session,
                                  get_articles_of_all_users_session)

from .auth_router import user_dep

from ..core import ses_dep


router = APIRouter()

#* USERS_RELATED


#?get
@router.get("/all_users", dependencies = [user_dep] )
async def get_all_users(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_users_cached(session=session, redis = redis, second_key_arg="all")


@router.get("/user_by_id/{user_id}", dependencies = [user_dep])
async def get_user_by_id(user_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_user_by_id_cached(session = session, redis=redis, user_id = user_id)


@router.get("/user_by_article_id/{article_id}", dependencies = [user_dep])
async def get_user_of_article(article_id: int, session: AsyncSession = ses_dep):
    return await get_user_of_article_session(session = session, article_id = article_id)


#* ARTICLES_RELATED


#?get
@router.get("/all_articles", dependencies = [user_dep])
async def get_all_articles(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_articles_cached(session=session, redis=redis, second_key_arg="all")


@router.get("/all_articles_with_users", dependencies = [user_dep])
async def get_all_articles_with_users(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_articles_of_all_users_session(session=session)

@router.get("/article_by_id/{article_id}", dependencies = [user_dep])
async def get_article_by_id(article_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_article_by_id_cached(session = session, redis=redis, article_id = article_id)

#?post
@router.post("/article", dependencies = [user_dep])
async def add_article(article: ArticleCreate, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await add_article_session(session = session, article_in = article)


@router.get("/articles_of_user/{user_id}", dependencies = [user_dep])
async def get_articles_of_user(user_id: int, session: AsyncSession = ses_dep):
    articles =  await get_articles_of_user_session(session = session, user_id = user_id)
    return {f"{user_id} user articles are:": articles}

