from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from ..back_backend.pre_post import redis_dep

from ..mod_sch.models import User
from ..mod_sch.schemas import UserSchema, UserCreate

from ..all_cruds.def_crud import adder_session
from ..all_cruds.cached_crud import get_users_cached, get_user_by_id_cached

from ..core import ses_dep


router = APIRouter(prefix="/tests", tags=["Tested"])


@router.get("/all_users")
async def get_all_users(session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_users_cached(session=session, redis = redis, second_key_arg="all")


@router.get("/user_by_id/{user_id}")
async def get_user_by_id(user_id: int, session: AsyncSession = ses_dep, redis: Redis = redis_dep):
    return await get_user_by_id_cached(session = session, redis=redis, user_id = user_id)



