# Copilot instructions — thin pointer to /specs

The real product context lives in `/specs`. This file just points you there. Don't
duplicate spec content here; keep it short so it never goes stale.

## Read these first (session-start hydrate), in order:
1. `specs/product.md` — what we're building and why
2. `specs/architecture.md` — the system map (~90s skim)
3. `specs/repo-map.md` — where things live
4. `specs/roadmap.md` — what's "now"
5. `specs/decisions.md` — **what we already rejected, and why. Do not re-suggest these.**
6. `specs/features/<name>.md` — the spec for the current task

Then confirm understanding briefly before writing code.

## Rules
- `specs/decisions.md` is binding. To revisit a rejected approach, say so explicitly
  and cite the decision — never silently re-propose it.
- Respect the constraints/invariants in `specs/architecture.md`.
- PM owns *what + why + how-we-validate*; you draft the *how* from the architecture; the dev confirms.

## Close-out
When a chunk of work is done, follow `RITUALS.md`: draft doc updates from the diff +
conversation for the human to edit.
