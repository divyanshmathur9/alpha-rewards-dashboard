from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    occurred_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), index=True)
    merchant: Mapped[str] = mapped_column(String(140), index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), index=True)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    status: Mapped[str] = mapped_column(String(16), index=True)
    payment_method: Mapped[str] = mapped_column(String(40))


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Reward(Base):
    __tablename__ = "rewards"

    id: Mapped[str] = mapped_column(String(48), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    cost: Mapped[int] = mapped_column(Integer)
    tone: Mapped[str] = mapped_column(String(24))


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reward_id: Mapped[str] = mapped_column(ForeignKey("rewards.id"))
    cost: Mapped[int] = mapped_column(Integer)
    redeemed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
