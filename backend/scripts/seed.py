"""Create the Alpha Rewards schema and load the supplied transaction dataset."""

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Optional

from sqlalchemy import select

from app.core.database import Base, SessionLocal, engine
from app.models import Reward, Transaction, Wallet

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions_DA.json"
COIN_CAP_PER_TRANSACTION = 100

REWARDS = [
    {"id": "coffee-credit", "title": "Coffee credit", "description": "₹150 off your next coffee order.", "cost": 180, "tone": "peach"},
    {"id": "mobile-topup", "title": "Mobile top-up", "description": "₹250 prepaid recharge credit.", "cost": 320, "tone": "blue"},
    {"id": "weekend-cashback", "title": "Weekend cashback", "description": "₹400 cashback on your next payment.", "cost": 520, "tone": "lilac"},
    {"id": "amazon-voucher", "title": "Amazon voucher", "description": "₹750 Amazon shopping voucher.", "cost": 900, "tone": "gold"},
    {"id": "travel-credit", "title": "Travel credit", "description": "₹1,000 toward your next trip.", "cost": 1250, "tone": "mint"},
]


def parse_timestamp(value: object) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000 if value > 10_000_000_000 else value, tz=timezone.utc)
    text = str(value).strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc)
    except ValueError:
        return None


def normalise_category(value: object) -> str:
    text = str(value or "").strip()
    return text if text and text.lower() != "none" else "Other"


def load_transactions() -> tuple[list[dict], int]:
    with DATA_PATH.open() as source:
        raw_items = json.load(source)

    rows = []
    balance = 0
    id_counts = {}
    for item in raw_items:
        amount = Decimal(str(item.get("amount", 0))).quantize(Decimal("0.01"))
        status = str(item.get("status", "PENDING")).upper()
        if status == "SUCCESS" and amount > 0:
            balance += min(int(amount // 100), COIN_CAP_PER_TRANSACTION)
        source_id = str(item["id"])
        id_counts[source_id] = id_counts.get(source_id, 0) + 1
        stored_id = source_id if id_counts[source_id] == 1 else "{}-{:02d}".format(source_id, id_counts[source_id])
        rows.append(
            {
                "id": stored_id,
                "occurred_at": parse_timestamp(item.get("timestamp")),
                "merchant": str(item.get("merchant") or "Unknown merchant").strip(),
                "category": normalise_category(item.get("category")),
                "amount": amount,
                "currency": str(item.get("currency") or "INR").upper(),
                "status": status,
                "payment_method": str(item.get("payment_method") or "Unknown"),
            }
        )
    return rows, balance


def main() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    rows, balance = load_transactions()
    with SessionLocal.begin() as session:
        session.bulk_insert_mappings(Transaction, rows)
        session.add(Wallet(id=1, balance=balance))
        session.bulk_insert_mappings(Reward, REWARDS)
    print(f"Seeded {len(rows):,} transactions and a {balance:,}-coin opening balance.")


if __name__ == "__main__":
    main()
