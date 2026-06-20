# Decisions

> A running log of the choices made and — most importantly — the options rejected, and why.

---

### Decision 004 — Draft PRs, not auto-merge for spec updates
- **Date:** 2026-06-20
- **Status:** accepted
- **Decision:** The GitHub Action opens a draft PR with spec updates; it never commits directly to main.
- **Why:** Spec updates drafted by AI need human review. An incorrect auto-committed spec is worse than no update — it actively misleads future sessions.
- **Rejected alternatives:**
  - Auto-commit directly to main — too risky; AI hallucinations would silently corrupt specs.
  - Push to a long-lived `spec-updates` branch — confusing; teams would ignore it.
- **Revisit if:** We add a confidence score and auto-merge only high-confidence, low-diff updates.

### Decision 003 — Zero-dependency Python script for the Action
- **Date:** 2026-06-20
- **Status:** accepted
- **Decision:** The spec-update script uses only Python stdlib (urllib, json, os) — no pip install step.
- **Why:** Fewer moving parts in CI. The anthropic SDK is convenient but adds a dependency that can break on version changes. urllib is always available on ubuntu-latest.
- **Rejected alternatives:**
  - `anthropic` Python SDK — cleaner API but requires `pip install anthropic` in the Action, slower cold start.
  - Node.js action — another runtime to maintain.
- **Revisit if:** The raw API response format changes enough to make stdlib parsing brittle.

### Decision 002 — No SaaS, no accounts, no external data storage
- **Date:** 2026-06-18
- **Status:** accepted
- **Decision:** The kit is files in a repo. No hosted service, no user accounts, no telemetry.
- **Why:** Adoption barrier stays near zero. Teams with data residency requirements can use it. No infra to maintain.
- **Rejected alternatives:**
  - Hosted dashboard for spec viewing/editing — nice UX but breaks the "zero setup" promise and requires auth.
  - Syncing specs to Notion/Confluence — useful but adds a dependency that can break and isn't needed for the core value.
- **Revisit if:** We pursue a team UI for ownership/configuration (currently tracking as a future idea).

### Decision 001 — Markdown files in the repo as the memory layer
- **Date:** 2026-06-18
- **Status:** accepted
- **Decision:** Specs are plain markdown files committed to the adopter's own repo.
- **Why:** Every AI tool can read markdown. Non-technical PMs can edit it. It's version-controlled, diffable, and requires no special tooling.
- **Rejected alternatives:**
  - YAML/JSON structured format — machine-readable but not human-friendly for PMs editing by hand.
  - Comments/annotations in code — scattered, hard for the AI to get a coherent view.
  - External knowledge base (Notion, Confluence) — adds a dependency and breaks the "one brain, many readers" goal.
- **Revisit if:** Structured format becomes necessary for programmatic integrations (e.g. Linear sync).
