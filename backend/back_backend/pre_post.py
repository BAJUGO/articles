from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from redis.asyncio import Redis

from ..core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"ALL SETTINGS: {settings}")
    redis_client = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True)

    app.state.redis = redis_client

    try:
        yield
    finally:
        await redis_client.aclose()


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis

redis_dep = Depends(get_redis)

