from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Baza = declarative_base()

class Base(Baza):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

