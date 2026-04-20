from typing import Annotated

import bcrypt

from fastapi import Depends, Form, HTTPException, Body
from pydantic import EmailStr
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import ses_dep
from ..mod_sch.models import User

from ..utils import json_body, json_to_dict_or_pyd_session


def hash_password(password: str) -> bytes:
    plain_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_bytes, salt)
    return hashed_pw


def verify_password(plain_pw: str, hashed_pw: bytes) -> bool:
    byte_pw = plain_pw.encode()
    return bcrypt.checkpw(byte_pw, hashed_pw)


async def authenticate_user(
        user_body: json_body,
        session: AsyncSession = ses_dep,
        # Это просто не нужно по причине того, что формат ввода будет определён в frontend части
        # now that I think about it, я понимаю, что при помощи формы намного меньше всякой херни приходится делать
        # везде, по типу перевода json в славянские dict и всё такое, но мне, если честно, в падлу что-то менять
        # email: EmailStr = Form(...),
        # password: str = Form(...),
):
    user_from_json = await json_to_dict_or_pyd_session(body = user_body, key_to_extract = "user_body")
    stmt = Select(User).where(User.email == str(user_from_json["email"]))
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=404, detail="Email or password is incorrect not found")
    if not verify_password(user_from_json["password"], user.hashed_password):
        raise HTTPException(status_code=404, detail="Email or password is incorrect not found")
    return user