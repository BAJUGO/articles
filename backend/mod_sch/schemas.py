from pydantic import BaseModel, Field, ConfigDict

class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AuthorPatch(BaseModel):
    name: str | None = Field(None, max_length=30)
    last_name: str | None = Field(None, max_length=30)


class AuthorCreate(BaseModel):
    name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)


class AuthorSchema(BaseReturn, AuthorCreate):
    pass


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



