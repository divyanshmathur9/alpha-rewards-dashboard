from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Reward, RewardRedemption, Wallet


def get_balance(session: Session) -> int:
    wallet = session.get(Wallet, 1)
    return wallet.balance if wallet else 0


def redeem_reward(session: Session, reward_id: str) -> tuple[Reward, int]:
    reward = session.get(Reward, reward_id)
    if reward is None:
        raise HTTPException(status_code=404, detail="Reward not found")

    wallet = session.scalar(select(Wallet).where(Wallet.id == 1).with_for_update())
    if wallet is None:
        raise HTTPException(status_code=500, detail="Wallet is not initialized")
    if wallet.balance < reward.cost:
        raise HTTPException(status_code=409, detail="You do not have enough coins for this reward")

    wallet.balance -= reward.cost
    session.add(RewardRedemption(reward_id=reward.id, cost=reward.cost))
    session.commit()
    session.refresh(wallet)
    return reward, wallet.balance

