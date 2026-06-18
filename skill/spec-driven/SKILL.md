---
name: spec-driven
description: "Automates the Spec-Driven Development kit: initialize the /specs scaffold in a repo, hydrate product context at session start, and run the iteration close-out that updates the living docs. Use when the user says 'spec-driven', 'hydrate from specs', 'init specs', 'close out', 'update the specs', or asks to set up / refresh durable product context for AI coding. Pairs with the /specs folder, the thin entry-file pointers (CLAUDE.md / .cursorrules / copilot-instructions.md), and RITUALS.md."
---

# Spec-Driven Development

Keeps durable product context in the repo so any AI tool starts each session "not from
zero." Three modes: **init**, **hydrate**, **close-out**. Figure out which the user wants,
then follow that section. When unsure, check whether `/specs` exists: no → likely init;
yes, start of work → hydrate; yes, end of work → close-out.

The source of truth is always the markdown in `/specs`. Entry files (`CLAUDE.md`,
`.cursorrules`, `.github/copilot-instructions.md`) are thin pointers — never put real
content in them.

---

## Mode 1 — Init

Scaffold the kit into a repo that doesn't have it.

1. Check for an existing `/specs`. If present, stop and switch to hydrate (don't clobber).
2. Create this structure (use the templates in this skill's `templates/` dir, or generate
   equivalents):
   ```
   specs/{product,architecture,roadmap,decisions,repo-map}.md
   specs/features/_TEMPLATE.md
   CLAUDE.md  .cursorrules  .github/copilot-instructions.md   # thin pointers
   RITUALS.md
   ```
3. **Bootstrap from the actual code** instead of leaving blanks: skim the repo and pre-fill
   `architecture.md` (components, data flow, stack) and `repo-map.md` (what lives where).
   Draft `product.md` from the README if one exists. Leave `decisions.md` mostly empty —
   it grows from real decisions — but seed Decision 001 with "adopt spec-driven dev" if useful.
4. Show the user what you filled and ask them to correct the *why* (product value,
   tech-choice reasoning) — that's the part you can't infer reliably.

## Mode 2 — Hydrate (session start)

Goal: load context in ~1-2 min so you don't start cold.

1. Read, in order: `specs/product.md` → `architecture.md` → `repo-map.md` →
   `roadmap.md` → `decisions.md` → the relevant `features/<name>.md`.
2. Report back in 3-4 lines: what the product is, what's "now" on the roadmap, and any
   decisions relevant to today's task.
3. **Explicitly name any rejected approaches** in `decisions.md` that touch today's work,
   so you don't re-propose them. Treat that file as binding: to revisit a rejected option,
   say so and cite the decision — never silently re-suggest it.
4. Flag anything that looks stale (doc disagrees with code).

## Mode 3 — Close-out (the important one — keep it cheap)

Goal: capture what changed before context is lost. **You draft; the human only edits.**
Target ~2 min of human effort.

1. Review the session: the diff (`git diff`, changed files) and this conversation.
2. Draft a **short diff per file** — propose concrete edits, don't apply silently:
   - **decisions.md** — the highest-value output. Every decision made, and crucially
     anything **tried and rejected, with the why**. Use the decision template. Append, newest first.
   - **architecture.md** — only if a component, data flow, or tech choice changed.
   - **roadmap.md** — move shipped items to "Recently shipped"; re-rank "Next".
   - **features/<name>.md** — fill the "Outcome" section (what shipped / what broke / learned).
   - **repo-map.md** — only if the layout changed.
3. Keep each edit tight; append/adjust rather than rewrite. Lean hardest on decisions.md.
4. Present the edits for the human to skim and approve. Apply once approved.
5. Plan next: update `roadmap.md` "Now" in one line. If next is a new feature, copy
   `features/_TEMPLATE.md` → `features/<name>.md` for the PM to fill requirements +
   validation up front.

---

## Principles

- **Map, not transcript.** `architecture.md` skimmable in ~90s. Small, high-signal docs.
- **One brain, many readers.** Real content in `/specs`; tool entry files just point to it.
- **Division of labor.** PM owns *what + why + how-we-validate*; you draft the *how* from
  the architecture; the dev confirms.
- **Staleness is the only failure mode.** The close-out exists to beat it — so it must stay cheap.
