from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from ..back_backend.pre_post import redis_dep

from ..mod_sch.models import Author
from ..mod_sch.schemas import AuthorSchema, AuthorCreate

from ..all_cruds.def_crud import adder_session
from ..all_cruds.cached_crud import get_authors_cached, get_author_by_id_cached

from ..core import ses_dep


router = APIRouter(prefix="/tests", tags=["Tested"])


@router.get("/all_authors")
async def get_all_authors(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_authors_cached(session=session, redis = redis, second_key_arg="all")


@router.get("/author_by_id/{author_id}")
async def get_author_by_id(author_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_author_by_id_cached(session = session, redis=redis, author_id = author_id)



