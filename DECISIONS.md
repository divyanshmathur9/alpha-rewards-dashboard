# Technical decisions

- Next.js App Router and TypeScript keep the frontend aligned with the brief.
- FastAPI routes, SQLAlchemy models, and a small rewards service separate HTTP concerns from business rules.
- PostgreSQL 18 runs through Docker Compose for a reproducible local setup.
- The transaction API paginates at 12 rows and filters in SQL, keeping the browser responsive with 10,000 records.
- The table is hand-built with semantic HTML and custom CSS, as required by the assignment.

