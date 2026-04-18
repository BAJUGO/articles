import json
from functools import wraps
from typing import Callable

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .def_crud import get_users_session, get_user_by_id_session


def cache_response_wrapper(ttl: int, namespace: str, key_builder: Callable[[dict], str] | None = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # При желании могу написать чтобы редис брался не как один из kwargs, а как state из request, и просто
            # передовать request, но хули разница я не знаю
            redis: Redis | None = kwargs.get("redis")
            if not redis or not key_builder:
                return await func(*args, **kwargs)
            key = key_builder(kwargs) if key_builder else str(kwargs)
            cache_key = f"{namespace}:{key}"
            try:
                if cached := await redis.get(cache_key):
                    return json.loads(cached)
            except Exception as e:
                print(f"exception with caching! {e}")
            response = await func(*args, **kwargs)
            try:
                await redis.set(cache_key, json.dumps(response), ex=ttl)
            except Exception as e:
                print(f"exception with caching! {e}")
            return response
        return wrapper
    return decorator


@cache_response_wrapper(ttl=60, namespace="users", key_builder= lambda kw: str(kw["second_key_arg"]))
async def get_users_cached(session: AsyncSession, redis: Redis | None, second_key_arg: str = "all"):
    return await get_users_session(session = session)


@cache_response_wrapper(ttl=60, namespace="users", key_builder= lambda kw: str(kw["user_id"]))
async def get_user_by_id_cached(session: AsyncSession, redis: Redis | None, user_id: int):
    return await get_user_by_id_session(session = session, user_id = user_id)