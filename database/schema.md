# Schema overview

`transactions` stores the supplied records as typed, queryable columns. `wallets` holds the single demo user's coin balance. `rewards` is the small redeemable catalogue, and `reward_redemptions` is an immutable redemption record.

The database is created and seeded with:

```bash
cd backend
PYTHONPATH=. .venv/bin/python scripts/seed.py
```

