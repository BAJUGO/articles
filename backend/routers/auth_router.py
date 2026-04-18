from typing import Annotated

from ..core import ses_dep
from ..all_cruds.def_crud import register_user
from .. import authorization as auth
from fastapi import APIRouter, Response, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from ..mod_sch.schemas import AuthorCreate


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/create_token", tags=["Auth"])
async def create_token(response: Response, user = Depends(auth.authenticate_user)):
    data = {"sub": str(user.id), "name": user.name, "role": user.role, "id": user.id}
    auth.set_new_tokens(data=data, response=response)
    return {"status": "oke"}


@router.get("/for_users_only", tags=["Auth"])
async def for_users_only(user_token: auth.AccessTokenData = Depends(auth.get_current_user_access_token)):
    return f"Hello, user! Your role is {user_token.role}. Your ID is {user_token.id}"


@router.post("/register", tags=["Auth"])
async def register(user: AuthorCreate, session: AsyncSession = ses_dep):
    await register_user(user_in=user, session = session)