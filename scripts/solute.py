#!/usr/bin/env python3
# SOLUTE-MANAGED: installer, uninstaller, and diagnostic entry point.
"""Manage the Solute marketplace and plugin without editing unrelated config."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PLUGIN = "solute"
MARKETPLACE = "solute"
MARKETPLACE_FILE = Path(".agents/plugins/marketplace.json")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def npm_codex_command(launcher: Path) -> list[str] | None:
    node_name = "node.exe" if os.name == "nt" else "node"
    node = launcher.parent / node_name
    if not node.is_file():
        resolved = shutil.which(node_name)
        node = Path(resolved) if resolved else node
    script = launcher.parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    if node.is_file() and script.is_file():
        return [str(node), str(script)]
    return None


def find_codex() -> list[str] | None:
    configured = os.environ.get("CODEX_CLI_PATH")
    if configured and Path(configured).is_file():
        path = Path(configured)
        if path.suffix.lower() in (".cmd", ".ps1"):
            return npm_codex_command(path)
        return [str(path)]
    if os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            candidates = list((Path(local) / "OpenAI/Codex/bin").glob("*/codex.exe"))
            candidates.extend((Path(local) / "OpenAI/Codex/bin").glob("codex.exe"))
            if candidates:
                return [str(max(candidates, key=lambda path: path.stat().st_mtime))]
        native = shutil.which("codex.exe")
        if native:
            return [native]
        npm_launcher = shutil.which("codex.cmd") or shutil.which("codex.ps1")
        return npm_codex_command(Path(npm_launcher)) if npm_launcher else None
    executable = shutil.which("codex")
    return [executable] if executable else None


def run_codex(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    command = find_codex()
    if command is None:
        raise RuntimeError("Codex CLI is not on PATH.")
    return subprocess.run(
        [*command, *args],
        check=check,
        text=True,
        capture_output=True,
    )


def parse_json_output(result: subprocess.CompletedProcess[str]) -> Any:
    return json.loads(result.stdout or "{}")


def marketplace_entries() -> list[dict[str, Any]]:
    result = run_codex("plugin", "marketplace", "list", "--json")
    payload = parse_json_output(result)
    return list(payload.get("marketplaces", []))


def install() -> int:
    root = repo_root()
    expected = root.resolve()
    existing = next((m for m in marketplace_entries() if m.get("name") == MARKETPLACE), None)
    if existing:
        current = Path(str(existing.get("root", ""))).resolve()
        if current != expected:
            raise RuntimeError(
                f"Marketplace '{MARKETPLACE}' already points to {current}, not {expected}. "
                "Remove or rename that marketplace before installing Solute."
            )
    else:
        run_codex("plugin", "marketplace", "add", str(root), "--json")
    run_codex("plugin", "add", f"{PLUGIN}@{MARKETPLACE}", "--json")
    print("Solute installed. Review and trust its hook in Codex, then start a new task.")
    return doctor()


def uninstall() -> int:
    plugin_result = run_codex(
        "plugin", "remove", f"{PLUGIN}@{MARKETPLACE}", "--json", check=False
    )
    market_result = run_codex(
        "plugin", "marketplace", "remove", MARKETPLACE, "--json", check=False
    )
    failures = []
    for label, result in (("plugin", plugin_result), ("marketplace", market_result)):
        message = f"{result.stdout}\n{result.stderr}".lower()
        if result.returncode and not any(
            phrase in message
            for phrase in (
                "not found",
                "unknown marketplace",
                "not installed",
                "not configured",
            )
        ):
            failures.append(f"{label}: {(result.stderr or result.stdout).strip()}")
    if failures:
        raise RuntimeError("Solute uninstall failed: " + "; ".join(failures))
    print("Solute plugin and marketplace registration removed. Start a new task.")
    return 0


def doctor() -> int:
    root = repo_root()
    required = [
        root / MARKETPLACE_FILE,
        root / "plugins/solute/.codex-plugin/plugin.json",
        root / "plugins/solute/hooks/hooks.json",
        root / "plugins/solute/scripts/solute_hook.py",
        root / "plugins/solute/scripts/solute_hook.sh",
        root / "plugins/solute/scripts/solute_hook.ps1",
        root / "plugins/solute/skills/solute/SKILL.md",
        root / "plugins/solute/skills/solute/references/policy.md",
        root / "plugins/solute/skills/solute/references/delegation-guide.md",
        root / "scripts/solute.sh",
        root / "scripts/solute.ps1",
        root / "UNINSTALL.md",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print("Missing Solute files:\n" + "\n".join(missing), file=sys.stderr)
        return 1
    if find_codex() is None:
        print("Codex CLI is not on PATH.", file=sys.stderr)
        return 1
    marketplace = json.loads((root / MARKETPLACE_FILE).read_text(encoding="utf-8"))
    manifest = json.loads(
        (root / "plugins/solute/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    if marketplace.get("name") != MARKETPLACE or manifest.get("name") != PLUGIN:
        print("Solute identifiers do not match the installer.", file=sys.stderr)
        return 1
    print("Solute doctor passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Install, remove, or check Solute.")
    parser.add_argument("command", choices=("install", "uninstall", "doctor"))
    args = parser.parse_args()
    try:
        return {"install": install, "uninstall": uninstall, "doctor": doctor}[args.command]()
    except (OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"Solute {args.command} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
