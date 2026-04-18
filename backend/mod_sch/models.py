from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import String, ARRAY

from .mixins import UserRelationshipMixin
from ..core import Base


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column()
    role: Mapped[str] = mapped_column()

    articles: Mapped[list["Article"]] = relationship(back_populates="user")


class Article(UserRelationshipMixin, Base):
    __tablename__ = "articles"
    _user_back_populates = "articles"

    title: Mapped[str | None] = mapped_column(String(50), server_default="untitled")
    main_text: Mapped[str] = mapped_column()
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)



