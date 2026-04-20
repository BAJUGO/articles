from typing import Annotated, TypeVar
from fastapi import Body
import json

from pydantic import BaseModel

P = TypeVar("P", bound=BaseModel)

json_body = Annotated[str, Body()]


async def json_to_dict_or_pyd_session(body: json_body, key_to_extract: str, to_schema: type[P] | None = None):
    object_body_json = json.loads(body)
    object_body = object_body_json.get(key_to_extract)
    if to_schema:
        return to_schema(**object_body)
    return object_body