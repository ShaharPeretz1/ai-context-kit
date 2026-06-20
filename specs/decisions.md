# Decisions

> A running log of the choices made and — most importantly — the options rejected, and why.

---

### Decision 005 — No API key: Action opens a GitHub Issue with a prompt instead of calling Claude directly
- **Date:** 2026-06-20
- **Status:** accepted — replaces Decision 004
- **Decision:** The GitHub Action builds a close-out prompt from the diff + specs and opens a GitHub Issue. The human pastes the prompt into claude.ai and applies the edits manually.
- **Why:** The Anthropic API is billed separately from Claude Max subscriptions. Requiring an API key adds friction (cost, secret setup) for users who already have a claude.ai subscription. The issue-based flow preserves the human-in-the-loop guarantee at zero extra cost.
- **Rejected alternatives:**
  - Call Claude API directly — requires a separate API key and billing; blocked by user constraint.
  - Use Haiku for low cost — still requires API key setup even at ~$1-2/month.
  - Auto-commit spec updates — removed this option entirely; human review is non-negotiable.
- **Revisit if:** A future plan tier gives API access bundled with the subscription, making the key frictionless.

### Decision 004 — Draft PRs, not auto-merge for spec updates
- **Date:** 2026-06-20
- **Status:** superseded by Decision 005
- **Decision:** ~~The GitHub Action opens a draft PR with spec updates.~~
- **Note:** Replaced when we switched from API-based to prompt-based flow. The human-in-the-loop guarantee is now enforced by the issue workflow rather than a draft PR.

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
