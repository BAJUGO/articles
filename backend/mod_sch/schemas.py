from pydantic import BaseModel, Field, ConfigDict
from pydantic import EmailStr


class BaseReturn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


#*Authors


class UserPatch(BaseModel):
    name: str | None = Field(None, max_length=30)
    last_name: str | None = Field(None, max_length=30)
    password: str | None = Field(None, max_length=50)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5, max_length=50)
    name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)


class UserSchema(BaseReturn, BaseModel):
    name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)


#* Articles


class ArticlePatch(BaseModel):
    title: str | None = Field(None, max_length=50)
    main_text: str | None = None
    user_id: int | None = None


class ArticleCreate(BaseModel):
    title: str = Field("untitled", max_length=50)
    main_text: str
    user_id: int | None = None


class ArticleSchema(BaseReturn, ArticleCreate):
    pass



