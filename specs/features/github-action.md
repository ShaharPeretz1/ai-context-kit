# Feature: GitHub Action — auto-draft spec updates on PR merge

## What it must do

- Trigger automatically when any PR merges to `main` or `master`
- Get the merged PR's diff
- Read all current `specs/` files for context
- Call Claude to draft minimal, targeted updates to the relevant spec files
- Open a **draft PR** (not auto-merge) with the proposed changes for human review
- Require only one setup step from the team: add `ANTHROPIC_API_KEY` as a repo secret

## Non-goals

- Never write outside `specs/` (hard safety check in the script)
- Never auto-merge — always a draft PR for human approval
- No external service, no dashboard, no accounts

## Plan

Implemented as two files teams copy from `kit/`:
- `.github/workflows/spec-update.yml` — the Action definition
- `.github/scripts/draft-spec-updates.py` — zero-dependency Python script (stdlib only)

The script calls the Anthropic Messages API directly via `urllib`, returns JSON with
updated file contents, writes them in place, and signals `has_changes` to the Action.

## How we'll know it worked

- A draft PR appears within ~2 min of a PR merge
- `decisions.md` is the most-updated file (it has the highest-value content)
- The draft is accurate enough that a human reviewer needs <2 min to approve it
- Zero false positives: if nothing relevant changed, no PR is opened
- no API key required — works with claude.ai subscription
