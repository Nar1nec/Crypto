from fastapi import FastAPI

from prices.router import router as prices_router

app = FastAPI(title="Crypto Price Tracker")

app.include_router(prices_router, prefix="/api/v1/prices", tags=["Prices"])
