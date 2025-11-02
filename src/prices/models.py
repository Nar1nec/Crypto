from sqlalchemy.orm import Mapped, mapped_column

from common import Base, BaseFieldsMixin


class PriceHistory(Base, BaseFieldsMixin):
    __tablename__ = "price_history"

    asset_id: Mapped[str] = mapped_column(index=True)
    price_usd: Mapped[float]
