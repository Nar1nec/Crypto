from typing import Any

from httpx import AsyncClient, HTTPStatusError, RequestError

from config import settings
from prices.exceptions import PriceRequestError, PriceStatusError


async def fetch_crypto_prices(coins: list[str] | None = None) -> Any:
    """
    Получает текущие цены криптовалют из CoinGecko.

    :param coins: список ID монет (например, ["bitcoin", "ethereum"])
    :return: словарь вида {"bitcoin": {"usd": 61234.5}, ...}
    """

    if not coins:
        return {}

    async with AsyncClient(timeout=10.0) as async_client:
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
