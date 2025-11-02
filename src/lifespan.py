from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.models import Base
from database.session import engine
from prices.models import PriceHistory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    print("Таблицы для создания:", Base.metadata.tables.keys())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
