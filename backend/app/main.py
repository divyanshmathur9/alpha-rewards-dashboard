from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, rewards, transactions
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title="Alpha Rewards API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transactions.router)
app.include_router(rewards.router)
app.include_router(analytics.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

