# Spec-Driven Development Kit

A simple way to give AI coding assistants (Claude, Cursor, Copilot, and friends) lasting
**memory of your product** — so every session doesn't start from a blank slate.

The result: you stop re-explaining what you're building every time, and the AI stops
suggesting ideas your team already tried and rejected.

## The idea in 30 seconds

AI assistants forget everything between sessions. Each conversation starts cold. The
costly thing you lose is *context*: what the product is, why it's built the way it is, and
**what you already tried, rejected, and why.**

This kit keeps that context as a handful of short, plain-English notes (Markdown files) in
a folder called `specs/` inside your project. At the end of each work session, the AI
drafts quick updates to those notes and you approve them — so the memory stays current
without much effort. Any AI tool reads the same notes: **one brain, many readers.**

You don't need to be technical to maintain this. The files are just notes you write and edit.

## What's in this repo

```
kit/        The kit itself — the templates you copy into your own project.
skill/      An optional add-on for Claude Code that automates the routine.
example/    A small worked example with every note filled in, so you can see what "good" looks like.
```

The kit also includes a GitHub Action that opens a draft PR with AI-drafted spec updates every time a PR merges. [See setup below.](#4-optional-auto-draft-spec-updates-on-pr-merge)

### `kit/` — the part you copy into your project

```
specs/
  product.md       What it is, who it's for, why it matters.
  team.md          Who owns what, how decisions get made, sprint cadence. Used by the AI and the GitHub Action.
  architecture.md  A one-page map of how the product is built (skimmable in ~90 seconds).
  roadmap.md       What's planned, and what's being worked on right now.
  decisions.md     A log of choices made — and the options you rejected, and why. The key file.
  repo-map.md      Where things live, so the AI doesn't waste time searching.
  features/        One note per feature: what it must do, the plan, and how you'll know it worked.

CLAUDE.md / .cursorrules / .github/copilot-instructions.md
                   Tiny "start here" files — one per AI tool — that just point to specs/.

RITUALS.md         The two simple routines: start-of-session and end-of-session.

.github/
  workflows/spec-update.yml      GitHub Action: opens a draft PR with spec updates on every merge.
  scripts/draft-spec-updates.py  The script the Action runs (calls Claude, writes updated files).
```

The "start here" files are intentionally tiny. All the real content lives in `specs/` only,
so it can never drift out of sync between tools.

### `skill/` — optional automation for Claude Code

`skill/spec-driven/` is an add-on for [Claude Code](https://docs.claude.com/en/docs/claude-code)
that automates the three routines below — setup, start-of-session, and end-of-session.
Teammates on other tools can ignore it and use `kit/` directly.

## How to use it

**1. Add it to your project.** Copy everything inside `kit/` into the top level of your
project. From this repo's folder, that's:

```bash
cp -R kit/. /path/to/your/project/
```

> **⚠️ Already have a `CLAUDE.md`, `.cursorrules`, or `.github/copilot-instructions.md`?**
> First, check exactly which files would be overwritten:
>
> ```bash
> TARGET=/path/to/your/project
> find kit -type f | while read f; do
>   dest="$TARGET/${f#kit/}"
>   [ -f "$dest" ] && echo "would overwrite: ${f#kit/}"
> done
> ```
>
> Then use this safe copy instead — any conflicts land as `filename.kit-new` next to your
> originals so nothing is lost:
>
> ```bash
> TARGET=/path/to/your/project
> find kit -type f | while read f; do
>   dest="$TARGET/${f#kit/}"
>   mkdir -p "$(dirname "$dest")"
>   if [ -f "$dest" ]; then
>     cp "$f" "${dest}.kit-new"
>     echo "conflict → ${dest}.kit-new"
>   else
>     cp "$f" "$dest"
>   fi
> done
> ```
>
> Diff each `.kit-new` file against your original, copy in what you need, then delete
> the `.kit-new` files.

Then fill in `product.md`, and the tables in `architecture.md` and `repo-map.md`. Add any
decisions you already know to `decisions.md`. (If you use the Claude Code add-on, it can
draft these from your existing code for you.)

**2. Start of each session (~1–2 min).** Ask the AI to read the `specs/` notes and summarize
where things stand. The "start here" file already tells it how. Now it's caught up.

**3. End of each session (~2 min).** Ask the AI to update the notes based on what just
happened — especially any new decisions or rejected ideas. You skim and approve.
**This step is the whole point — keep it quick, and the notes stay alive.**

The exact prompts to copy-paste are in [`kit/RITUALS.md`](kit/RITUALS.md).

**4. (Optional) Auto-prompt spec close-out on PR merge.**

The kit ships a GitHub Action that watches for merged PRs and opens a GitHub issue
with a ready-to-paste close-out prompt. No API key or extra cost — it works with
your existing claude.ai subscription.

Setup takes one minute:

1. **Fill in `specs/team.md`** — the Action includes it in the prompt for better context.

2. **That's it.** The workflow (`.github/workflows/spec-update.yml`) was copied when you
   ran `cp -R kit/.` in step 1. On the next PR merge to `main`, an issue appears titled
   `Spec close-out: PR #N — <title>`.

When the issue appears: open claude.ai, optionally attach your `specs/` files, paste
the prompt from the issue, apply the suggested edits, close the issue.

> The prompt leans hardest on `decisions.md` since that's the highest-value file.
> The whole flow takes about 2 minutes.

## Who does what

The product owner writes *what* to build, *why*, and *how you'll know it worked*. The AI
drafts *how* to build it, based on the architecture notes. The developer confirms. Feature
specs are written *with* the AI, *from* the existing notes — then edited by a human.

## Why it works

- **The memory lives with the project, not in one tool** — it survives switching tools and onboarding new people.
- **The rejected-ideas log compounds** — every session, it gets harder for any AI to waste your time on dead ends.
- **Quick beats perfect** — the only way this fails is if the notes go stale, so the routine is built to take about two minutes.

New to the example? Start here: [`example/quicklink/`](example/quicklink/).

## License

[MIT](LICENSE) — free to use, copy, and adapt. Built for a PM group chat; shared in case
it's useful to you too.
