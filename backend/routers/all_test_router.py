from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from ..mod_sch.models import Author
from ..mod_sch.schemas import AuthorSchema, AuthorCreate
from ..all_cruds.def_crud import get_authors_session, adder_session, get_author_by_id_session
from ..core import ses_dep


router = APIRouter(prefix="/tests", tags=["Tested"])

@router.get("/all_authors")
async def get_all_authors(session: AsyncSession = ses_dep):
    return await get_authors_session(session = session)


@router.get("/author_by_id/{author_id}")
async def get_author_by_id(author_id: int, session: AsyncSession = ses_dep):
    return await get_author_by_id_session(session = session, author_id = author_id)

@router.post("/add_author")
async def add_author(obj: AuthorCreate, session: AsyncSession = ses_dep):
    return await adder_session(session=session, model_type=Author, obj_to_add=obj, to_return_object=True)



