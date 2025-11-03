from datetime import datetime

from pydantic import BaseModel


class PriceItem(BaseModel):
    usd: float


class PriceResponse(BaseModel):
    data: dict[str, PriceItem]


class PriceHistoryResponse(BaseModel):
    asset_id: str
    price_usd: float
    created_at: datetime

    model_config = {"from_attributes": True}
