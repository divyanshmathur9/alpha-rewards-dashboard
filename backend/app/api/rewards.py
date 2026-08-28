from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models import Reward
from app.schemas.api import BalanceResponse, RedemptionResponse, RedeemRequest, RewardItem
from app.services.rewards import get_balance, redeem_reward

router = APIRouter(prefix="/api/rewards", tags=["rewards"])


@router.get("/balance", response_model=BalanceResponse)
def balance(session: Session = Depends(get_session)):
    return BalanceResponse(balance=get_balance(session))


@router.get("", response_model=list[RewardItem])
def list_rewards(session: Session = Depends(get_session)):
    rewards = session.scalars(select(Reward).order_by(Reward.cost)).all()
    return [RewardItem.model_validate(reward, from_attributes=True) for reward in rewards]


@router.post("/redeem", response_model=RedemptionResponse)
def redeem(payload: RedeemRequest, session: Session = Depends(get_session)):
    reward, balance_after = redeem_reward(session, payload.reward_id)
    return RedemptionResponse(balance=balance_after, reward=RewardItem.model_validate(reward, from_attributes=True))

