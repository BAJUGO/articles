import json

from typing import TypeVar, Any

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..mod_sch.schemas import AuthorSchema
from ..mod_sch.models import Author, Article

from fastapi.exceptions import HTTPException

T = TypeVar("T", Author, Article)
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

async def get_authors_session(session: AsyncSession):
    return await models_to_schemas(await getter_session(session = session, model_type = Author), schema = AuthorSchema)


async def get_author_by_id_session(session: AsyncSession, author_id: int):
    return await model_to_schema(await getter_by_id_session(session = session, model_type = Author, obj_id=author_id), schema=AuthorSchema)