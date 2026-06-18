# Decisions

> A running log of choices made — and the options rejected, and why. (Newest first.)

## Template (copy for each new decision)

```
### Decision NNN — <short title>
- **Date:** YYYY-MM-DD
- **Status:** accepted | replaced by Decision XXX | reversed
- **Decision:** what we're doing.
- **Why:** the driving reason.
- **Rejected alternatives:**
  - <option> — why we said no.
- **Revisit if:** the condition that would make us reopen this.
```

---

### Decision 002 — Store clicks in Postgres, not Redis
- **Date:** 2026-05-12
- **Status:** accepted
- **Decision:** Click events go into a Postgres `click_events` table.
- **Why:** One datastore to run and back up. Volume is low; durability matters more than
  write latency, and the redirect doesn't wait on the write anyway.
- **Rejected alternatives:**
  - **Redis counters** — fast, but adds a second piece of infra to operate and back up,
    and we'd lose per-event detail we may want later. Not worth it at our scale.
  - **Append to a log file** — cheap, but querying it for click counts is painful and
    doesn't survive a container restart cleanly.
- **Revisit if:** sustained write rate exceeds ~100/s, at which point a buffer in front of
  Postgres (or Redis) becomes worth the operational cost.

### Decision 001 — Random Base62 slugs over auto-increment IDs
- **Date:** 2026-05-10
- **Status:** accepted
- **Decision:** Generate 7-char random Base62 slugs; retry on the rare collision.
- **Why:** Short, non-guessable, and require no central counter — keeps create path stateless.
- **Rejected alternatives:**
  - **Auto-increment integer encoded to Base62** — makes total link count and creation
    order trivially enumerable by anyone (`/1`, `/2`, ...). Privacy leak, rejected.
  - **Hash of the URL** — same URL collapses to same slug, which breaks custom slugs and
    leaks that two users shortened the same link.
- **Revisit if:** collision retries become measurable (would mean we've outgrown 7 chars).
