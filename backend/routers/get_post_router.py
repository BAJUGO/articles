from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select


from ..back_backend.pre_post import redis_dep

from ..mod_sch.models import User
from ..mod_sch.schemas import UserSchema, UserCreate, ArticleCreate

from ..all_cruds.def_crud import add_article_session
from ..all_cruds.cached_crud import get_users_cached, get_user_by_id_cached, get_article_by_id_cached, get_articles_cached
from ..all_cruds.rel_crud import get_articles_of_user_session, get_user_of_article_session

from ..core import ses_dep


router = APIRouter(prefix="/tests", tags=["Tested"])

#* USERS_RELATED
@router.get("/all_users")
async def get_all_users(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_users_cached(session=session, redis = redis, second_key_arg="all")


@router.get("/user_by_id/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_user_by_id_cached(session = session, redis=redis, user_id = user_id)

#* ARTICLES_RELATED
@router.get("/all_articles")
async def get_all_articles(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_articles_cached(session=session, redis=redis, second_key_arg="all")


@router.get("/article_by_id/{article_id}")
async def get_article_by_id(article_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_article_by_id_cached(session = session, redis=redis, article_id = article_id)


@router.post("/article")
async def add_article(article: ArticleCreate, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await add_article_session(session = session, article_in = article)


@router.get("/articles_of_user/{user_id}")
async def get_articles_of_user(user_id: int, session: AsyncSession = ses_dep):
    return await get_articles_of_user_session(session = session, user_id = user_id)


@router.get("/user_id_by_article/{article_id}")
async def get_user_of_article(article_id: int,session: AsyncSession = ses_dep):
    return await get_user_of_article_session(session = session, article_id = article_id)