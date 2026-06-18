# Repo Map

## Directory guide

| Path | What's here | Touch this when... |
|------|-------------|--------------------|
| `app/` | the FastAPI application | adding behavior |
| `app/routes/` | endpoint handlers (`links.py`, `redirect.py`) | adding/changing an endpoint |
| `app/db/` | `schema.sql`, connection helper | changing the data model |
| `tests/` | pytest suite | adding any feature (write the test here) |

## Key files

| File | Role |
|------|------|
| `app/main.py` | app entry point, wires routes |
| `app/slugs.py` | Base62 slug generation (see Decision 001) |
| `app/auth.py` | API-key check for write endpoints |
| `app/db/schema.sql` | `links` and `click_events` tables |

## Where to make common changes

- **Add an API endpoint:** new handler in `app/routes/`, register it in `app/main.py`.
- **Add a DB migration:** edit `app/db/schema.sql` (no migration tool yet — small project).
- **Change config / env:** `app/config.py` reads `DATABASE_URL`, `API_KEY`.
- **Add a test:** `tests/test_<area>.py`, run with `pytest`.

## Conventions

- Routes stay thin; logic lives in module functions (`slugs.py`, etc.) so it's testable.
- Every endpoint has at least one happy-path and one failure test.
