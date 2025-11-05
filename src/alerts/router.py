from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from alerts.schemas import AlertCreate, AlterResponse
from alerts.service import create_alert
from database.session import get_db

router = APIRouter()


@router.post("/", response_model=AlterResponse)
async def create_alert_endpoint(
    alert: AlertCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    return await create_alert(alert, db)
