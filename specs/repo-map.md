# Repo Map

## Top-level layout

```
ai-context-kit/
  kit/                    The distributable kit — teams copy this into their project
  skill/spec-driven/      Claude Code skill for automating kit workflows
  example/quicklink/      Worked example with all specs filled in
  specs/                  This repo's own specs (dog-fooding the kit)
  README.md               Public docs and setup guide
```

## kit/ — what teams copy

```
kit/
  specs/
    product.md            What / who / why
    team.md               Ownership, decision-making, cadence
    architecture.md       System map
    roadmap.md            Planned work
    decisions.md          Choices made + rejected alternatives
    repo-map.md           Where things live
    features/
      _TEMPLATE.md        Copy per feature
  .github/
    workflows/
      spec-update.yml     GitHub Action: draft spec updates on PR merge
    scripts/
      draft-spec-updates.py  Calls Claude API, writes updated files
  CLAUDE.md               AI entry point → points to specs/
  .cursorrules            Same, for Cursor
  RITUALS.md              Session start / close-out prompts
```

## skill/ — Claude Code add-on

```
skill/spec-driven/
  SKILL.md                Skill definition and workflow
  templates/              Mirrors kit/ — used by /setup command
```
