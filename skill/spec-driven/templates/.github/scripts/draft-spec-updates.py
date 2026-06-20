#!/usr/bin/env python3
"""
Draft spec updates after a PR merge using Claude.
Called by .github/workflows/spec-update.yml.
Writes updated spec files in place; signals has_changes via GITHUB_OUTPUT.
"""
import json
import os
import sys
import urllib.request
import urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PR_NUMBER = os.environ.get("PR_NUMBER", "unknown")
PR_TITLE = os.environ.get("PR_TITLE", "")
PR_BODY = os.environ.get("PR_BODY", "")
GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "")

SPEC_FILES = [
    "specs/product.md",
    "specs/architecture.md",
    "specs/roadmap.md",
    "specs/decisions.md",
    "specs/repo-map.md",
    "specs/team.md",
]

# Truncate diff to stay well within token limits
MAX_DIFF_CHARS = 12_000


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_output(key, value):
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as f:
            # Use multiline delimiter for values that may contain newlines
            delimiter = "EOF_" + key.upper()
            f.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")
    else:
        print(f"OUTPUT {key}={value}")


def call_claude(messages, system):
    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 4096,
        "system": system,
        "messages": messages,
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Claude API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    if not API_KEY:
        print("ANTHROPIC_API_KEY not set — skipping spec update", file=sys.stderr)
        write_output("has_changes", "false")
        return

    diff = read_file("/tmp/pr.diff") or ""
    if not diff.strip():
        print("Empty diff — nothing to update")
        write_output("has_changes", "false")
        return

    if not os.path.isdir("specs"):
        print("No specs/ directory found — skipping")
        write_output("has_changes", "false")
        return

    # Read current spec files
    specs = {p: c for p in SPEC_FILES if (c := read_file(p))}
    if not specs:
        print("No spec files found — skipping")
        write_output("has_changes", "false")
        return

    specs_block = "\n\n".join(f"=== {p} ===\n{c}" for p, c in specs.items())
    truncated_diff = diff[:MAX_DIFF_CHARS]
    if len(diff) > MAX_DIFF_CHARS:
        truncated_diff += f"\n... (diff truncated at {MAX_DIFF_CHARS} chars)"

    system = """\
You are a spec maintenance assistant. After a PR merges, you draft minimal, accurate
updates to the spec files so they stay in sync with the code.

Rules:
- Only update files where something genuinely changed.
- Lean hardest on decisions.md — any technical choice made in this PR, and any approach
  that was tried and rejected, belongs there using the existing decision template format.
- Keep changes tight: append or adjust, never rewrite from scratch.
- Preserve all existing content; only add or modify what the PR actually changes.
- If a file needs no update, omit it entirely.
- Return ONLY a valid JSON object — no markdown fences, no other text."""

    prompt = f"""\
PR #{PR_NUMBER} just merged: "{PR_TITLE}"

PR description:
{PR_BODY[:2000] if PR_BODY else "(none)"}

Diff:
{truncated_diff}

Current spec files:
{specs_block}

Draft minimal updates to reflect what this PR changed. Return this JSON shape:
{{
  "updates": [
    {{
      "file": "specs/decisions.md",
      "content": "... full updated file content ..."
    }}
  ],
  "summary": "One sentence describing what changed and which spec files were updated."
}}

If nothing needs updating, return: {{"updates": [], "summary": "No spec updates needed."}}"""

    print(f"Calling Claude for PR #{PR_NUMBER}: {PR_TITLE}")
    raw = call_claude([{"role": "user", "content": prompt}], system)

    # Strip accidental markdown fences
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:])
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3].rstrip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse Claude response: {e}", file=sys.stderr)
        print(f"Response (first 500 chars): {raw[:500]}", file=sys.stderr)
        sys.exit(1)

    updates = result.get("updates", [])
    summary = result.get("summary", "No spec updates needed.")

    print(f"Summary: {summary}")

    if not updates:
        write_output("has_changes", "false")
        return

    for update in updates:
        path = update.get("file", "")
        content = update.get("content", "")
        if not path or not content:
            continue
        # Safety: only write inside specs/
        if not path.startswith("specs/"):
            print(f"Skipping unexpected path: {path}", file=sys.stderr)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        print(f"Updated: {path}")

    write_output("has_changes", "true")
    write_output("summary", summary)


if __name__ == "__main__":
    main()
