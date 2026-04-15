from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Author

class AuthorRelationshipMixin:
    _author_back_populates: str | None = None

    @declared_attr
    def author_id(self) -> Mapped[int]:
        return mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), index=True)

    @declared_attr
    def author(self) -> Mapped["Author"]:
        return relationship("Author", back_populates=self._author_back_populates)

