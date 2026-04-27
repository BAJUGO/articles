from typing import Annotated

from ..core import ses_dep
from ..all_cruds.def_crud import register_user
from .. import authorization as auth
from fastapi import APIRouter, Response, Depends, Body, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..mod_sch.schemas import UserCreate

from ..utils import json_body, json_to_dict_or_pyd_session


router = APIRouter(tags=["Auth"])

user_dep = Depends(auth.get_current_user_token)


@router.get("/initPage")
async def check_the_data(request: Request, response: Response):
    token = auth.get_current_user_token(request=request)
    if token:
        auth.set_new_tokens(data=token.model_dump(), response=response)
        response.status_code = 200
        return response
    raise HTTPException(status_code=401, detail="Unauthorized error  {happened in initPage}")


@router.get("/delete_cookies")
async def delete_cookies(request: Request, response: Response):
    if request.cookies.get("access_token") or request.cookies.get("refresh_token"):
        try:
            response.delete_cookie(key="access_token", path="/")
            response.delete_cookie(key="refresh_token", path="/")
        except Exception as e:
            pass
        response.status_code, response.content = 200, "OK"
        return response
    response.status_code = 401
    return response



@router.post("/create_token", tags=["Auth"])
async def create_token(response: Response, user = Depends(auth.authenticate_user)):
    data = {"sub": str(user.id), "name": user.name, "role": user.role, "id": user.id}
    auth.set_new_tokens(data=data, response=response)
    return {"status": "oke"}


@router.get("/for_users_only", tags=["Auth"], dependencies=[user_dep])
async def for_users_only(user_token: auth.AccessTokenData = user_dep):
    return f"Hello, {user_token.name}! Your role is {user_token.role}. Your ID is {user_token.id}"


@router.post("/register", tags=["Auth"])
async def register(user_data: UserCreate, session: AsyncSession = ses_dep):
    await register_user(user_data=user_data, session = session)
    return {"status": "oke"}