from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import ses_dep
from ..all_cruds.def_crud import delete_article_session, delete_user_session

router = APIRouter()


#* USERS RELATED


#?delete
@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    await delete_user_session(session = session, user_id = user_id)
    return f"{user_id} user is deleted (including theirs articles)"



#* ARTICLES RELATED


#?delete
@router.delete("/delete_aritcle/{article_id}")
async def delete_article(article_id: int, session: AsyncSession = ses_dep):
    await delete_article_session(session = session, article_id = article_id)
    return f"{article_id} article is deleted"