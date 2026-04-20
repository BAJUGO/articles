from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..mod_sch import ArticleSchema, ArticleCreate, ArticlePatch
from ..core import ses_dep
from ..all_cruds.def_crud import delete_article_session, delete_user_session, update_article_session


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


@router.put("/chacnge_article/{article_id}")
async def change_article(article_id: int, new_article: ArticleCreate, session: AsyncSession = ses_dep):
    return await update_article_session(session = session, article_id = article_id, article_in = new_article)


@router.patch("/chacnge_article/{article_id}")
async def change_article(article_id: int, new_article: ArticlePatch, session: AsyncSession = ses_dep):
    return await update_article_session(session = session, article_id = article_id, article_in = new_article)