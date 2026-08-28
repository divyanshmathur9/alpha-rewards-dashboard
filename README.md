# Alpha Rewards Dashboard

A full-stack spending and rewards dashboard built for the Digital Alpha full-stack assessment. It turns the supplied 10,000-transaction dataset into a fast, filterable activity view with analytics and redeemable rewards.

## Highlights

- Custom transaction table with merchant search, category/status filters, date range, amount range, sorting, and pagination
- Transaction detail drawer with payment metadata and reference ID
- Category spending insights and a points balance
- Reward catalogue with live redemption validation and balance updates
- Seeded PostgreSQL database containing the supplied dataset

## Stack

- Next.js, React, TypeScript, custom CSS
- FastAPI, SQLAlchemy, PostgreSQL 18
- Docker Compose for local PostgreSQL

## Run locally

Prerequisites: Docker Desktop, Node.js 20+ and Python 3.9+.

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

### Transaction query parameters

The transactions endpoint supports `search`, `category`, `status`, `date_from`, `date_to`, `min_amount`, `max_amount`, `sort_by`, `sort_order`, `page`, and `page_size`.

## Project structure

- `frontend/` — Next.js dashboard
- `backend/` — FastAPI application, database models, API routes, and seed script
- `database/` — schema notes
- `ASSUMPTIONS.md` — stated product/data assumptions
- `DECISIONS.md` — architecture decisions and trade-offs
- `AI-USAGE.md` — concise disclosure of AI assistance

## Verification

Frontend linting: `npm --prefix frontend run lint`.

Backend seed test: `cd backend && PYTHONPATH=. .venv/bin/pytest`.

## Status

Done: PostgreSQL schema/seed, transaction API with search/filter/pagination/sorting, analytics API, rewards validation and redemption, responsive dashboard, searchable/filterable table, spending insights, reward catalogue, and transaction details.

The supplied dataset is seeded deterministically and duplicate source IDs are preserved with stable suffixes. The application is designed for local demonstration with Docker Compose, the FastAPI server, and the Next.js server running together.
