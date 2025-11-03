import asyncio

from database.session import AsyncSessionLocal
from prices.service import (
    clean_old_prices_by_asset,
    fetch_crypto_prices,
    save_prices_to_db,
)


class PriceCollector:
    TRACKED_ASSETS = ["bitcoin", "ethereum", "tether", "binancecoin", "solana"]
    TIME_OUT_PRICE_COLLECTOR_SEC = 300

    async def start(self) -> None:
        """
        Автоматический сборщик цен на крипту.
        """
        while True:
            try:
                async with AsyncSessionLocal() as db:
                    prices = await fetch_crypto_prices(self.TRACKED_ASSETS)
                    await save_prices_to_db(db, prices)
                    for asset in self.TRACKED_ASSETS:
                        await clean_old_prices_by_asset(db, asset)
            except Exception:
                pass
            await asyncio.sleep(self.TIME_OUT_PRICE_COLLECTOR_SEC)
