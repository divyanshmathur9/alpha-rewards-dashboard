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

## Live demo

- Frontend: https://alpha-rewards-dashboard.vercel.app
- Backend API: https://alpha-rewards-api.onrender.com

The backend is hosted on Render's free tier, so its first request after inactivity can take up to about a minute while the service wakes up.

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

## Delivery status

### Done

- PostgreSQL schema and deterministic seed for all 10,000 supplied transactions
- Server-side transaction search, combined filters, sorting, and pagination
- Transaction details, category spend insights, and rewards balance/catalogue
- Reward confirmation, validation, and immediate balance update
- Responsive Next.js frontend and deployed FastAPI/PostgreSQL backend

### Not done

- Automated coverage currently focuses on the seed path; endpoint and browser-level tests would be the next additions.
- A monthly spend-trend chart is not included; the interactive category chart is the selected analytics view.

### Known issues

- The Render free service may take up to roughly a minute to respond after a period of inactivity.
- Each Render redeploy runs the seed command so the demo starts from a clean, predictable dataset.

The supplied dataset is seeded deterministically and duplicate source IDs are preserved with stable suffixes.
