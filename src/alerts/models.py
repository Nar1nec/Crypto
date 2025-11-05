from sqlalchemy.orm import Mapped, mapped_column

from common.models import Base, IDFieldMixin


class Alert(Base, IDFieldMixin):
    __tablename__ = "alerts"

    asset_id: Mapped[str] = mapped_column(index=True)
    condition: Mapped[str]
    target_price: Mapped[float]
    is_triggered: Mapped[bool] = mapped_column(default=False)
