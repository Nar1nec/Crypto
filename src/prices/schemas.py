from pydantic import BaseModel


class PriceItem(BaseModel):
    usd: float


class PriceResponse(BaseModel):
    data: dict[str, PriceItem]
