# Roadmap

## Now (current iteration)

- [ ] **Click analytics endpoint** — users can create links but can't see counts yet; this
  closes the loop on the core value prop → [features/click-analytics.md](features/click-analytics.md)

## Next

- Custom slug validation (reserved words, profanity, length limits).
- Rate limiting on the create endpoint.
- Simple web UI for creating links (currently API-only).

## Later / maybe

- `click_events` retention/rollup job (table grows unbounded — see architecture rough edges).
- Geo/device breakdown (explicitly out of product scope today; promote only if asked).

## Recently shipped

- _2026-05-12_ — Redirect endpoint with fire-and-forget click logging.
- _2026-05-10_ — Create-link API with random Base62 slugs and API-key auth.
