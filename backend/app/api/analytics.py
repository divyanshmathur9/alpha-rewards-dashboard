from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models import Transaction
from app.schemas.api import AnalyticsResponse, CategorySpend, MonthlySpend

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsResponse)
def analytics(session: Session = Depends(get_session)):
    valid_spend = (Transaction.status == "SUCCESS", Transaction.amount > 0)
    categories = session.execute(
        select(Transaction.category, func.sum(Transaction.amount).label("amount"))
        .where(*valid_spend)
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
    ).all()
    months = session.execute(
        select(func.to_char(Transaction.occurred_at, "YYYY-MM").label("month"), func.sum(Transaction.amount).label("amount"))
        .where(*valid_spend, Transaction.occurred_at.is_not(None))
        .group_by("month")
        .order_by("month")
    ).all()
    total = session.scalar(select(func.coalesce(func.sum(Transaction.amount), 0)).where(*valid_spend)) or 0
    return AnalyticsResponse(
        total_spend=float(total),
        category_spend=[CategorySpend(category=row.category, amount=float(row.amount)) for row in categories],
        monthly_spend=[MonthlySpend(month=row.month, amount=float(row.amount)) for row in months],
    )

