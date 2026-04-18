from pydantic import BaseModel, Field, ConfigDict
from pydantic import EmailStr


class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


#*Authors


class AuthorPatch(BaseModel):
    name: str | None = Field(None, max_length=30)
    last_name: str | None = Field(None, max_length=30)
    password: str | None = Field(None, max_length=50)


class AuthorCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=50)
    name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)


class AuthorSchema(BaseReturn, BaseModel):
    name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)



#* Articles



class ArticlePatch(BaseModel):
    title: str | None = Field(None, max_length=50)
    main_text: str | None = None
    author_id: int | None = None


class ArticleCreate(BaseModel):
    title: str = Field("untitled", max_length=50)
    main_text: str
    author_id: int


class ArticleSchema(BaseReturn, ArticleCreate):
    pass



