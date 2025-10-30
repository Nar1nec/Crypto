from unittest.mock import patch
import pytest
from prices.exceptions import PriceStatusError, PriceRequestError
from prices.service import fetch_crypto_prices
import respx
from httpx import RequestError, Response

@pytest.mark.asyncio
async def test_fetch_crypto_prices_with_empty_data():
    result = await fetch_crypto_prices()
    assert result == {}

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception_type", "status_code"),[(PriceStatusError, 400), (PriceStatusError, 500)]
)
async def test_fetch_crypto_prices_with_status_400(exception_type, status_code):
    with respx.mock:
        respx.get("https://api.coingecko.com/api/v3/simple/price").mock(return_value=Response(status_code=status_code))
    
        with pytest.raises(exception_type):
            await fetch_crypto_prices(["a", "b"])

@pytest.mark.asyncio
async def test_fetch_crypto_prices_with_status_500():
    with respx.mock:
        respx.get("https://api.coingecko.com/api/v3/simple/price").mock(side_effect=RequestError("mocked network error"))
    
        with pytest.raises(PriceRequestError):
            await fetch_crypto_prices(["a", "b"])

@pytest.mark.asyncio
async def test_fetch_crypto_prices_with_valid_data():
    with respx.mock:
        respx.get("https://api.coingecko.com/api/v3/simple/price").mock(return_value=Response(status_code=200, json={"bitcoin": {"usd": 60000}}))
        
        result = await fetch_crypto_prices(["test"])
        
        assert result == {"bitcoin": {"usd": 60000}}