from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models import Transaction
from app.schemas.api import TransactionItem, TransactionPage

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=TransactionPage)
def list_transactions(
    search: Optional[str] = None,
    category: Optional[List[str]] = Query(default=None),
    status: Optional[List[str]] = Query(default=None),
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    min_amount: Optional[float] = Query(default=None, ge=0),
    max_amount: Optional[float] = Query(default=None, ge=0),
    sort_by: str = Query(default="date", pattern="^(date|amount)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=10, le=100),
    session: Session = Depends(get_session),
):
    filters = []
    if search:
        filters.append(Transaction.merchant.ilike(f"%{search.strip()}%"))
    if category:
        filters.append(Transaction.category.in_(category))
    if status:
        filters.append(Transaction.status.in_([item.upper() for item in status]))
    if date_from:
        filters.append(Transaction.occurred_at >= date_from)
    if date_to:
        filters.append(Transaction.occurred_at <= date_to)
    if min_amount is not None:
        filters.append(Transaction.amount >= min_amount)
    if max_amount is not None:
        filters.append(Transaction.amount <= max_amount)

    total = session.scalar(select(func.count()).select_from(Transaction).where(*filters)) or 0
    sort_column = Transaction.occurred_at if sort_by == "date" else Transaction.amount
    ordering = sort_column.asc() if sort_order == "asc" else sort_column.desc()
    rows = session.scalars(
        select(Transaction)
        .where(*filters)
        .order_by(ordering.nullslast(), Transaction.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return TransactionPage(items=[TransactionItem.model_validate(row, from_attributes=True) for row in rows], total=total, page=page, page_size=page_size)


@router.get("/{transaction_id}", response_model=TransactionItem)
def get_transaction(transaction_id: str, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionItem.model_validate(transaction, from_attributes=True)
