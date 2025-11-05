from typing import Literal

from pydantic import BaseModel


class AlertCreate(BaseModel):
    asset_id: str
    condition: Literal["lte", "gte"]
    target_price: float


class AlterResponse(BaseModel):
    id: int
    asset_id: str
    condition: str
    target_price: float
    is_triggered: bool

    model_config = {"from_attributes": True}
