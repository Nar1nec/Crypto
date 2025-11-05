from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from prices.enums import CryptoAsset
from prices.exceptions import BasePriceException
from prices.models import PriceHistory
from prices.schemas import PriceHistoryResponse, PriceResponse
from prices.service import fetch_crypto_prices

router = APIRouter()


@router.get("/latest_prices", response_model=PriceResponse)
async def get_latest_prices(
    symbols: list[str] = Query(
        default=["bitcoin", "ethereum", "tether", "binancecoin", "solana"],
        description="Список ID криптовалют.",
    ),
) -> PriceResponse:
    try:
        result = await fetch_crypto_prices(symbols)
    except BasePriceException as e:
        raise HTTPException(detail=e.message, status_code=e.status_code) from e
    return PriceResponse(data=result)


@router.get("/history/{asset_id}", response_model=list[PriceHistoryResponse])
async def get_price_history(
    asset_id: CryptoAsset, db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.asset_id == asset_id)
        .order_by(PriceHistory.created_at.desc())
        .limit(100)
    )
    return result.scalars().all()
