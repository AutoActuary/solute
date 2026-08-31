#!/usr/bin/env python3
# SOLUTE-MANAGED: installed with the Solute plugin. Remove with `codex plugin remove solute@solute`.
"""Inject the compact Solute policy for Sol user turns."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


OPTOUT = re.compile(
    r"\b(?:do not|don't)\s+use\s+(?:/|\$)?solute\b",
    flags=re.IGNORECASE,
)


def is_sol_model(model: object) -> bool:
    slug = str(model or "").strip().lower()
    return slug == "sol" or slug.endswith("-sol") or "-sol-" in slug


def should_activate(event: dict[str, Any]) -> bool:
    return (
        event.get("hook_event_name") == "UserPromptSubmit"
        and is_sol_model(event.get("model"))
        and not OPTOUT.search(str(event.get("prompt") or ""))
    )


def policy_path() -> Path:
    return Path(__file__).resolve().parents[1] / "skills" / "solute" / "references" / "policy.md"


def guide_path() -> Path:
    return policy_path().with_name("delegation-guide.md")


def load_policy() -> str:
    policy = policy_path().read_text(encoding="utf-8").strip()
    return policy.replace("`delegation-guide.md`", f"`{guide_path()}`")


def build_output(event: dict[str, Any]) -> dict[str, Any] | None:
    if not should_activate(event):
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": load_policy(),
        }
    }


def main() -> int:
    try:
        event = json.load(sys.stdin)
        output = build_output(event)
        if output is not None:
            json.dump(output, sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
        return 0
    except Exception as exc:
        print(f"Solute hook skipped: {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
