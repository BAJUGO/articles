from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import ses_dep
from ..mod_sch import Article
from ..all_cruds.def_crud import delete_article_session

router = APIRouter()


#* USERS RELATED






#* ARTICLES RELATED


#?delete
@router.delete("/delete_aritcle/{article_id}")
async def delete_article(article_id: int, session: AsyncSession = ses_dep):
    return await delete_article_session(session = session, article_id = article_id)