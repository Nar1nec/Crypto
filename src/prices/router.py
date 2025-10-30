from fastapi import APIRouter, HTTPException, Query

from prices.exceptions import BasePriceException
from prices.schemas import PriceResponse
from prices.service import fetch_crypto_prices

router = APIRouter()


@router.get("/latest_prices", response_model=PriceResponse)
async def get_latest_prices(
    symbols: list[str] = Query(
        default=["bitcoin", "ethereum"],
        description="Список ID криптовалют (например, bitcoin, ethereum).",
    ),
) -> PriceResponse:
    try:
        result = await fetch_crypto_prices(symbols)
    except BasePriceException as e:
        raise HTTPException(detail=e.message, status_code=e.status_code) from e
    return PriceResponse(data=result)
