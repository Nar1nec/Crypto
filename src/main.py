from fastapi import FastAPI

from alerts.router import router as alerts_router
from lifespan import lifespan
from prices.router import router as prices_router

app = FastAPI(title="Crypto Price Tracker", lifespan=lifespan)

app.include_router(prices_router, prefix="/api/v1/prices", tags=["Prices"])
app.include_router(alerts_router, prefix="/api/v1/alerts", tags=["Alerts"])
