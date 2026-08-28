# Assumptions

- This is a single demo user's wallet; authentication is outside the brief.
- Successful positive transactions earn `floor(amount / 100)` coins, capped at 100 coins per transaction.
- Duplicate source IDs are retained by adding a deterministic suffix so no supplied record is discarded.
- Missing or blank categories are shown as `Other`.
- Analytics totals include successful transactions with positive amounts only.

