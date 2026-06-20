# Architecture

## System in one diagram

```
kit/                   Templates teams copy into their own project
  specs/               Markdown files — the persistent memory layer
  .github/             GitHub Action + Python script (auto spec-update on PR merge)
  CLAUDE.md            AI entry point — points to specs/
  .cursorrules         Same, for Cursor
  RITUALS.md           Session start/close-out prompts

skill/spec-driven/     Claude Code skill — automates setup + session rituals
  SKILL.md             Skill entry point
  templates/           Mirrors kit/ — copied to user project on /setup

example/quicklink/     Worked example with all specs filled in
README.md              Public docs
```

## Components

| Component | Responsibility | Lives in |
|-----------|----------------|----------|
| spec templates | The memory layer — product, arch, roadmap, decisions, team | `kit/specs/` |
| AI entry files | Point each AI tool at specs/ | `kit/CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md` |
| GitHub Action | Opens draft PR with spec updates on every merge | `kit/.github/workflows/spec-update.yml` |
| spec-update script | Calls Claude API, writes updated files, signals the Action | `kit/.github/scripts/draft-spec-updates.py` |
| Claude Code skill | Automates setup, session start, close-out via `/spec-driven` | `skill/spec-driven/` |

## Data flow

1. **Session start:** AI reads `CLAUDE.md` → reads all `specs/` files → confirms understanding → works.
2. **PR merge:** Action gets diff → Python script calls Claude API with diff + specs → Claude returns JSON with updated file contents → script writes files → Action opens draft PR.
3. **Close-out (manual):** Human prompts AI with RITUALS.md close-out prompt → AI drafts spec edits → human approves.

## Key tech choices

| Choice | Why | See |
|--------|-----|-----|
| Markdown files in repo | Zero infra, any AI can read, version-controlled, editable by non-devs | decisions.md#001 |
| No SaaS / accounts | Adopters keep their data; simpler adoption | decisions.md#002 |
| Python + urllib for Action script | Zero pip dependencies — works out of the box on ubuntu-latest | decisions.md#003 |
| Draft PRs not auto-merge | Humans stay in the loop; prevents bad auto-commits to main | decisions.md#004 |

## Constraints & invariants

- The Action script must only write to `specs/` — path safety check is in the script.
- `kit/` and `skill/spec-driven/templates/` must stay in sync (same files).
- The close-out ritual must be achievable in ~2 min of human effort.
