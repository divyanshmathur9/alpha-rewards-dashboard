from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TransactionItem(BaseModel):
    id: str
    occurred_at: Optional[datetime]
    merchant: str
    category: str
    amount: float
    currency: str
    status: str
    payment_method: str


class TransactionPage(BaseModel):
    items: list[TransactionItem]
    total: int
    page: int
    page_size: int


class RewardItem(BaseModel):
    id: str
    title: str
    description: str
    cost: int
    tone: str


class BalanceResponse(BaseModel):
    balance: int


class RedeemRequest(BaseModel):
    reward_id: str = Field(min_length=1, max_length=48)


class RedemptionResponse(BaseModel):
    balance: int
    reward: RewardItem


class CategorySpend(BaseModel):
    category: str
    amount: float


class MonthlySpend(BaseModel):
    month: str
    amount: float


class AnalyticsResponse(BaseModel):
    total_spend: float
    category_spend: list[CategorySpend]
    monthly_spend: list[MonthlySpend]
