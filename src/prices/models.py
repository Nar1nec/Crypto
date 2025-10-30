from sqlalchemy.orm import Mapped, mapped_column

from common import BaseFieldsMixin


class PriceHistory(BaseFieldsMixin):
    __tablename__ = "price_history"

    asset_id: Mapped[str] = mapped_column(index=True)
    price_usd: Mapped[float]
