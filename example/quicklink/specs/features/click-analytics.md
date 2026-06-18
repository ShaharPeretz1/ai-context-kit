# Feature: click-analytics

## Status

in progress

## Requirements — _PM owns this_

- **Problem / motivation:** Users can create links but have no way to see how many times
  they were clicked, which is half the reason they'd self-host instead of using a plain redirect.
- **User story:** As a link owner, I want to see the click count for a link so that I can
  tell whether a campaign is working.
- **Must do:**
  - Return total click count for a given slug.
  - Require the API key (analytics are not public even though redirects are).
- **Must not do / out of scope:**
  - Geo/device/referrer breakdown (product scope says no for now).
  - Time-series charts — a single total is enough for v1.

## Validation — _PM owns this, write up front_

- **Acceptance criteria:**
  - [ ] `GET /api/links/{slug}/stats` returns `{slug, clicks}` for an existing link.
  - [ ] Returns 404 for an unknown slug.
  - [ ] Returns 401 without a valid API key.
- **Metrics / signals:** count matches the number of `click_events` rows for that slug.
- **How to test it:** create a link, hit `/{slug}` N times, assert stats returns N.

## Plan — _AI drafts from architecture.md, dev confirms_

- **Approach:** add a read endpoint that `COUNT(*)`s `click_events` for the slug. No new
  table; reuse the existing fire-and-forget logging.
- **Components touched:** `app/routes/links.py` (new handler), `app/main.py` (register).
- **Steps:**
  1. Add `GET /api/links/{slug}/stats` handler behind the API-key dependency.
  2. Query `SELECT COUNT(*) FROM click_events WHERE slug = $1`; 404 if the link doesn't exist.
  3. Tests per the acceptance criteria.
- **Risks / unknowns:** `COUNT(*)` on a growing `click_events` is fine now but ties into the
  unbounded-growth rough edge; fine for v1.
- **New decisions this introduces:** none yet (no rollup table — deferred).

## Outcome — _filled at close-out_

- **What shipped:** _(pending)_
- **What broke / surprised us:**
- **What we learned:**
- **Follow-ups → roadmap:**
