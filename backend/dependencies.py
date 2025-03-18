from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session 