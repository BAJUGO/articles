from asyncio import current_task

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from .config import settings


class DbHelper:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )

    async def session_dependency(self):
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess


db_helper = DbHelper(url=settings.db_url, echo=settings.echo)
ses_dep = Depends(db_helper.session_dependency)