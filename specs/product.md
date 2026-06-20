# Product

## One-liner

A kit that gives AI coding assistants persistent memory of your product — so every
session doesn't start from a blank slate.

## Who it's for

- **Primary user:** developers and PMs using AI assistants (Claude, Cursor, Copilot)
  on real products with real teams.
- **Their job-to-be-done:** "Stop re-explaining what we're building every session, and
  stop the AI from re-suggesting approaches we already tried and rejected."

## The problem

AI assistants forget everything between sessions. The costly thing you lose is context:
what the product is, why it's built the way it is, and what you already tried and
rejected. Teams waste minutes every session on re-hydration, and hours across a project
re-litigating dead decisions.

## Value proposition

A handful of short markdown files in a `specs/` folder that any AI tool can read.
One brain, many readers. The kit provides the templates, the rituals to keep them alive,
and automation (GitHub Action) so the specs don't go stale without anyone remembering.

## Scope

- **In scope:** spec templates, session rituals, Claude Code skill, GitHub Action for
  auto-drafted spec updates on PR merge, team structure template.
- **Explicitly out of scope:** hosted SaaS, accounts, dashboards, storing any user data.
  Everything lives in the adopter's own repo.

## Success looks like

- A team installs the kit and their AI sessions stop starting cold after the first week.
- The specs stay alive for >1 month without manual effort (Action handles the close-out).
- The rejected-alternatives log in `decisions.md` prevents at least one re-litigated
  decision per sprint.
