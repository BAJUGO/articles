from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import json_body, json_to_dict_or_pyd_session
from ..authorization import admin_dep
from ..mod_sch import ArticleSchema, ArticleCreate, ArticlePatch, UserPatch
from ..core import ses_dep
from ..all_cruds.def_crud import (delete_article_session,
                                  delete_user_session,
                                  update_article_session,
                                  change_user_info_session,
                                  change_user_role_session)

from .auth_router import user_dep


router = APIRouter()


#* USERS RELATED


#?delete
@router.delete("/users/{user_id}", dependencies = [user_dep])
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    await delete_user_session(session = session, user_id = user_id)
    return f"{user_id} user is deleted (including theirs articles)"

#?update
@router.patch("/change_user/{user_id}", dependencies = [user_dep])
async def change_user(user_id: int, changes: UserPatch, session: AsyncSession = ses_dep):
    return await change_user_info_session(session = session, user_id = user_id, changes = changes)


@router.patch("/change_user_role/{user_id}", dependencies = [admin_dep])
async def change_user_role(user_id: int, new_role: str, session: AsyncSession = ses_dep):
    return await change_user_role_session(session = session, user_id = user_id, new_role = new_role)



#* ARTICLES RELATED

#?delete
@router.delete("/articles/{article_id}", dependencies = [user_dep])
async def delete_article(article_id: int, session: AsyncSession = ses_dep):
    await delete_article_session(session = session, article_id = article_id)
    return f"{article_id} article is deleted"



#?update
# @router.put("/articles/{article_id}", dependencies = [user_dep])
# async def change_article(article_id: int, changes: ArticleCreate, session: AsyncSession = ses_dep):
#     return await update_article_session(session = session, article_id = article_id, changes = changes)

#! there is no sense in upper one, but it's just a possibility to show that I actually can write function like this

@router.patch("/articles/{article_id}", dependencies = [user_dep])
async def change_article(article_id: int, changes_json: json_body, session: AsyncSession = ses_dep):
    changes = await json_to_dict_or_pyd_session(body = changes_json, key_to_extract="update_body")
    return await update_article_session(session = session, article_id = article_id, changes = ArticlePatch(**changes))