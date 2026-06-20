# CLAUDE.md

<!-- ADOPTING THE KIT: if your repo already had a CLAUDE.md, do NOT overwrite it with this
     file. Keep your existing one and paste the "Read these first" + "Rules" sections below
     into it. This template is only a starting point for repos with no CLAUDE.md yet. -->

> Thin pointer. The real context lives in [`/specs`](specs/). Don't duplicate it here —
> keep this file short so it never goes stale.

## Read these first (session-start hydrate)

At the start of every session, read, in order:

1. [`specs/product.md`](specs/product.md) — what we're building and why
2. [`specs/team.md`](specs/team.md) — who owns what and how decisions get made
3. [`specs/architecture.md`](specs/architecture.md) — the system map (~90s skim)
4. [`specs/repo-map.md`](specs/repo-map.md) — where things live
5. [`specs/roadmap.md`](specs/roadmap.md) — what's "now"
6. [`specs/decisions.md`](specs/decisions.md) — **what we already rejected, and why — do not re-suggest these**
7. The relevant [`specs/features/<name>.md`](specs/features/) for the task at hand

Then confirm your understanding in 3-4 lines before writing code.

## Rules

- Treat `specs/decisions.md` as binding. If you think a rejected approach should be
  reconsidered, say so explicitly and cite the decision — don't silently re-propose it.
- Respect the constraints/invariants in `specs/architecture.md`.
- PM owns *what + why + how-we-validate*; you draft the *how* from the architecture; the dev confirms.

## Close-out ritual

When a chunk of work is done, run the iteration close-out in [`RITUALS.md`](RITUALS.md):
draft the doc updates (decisions, architecture, roadmap, feature outcome) from the
diff + this conversation, and hand them to the human to edit. Keep it cheap (~2 min).
