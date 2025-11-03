from typing import Any

from httpx import AsyncClient, HTTPStatusError, RequestError
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from prices.constants import MAX_RECORDS_PER_ASSET, TIME_OUT_COINGECKO_GET_PRICES
from prices.exceptions import PriceRequestError, PriceStatusError
from prices.models import PriceHistory


async def fetch_crypto_prices(coins: list[str] | None = None) -> Any:
    """
    Получает текущие цены криптовалют из CoinGecko.

    Args:
        coins (list[str] | None): список ID монет (например, ["bitcoin", "ethereum"])
    """

    if not coins:
        return {}

    async with AsyncClient(timeout=TIME_OUT_COINGECKO_GET_PRICES) as async_client:
        try:
            response = await async_client.get(
                url=settings.COINGECKO_PRICE_URL,
                params={
                    "ids": ",".join(coins),
                    "vs_currencies": "usd",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as e:
            raise PriceStatusError(
                f"CoinGecko API error: {e.response.status_code}", status_code=400
            ) from e
        except RequestError as e:
            raise PriceRequestError(
                f"Network error while calling CoinGecko: {e}", status_code=500
            ) from e
        return response.json()


async def save_prices_to_db(db: AsyncSession, crypto_prices: dict) -> None:
    """
    Сохраняет в БД данные о ценах на монеты.

    Args:
        db (AsyncSession): Сессия БД
        crypto_prices (dict): Данные по ценам крипты
    """
    records = []
    for asset, price in crypto_prices.items():
        if "usd" in price:
            records.append(PriceHistory(asset_id=asset, price_usd=price["usd"]))
    db.add_all(records)
    await db.commit()


async def clean_old_prices_by_asset(db: AsyncSession, asset_id: str) -> None:
    """
    Удаляет старые записи, если их больше MAX_RECORDS_PER_ASSET.

    Args:
        db (AsyncSession): Сессия БД
        asset_id (str): Тип монеты
    """
    keep_ids = (
        select(PriceHistory.id)
        .where(PriceHistory.asset_id == asset_id)
        .order_by(PriceHistory.created_at.desc())
        .limit(MAX_RECORDS_PER_ASSET)
    )
    delete_query = delete(PriceHistory).where(
        (PriceHistory.asset_id == asset_id) & (~PriceHistory.id.in_(keep_ids))
    )
    await db.execute(delete_query)
