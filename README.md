# Alpha Rewards Dashboard

A polished spending and rewards dashboard built for the Digital Alpha full-stack assessment.

## Stack

- Next.js, React, TypeScript, custom CSS
- FastAPI, SQLAlchemy, PostgreSQL 18
- Docker Compose for local PostgreSQL

## Run locally

Start PostgreSQL from the project root:

```bash
docker compose up -d postgres
```

Seed the schema and supplied 10,000-row dataset:

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python scripts/seed.py
PYTHONPATH=. .venv/bin/uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000.

If the API runs on a different host or port, create `frontend/.env.local` with
`NEXT_PUBLIC_API_URL=http://your-api-host:8000` before starting Next.js.

## API

`GET /api/transactions`, `GET /api/rewards/balance`, `GET /api/rewards`, `POST /api/rewards/redeem`, and `GET /api/analytics`.

## Status

Done: PostgreSQL schema/seed, transaction API with search/filter/pagination/sorting, analytics API, rewards validation and redemption, responsive dashboard, searchable/filterable table, spending insights, reward catalogue, and transaction details.

The supplied dataset is seeded deterministically and duplicate source IDs are preserved with stable suffixes.
