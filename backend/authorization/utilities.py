import bcrypt

from fastapi import Depends, Form, HTTPException
from pydantic import EmailStr
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import ses_dep
from ..mod_sch.models import Author


def hash_password(password: str) -> bytes:
    plain_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_bytes, salt)
    return hashed_pw


def verify_password(plain_pw: str, hashed_pw: bytes) -> bool:
    byte_pw = plain_pw.encode()
    return bcrypt.checkpw(byte_pw, hashed_pw)


async def authenticate_user(
        session: AsyncSession = ses_dep,
        email: EmailStr = Form(...),
        password: str = Form(...),
):
    stmt = Select(Author).where(Author.email == str(email))
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=404, detail="Email or password is incorrect not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Email or password is incorrect not found")
    return user