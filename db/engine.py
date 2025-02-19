from contextlib import asynccontextmanager
from os import getenv, path
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from load_dotenv import load_dotenv

from .base import Base

SRC_PATH = Path(__file__).parent.parent

load_dotenv(path.join(SRC_PATH, 'secrets.env'))

DB_PASSWORD_FILE = getenv('DB_PASSWORD_FILE')
if DB_PASSWORD_FILE is None:
    DB_PASSWORD_FILE = path.join(SRC_PATH, 'db_password.txt')


def get_db_password(file):
    with open(file=file, mode='r', encoding='UTF-8') as f:
        return f.read()


DB_URL = (
    f"postgresql+asyncpg://"
    f"{getenv('DB_USER')}:{get_db_password(DB_PASSWORD_FILE)}@"
    f"{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
)

engine = create_async_engine(url=DB_URL, echo=True, pool_size=100)

AsyncSessionMaker = async_sessionmaker(engine,
                                        expire_on_commit=False,
                                        class_=AsyncSession)


@asynccontextmanager
async def get_db():
    async with AsyncSessionMaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def db_session(func):
    async def wrapper(*args, **kwargs):
        async with get_db() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # rm if drop not needed
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
