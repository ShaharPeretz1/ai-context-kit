# Architecture

## System in one diagram

```
[ client / curl ] --POST /api/links--> [ FastAPI app ] --> [ Postgres ]
[ browser ] ------GET /{slug}--------> [ FastAPI app ] --(lookup)--> [ Postgres ]
                                             |
                                             +--(async)--> click_events table
```

## Components

| Component | Responsibility | Lives in |
|-----------|----------------|----------|
| API app | create links, redirect, expose JSON API | `app/main.py`, `app/routes/` |
| Storage | links + click_events tables | Postgres, schema in `app/db/schema.sql` |
| Slug generator | make short, collision-resistant slugs | `app/slugs.py` |
| Auth | API-key check on write endpoints | `app/auth.py` |

## Data flow

1. **Create:** `POST /api/links {url, slug?}` → validate → generate slug if absent →
   insert into `links` → return short URL.
2. **Resolve:** `GET /{slug}` → look up in `links` → 301 redirect → fire-and-forget insert
   into `click_events` (never blocks the redirect).

## Key tech choices

| Choice | Why | See |
|--------|-----|-----|
| FastAPI (Python) | team knows it; async redirect path is cheap | — |
| Postgres | one store for links + events; we already run it | [decisions.md](decisions.md#decision-002--store-clicks-in-postgres-not-redis) |
| Base62 random slugs | short, no coordination needed | [decisions.md](decisions.md#decision-001--random-base62-slugs-over-auto-increment-ids) |

## Constraints & invariants

- The redirect path must never block on analytics. Click logging is fire-and-forget.
- Slugs are immutable once created (links are shared; they can't change target silently —
  deletion only).
- Write endpoints require an API key; the redirect endpoint is public.

## Known rough edges

- No connection pooling tuning yet; fine under current load, revisit before >100 req/s.
- `click_events` grows unbounded — needs a retention/rollup job eventually (roadmap "Later").
