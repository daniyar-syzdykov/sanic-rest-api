from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import Base


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None
    
    def __getattr__(self, name):
        return getattr(self._session, name)
    
    async def init(self):
        user = 'postgres'
        password = '1234'
        host = 'localhost'
        port = '5432'
        db_name = 'test_assignment'
        url = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'
        self._engine = create_async_engine(url, echo=True)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async_db_session: AsyncSession = AsyncDatabaseSession()
