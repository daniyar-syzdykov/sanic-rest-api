from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import Base
from config import DB_NAME, DB_PASSWORD, DB_PORT, DB_HOST, DB_USER


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        self._engine = create_async_engine(url)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async_db_session: AsyncSession = AsyncDatabaseSession()
