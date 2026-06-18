# Architecture

<!--
PURPOSE: The map of the system. Target: skimmable in ~90 seconds. This is what
lets the AI stop "trying to understand the code" and start contributing. Describe
shape and *why*, not line-by-line detail. Link to repo-map.md for where things live.
Update when components, data flow, or a key tech choice changes.
-->

## System in one diagram

<!-- A simple text diagram or bullet flow beats prose. Show the major pieces and how
data moves between them. -->
```
[ client ] --> [ api ] --> [ db ]
                  |
                  +--> [ worker / queue ]
```

## Components

<!-- One row per major component: what it does, where it lives. Keep it tight. -->

| Component | Responsibility | Lives in |
|-----------|----------------|----------|
|           |                |          |

## Data flow

<!-- The 1-3 critical paths through the system (e.g. "a request to X goes ..."). -->
1. 

## Key tech choices

<!-- Stack + the *reason* each was chosen. The reason is the valuable part — it
prevents the AI from re-litigating settled decisions. Link to decisions.md for the
full rejected-alternatives log. -->

| Choice | Why | See |
|--------|-----|-----|
|        |     | [decisions.md](decisions.md#) |

## Constraints & invariants

<!-- Things that must stay true: performance budgets, security rules, data that can
never be deleted, external SLAs, etc. The AI should treat these as hard rules. -->
- 

## Known rough edges

<!-- Tech debt and fragile areas the AI should handle with care. -->
- 
