# Rituals

Two rituals keep the specs alive. The first is cheap and you do it every session.
The second is the whole game: **if the close-out isn't cheap, the docs go stale and
the kit dies.** So the rule is — the AI drafts, the human just edits.

---

## Ritual 1 — Session start (hydrate) · ~1-2 min

Goal: the AI stops starting "from zero." Run this at the top of every session.

**Human:** point the AI at the specs (the entry file — `CLAUDE.md` / `.cursorrules` /
`copilot-instructions.md` — already says to read them). A simple prompt:

> Hydrate from /specs, then tell me in 3-4 lines: what this product is, what's "now"
> on the roadmap, and any decisions relevant to today's task. Flag anything stale.

**AI reads, in order:** `product.md` → `architecture.md` → `repo-map.md` →
`roadmap.md` → `decisions.md` → the relevant `features/<name>.md`.

**AI confirms** understanding in 3-4 lines and names any rejected approaches that are
relevant (so they don't get re-proposed). Then you work.

---

## Ritual 2 — Iteration close-out (the close-out) · ~2 min

Goal: capture what changed so the next session inherits it. Run when a chunk of work
is done (a feature, a fix, the end of a session) — **before** the context is lost.

### Step 1 — AI drafts the updates (this is the cheap part)

Prompt the AI:

> Close-out: from our diff and this conversation, draft updates to the specs. Show me
> a short diff per file, nothing else to edit yet:
> - **decisions.md** — any decision we made, and crucially anything we TRIED and
>   REJECTED, with the why. Use the decision template.
> - **architecture.md** — only if a component, data flow, or tech choice changed.
> - **roadmap.md** — move shipped items to "Recently shipped", re-rank what's next.
> - **features/<name>.md** — fill the "Outcome" section.
> - **repo-map.md** — only if the layout changed.
> Keep each edit tight. Don't rewrite; append/adjust.

The AI proposes concrete edits. It should lean hardest on **decisions.md** — the
rejected-and-why entries are the highest-value thing produced all session.

### Step 2 — Human edits (≤2 min)

Skim the proposed edits. Cut fluff, fix anything wrong, approve. Don't perfect it —
a slightly rough living doc beats a pristine dead one.

### Step 3 — Plan the next iteration

One line: what's next and why. Update `roadmap.md` "Now". If the next thing is a new
feature, copy `features/_TEMPLATE.md` → `features/<name>.md` and have the PM fill
requirements + validation up front.

---

## Why this works

- **Context lives in the repo, not a tool.** Any AI (Claude, Cursor, Copilot) reads
  the same `/specs`. One brain, many readers.
- **The rejected-alternatives log compounds.** Every close-out, it gets a little
  harder for any AI to waste your time re-suggesting dead ends.
- **Cheap beats perfect.** The only failure mode is staleness. Keeping the close-out
  to ~2 min of human effort is what prevents it.
