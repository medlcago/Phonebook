import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.models import Base
from config import config

engine = create_async_engine(url=config.db.url)
async_session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def delete_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(create_database())
