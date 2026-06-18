# Product

## One-liner

A self-hosted URL shortener that gives small teams branded short links and basic click
analytics without sending their data to a third party.

## Who it's for

- **Primary user:** developers and marketers at small companies (5-50 people) who want
  short links on their own domain.
- **Their job-to-be-done:** "Turn a long, ugly URL into a short branded one I can share,
  and tell me how many people clicked it — without paying a SaaS or leaking the data."

## The problem

Hosted shorteners (Bitly et al.) are priced per-seat, rate-limit the free tier, and own
your click data. Teams that care about data residency or just want something cheap have
to either overpay or build it themselves each time.

## Value proposition

Drop-in, self-hosted, single binary + Postgres. Branded domain, click counts, and an API,
with the data staying in your infrastructure. Boring on purpose.

## Scope

- **In scope:** create/resolve short links, custom slugs, click counting, a small JSON API, basic auth.
- **Explicitly out of scope:** A/B testing, geo/device analytics dashboards, team roles &
  permissions, link expiration campaigns. (See roadmap "Later".)

## Success looks like

- A team can self-host and create their first branded link in under 10 minutes.
- Redirects resolve in <50ms p95.
