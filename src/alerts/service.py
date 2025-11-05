from sqlalchemy.ext.asyncio import AsyncSession

from alerts.models import Alert
from alerts.schemas import AlertCreate, AlterResponse


async def create_alert(alert: AlertCreate, db: AsyncSession) -> Alert:
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    await db.commit()
    await db.refresh(db_alert)
    return db_alert
