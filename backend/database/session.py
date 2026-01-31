from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
# Create engine with connection pooling settings for robustness
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,  # Test connections before using them to prevent SSL errors
    pool_recycle=1800,   # Recycle connections every 30 minutes
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Async engine for aiosqlite and async PostgreSQL
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

if "sqlite" in DATABASE_URL:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
elif "postgresql" in DATABASE_URL:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

async_engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800,
)

async def get_async_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session