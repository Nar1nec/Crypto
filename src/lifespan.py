import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.models import Base
from database.session import engine
from prices.collector import PriceCollector


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await drop_tables()
    await create_tables()

    task = asyncio.create_task(PriceCollector().start())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
