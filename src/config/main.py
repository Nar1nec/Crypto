from pydantic import Field
from pydantic_settings import BaseSettings

from config.env_config import DatabaseSettings


class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)  # type: ignore

    COINGECKO_PRICE_URL: str


settings = Settings()  # type: ignore
