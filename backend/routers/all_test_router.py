from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core import ses_dep

router = APIRouter(prefix="/tests", tags=["Tested"])

@router.get("/all_articles")
async def get_all_articles(session: AsyncSession = ses_dep):
    pass