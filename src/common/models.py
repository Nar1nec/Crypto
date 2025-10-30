from datetime import datetime
from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    pass

class TimestampFieldsMixin(MappedAsDataclass):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        init=False
    )

class IDFieldMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

class BaseFieldsMixin(IDFieldMixin, TimestampFieldsMixin):
    pass