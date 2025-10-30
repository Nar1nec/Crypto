from typing import Dict
from pydantic import BaseModel

class PriceItem(BaseModel):
    usd: float

class PriceResponse(BaseModel):
    data: Dict[str, PriceItem]