#!/usr/bin/env python3
"""
Build a close-out prompt from a merged PR's diff + current specs,
and write it to /tmp/issue-body.md for the Action to post as a GitHub issue.
No API key required.
"""
import os

PR_NUMBER = os.environ.get("PR_NUMBER", "?")
PR_TITLE = os.environ.get("PR_TITLE", "")
PR_BODY = os.environ.get("PR_BODY", "")

SPEC_FILES = [
    "specs/product.md",
    "specs/team.md",
    "specs/architecture.md",
    "specs/roadmap.md",
    "specs/decisions.md",
    "specs/repo-map.md",
]

MAX_DIFF_CHARS = 8_000
MAX_SPECS_CHARS = 6_000


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


def main():
    diff = read_file("/tmp/pr.diff") or ""
    if not diff.strip():
        print("Empty diff — no issue needed")
        return

    if not os.path.isdir("specs"):
        print("No specs/ directory — skipping")
        return

    # Collect specs within total budget
    specs_parts = []
    total = 0
    for path in SPEC_FILES:
        content = read_file(path)
        if not content:
            continue
        remaining = MAX_SPECS_CHARS - total
        if remaining <= 0:
            break
        chunk = content[:remaining]
        if len(content) > remaining:
            chunk += "\n... (truncated)"
        specs_parts.append(f"=== {path} ===\n{chunk}")
        total += len(chunk)

    if not specs_parts:
        print("No spec files found — skipping")
        return

    truncated_diff = diff[:MAX_DIFF_CHARS]
    if len(diff) > MAX_DIFF_CHARS:
        truncated_diff += f"\n... (diff truncated at {MAX_DIFF_CHARS} chars)"

    specs_block = "\n\n".join(specs_parts)
    pr_desc_line = f"\nPR description: {PR_BODY[:400]}" if PR_BODY.strip() else ""

    prompt = f"""\
Close-out for merged PR #{PR_NUMBER}: "{PR_TITLE}"{pr_desc_line}

DIFF:
```diff
{truncated_diff}
```

CURRENT SPECS:
{specs_block}

---

Draft minimal updates to the spec files that reflect what this PR changed.

Rules:
- Only update files where something genuinely changed.
- Lean hardest on decisions.md — any choice made or approach rejected in this PR belongs there, using the existing decision template.
- Keep changes tight: append or adjust, never rewrite from scratch.
- Return a short updated section (or full file if small) per file that needs changing.
- If a file needs no update, skip it entirely.\
"""

    issue_body = f"""\
## Spec close-out: PR #{PR_NUMBER} — {PR_TITLE}

Paste the prompt below into **[claude.ai](https://claude.ai)**, apply the suggested edits to your `specs/` files, then close this issue.

> **For best results:** upload your `specs/` files as attachments in claude.ai before pasting — it gives Claude the full untruncated context.

---

<details>
<summary><strong>Prompt — click to expand, then copy all</strong></summary>

```
{prompt}
```

</details>

---

**Steps:**
1. Open [claude.ai](https://claude.ai) in a new conversation
2. *(Recommended)* attach your `specs/` folder files
3. Expand the prompt above, copy it, paste it
4. Apply the suggested edits to `specs/`
5. Close this issue
"""

    with open("/tmp/issue-body.md", "w") as f:
        f.write(issue_body)

    print(f"Close-out issue body written for PR #{PR_NUMBER}: {PR_TITLE}")


if __name__ == "__main__":
    main()
