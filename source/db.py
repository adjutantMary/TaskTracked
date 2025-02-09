from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv
from .models.base import Base


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR.parent, ".env")
load_dotenv(dotenv_path=env_path)

engine = create_async_engine(os.environ.get("DATABASE_URL"), echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
