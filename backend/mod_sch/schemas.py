from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(str, max_length=50)
    main_text: str = Field(str)
