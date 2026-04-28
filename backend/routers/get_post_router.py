from fastapi import APIRouter
from redis.asyncio import Redis
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.embeddings import get_embedding
from ..services.weaviate_index import connect_weaviate, ensure_collection, COLLECTION_NAME

import weaviate.classes as wvc



from ..back_backend.pre_post import redis_dep

from ..mod_sch.models import User, Article
from ..mod_sch.schemas import UserSchema, UserCreate, ArticleCreate, ArticleSearch

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
@router.get("/articles/get_articles", dependencies = [user_dep])
async def get_all_articles(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    articles = await get_articles_cached(session=session, redis=redis, second_key_arg="all")
    return {"items": articles if articles else ''}


@router.get("/all_articles_with_users", dependencies = [user_dep])
async def get_all_articles_with_users(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_articles_of_all_users_session(session=session)

@router.get("/articles/{article_id}", dependencies = [user_dep])
async def get_article_by_id(article_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    article =  await get_article_by_id_cached(session = session, redis=redis, article_id = article_id)
    return {"items": [article] if article else []}


@router.get("/articles/user/{user_id}", dependencies = [user_dep])
async def get_articles_of_user(user_id: int, session: AsyncSession = ses_dep):
    articles =  await get_articles_of_user_session(session = session, user_id = user_id)
    return {"items": articles if articles else ''}


#?post
@router.post("/articles/add_article")
async def add_article(article: ArticleCreate, session: AsyncSession = ses_dep, user = user_dep):
    article.user_id = user.id
    added_article =  await add_article_session(session = session, article_in = article)
    return {"items": [added_article] if added_article else []}


@router.post("/search")
async def search_article(payload: ArticleSearch, session: AsyncSession = ses_dep, user = user_dep):
    query_vector = get_embedding(payload.query)

    with connect_weaviate() as client:
        ensure_collection(client)
        collection = client.collections.use(COLLECTION_NAME)

        result = collection.query.near_vector(
            near_vector=query_vector,
            limit=2,
            filters=wvc.query.Filter.by_property("user_id").equal(str(payload.user_id)),
        )

        articles_ids = [int(obj.properties["article_id"]) for obj in result.objects]

        if not articles_ids:
            return []

        rows = await session.execute(
            select(Article).where(Article.id.in_(articles_ids))
        )
        articles_by_id = {a.id: a for a in rows.scalars().all()}

        return [articles_by_id[i] for i in articles_ids if i in articles_by_id]

