from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from .mixins import AuthorRelationshipMixin
from ..core import Base


class Author(Base):
    __tablename__ = "authors"
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))

    articles: Mapped[list["Article"]] = relationship(back_populates="author")



class Article(AuthorRelationshipMixin, Base):
    __tablename__ = "articles"
    _author_back_populates = "articles"

    title: Mapped[str] = mapped_column(String(50))
    main_text: Mapped[str] = mapped_column()
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)



