import json

from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..authorization.utilities import hash_password

from ..mod_sch.schemas import UserSchema, ArticleSchema
from ..mod_sch.models import User, Article

from fastapi.exceptions import HTTPException

T = TypeVar("T", User, Article)
P = TypeVar("P", bound=BaseModel)


# transform model to schema functions

async def model_to_schema(model: T, schema: type[P]) -> P:
    return schema.model_validate(model).model_dump()

async def models_to_schemas(models: list[T], schema: type[P]) -> list[P]:
    return [schema.model_validate(model).model_dump() for model in models]


# Base operations used further in more complex functions

#* GETTERS
async def getter_session(session: AsyncSession, model_type: type[T]) -> list[T]:
    stmt = Select(model_type).order_by(model_type.id)
    objs = list(await session.scalars(stmt))
    if objs:
        return objs
    raise HTTPException(status_code=404, detail=f"{model_type.__name__} not found")


async def getter_by_id_session(session: AsyncSession, model_type: type[T], obj_id: int) -> T:
    obj = await session.get(model_type, obj_id)
    if obj:
        return obj
    raise HTTPException(status_code=404, detail=f"{model_type.__name__} not found")


#* ADDERS
async def adder_session(session: AsyncSession, model_type: type[T], obj_to_add: P, to_return_object: bool = False) -> T | None:
    obj = model_type(**obj_to_add.model_dump())
    session.add(obj)
    await session.commit()
    return obj if to_return_object else None



#! COMPLEX ONES

#* USERS
async def get_users_session(session: AsyncSession):
    return await models_to_schemas(await getter_session(session = session, model_type = User), schema = UserSchema)


async def get_user_by_id_session(session: AsyncSession, user_id: int):
    return await model_to_schema(await getter_by_id_session(session = session, model_type = User, obj_id=user_id), schema=UserSchema)


#* ARTICLES
async def get_articles_session(session: AsyncSession):
    return await models_to_schemas(await getter_session(session = session, model_type = Article), schema = ArticleSchema)


async def get_article_by_id_session(session: AsyncSession, article_id: int):
    return await model_to_schema(await getter_by_id_session(session = session, model_type = Article, obj_id = article_id), schema=ArticleSchema)


#* USERS
async def register_user(user_in, session: AsyncSession):
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hash_password(user_in.password), role="user")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return await model_to_schema(model = user, schema = UserSchema)