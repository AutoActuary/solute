# SOLUTE-MANAGED: tests for Solute activation and injected policy.

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / "plugins/solute/scripts/solute_hook.py"
SPEC = importlib.util.spec_from_file_location("solute_hook", HOOK_PATH)
assert SPEC and SPEC.loader
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


class HookTests(unittest.TestCase):
    def event(self, model: str, prompt: str = "Fix the failing tests") -> dict[str, str]:
        return {
            "hook_event_name": "UserPromptSubmit",
            "model": model,
            "prompt": prompt,
        }

    def test_activates_for_current_and_future_sol_slugs(self) -> None:
        for model in ("gpt-5.6-sol", "gpt-5.7-sol", "vendor-sol-preview", "sol"):
            with self.subTest(model=model):
                self.assertTrue(HOOK.should_activate(self.event(model)))

    def test_does_not_activate_for_other_models(self) -> None:
        for model in ("gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.5", ""):
            with self.subTest(model=model):
                self.assertFalse(HOOK.should_activate(self.event(model)))

    def test_optout_is_case_insensitive_and_accepts_skill_forms(self) -> None:
        prompts = (
            "Don't use /solute for this one",
            "DO NOT USE SOLUTE",
            "Please don't use $solute today",
        )
        for prompt in prompts:
            with self.subTest(prompt=prompt):
                self.assertFalse(HOOK.should_activate(self.event("gpt-5.6-sol", prompt)))

    def test_subprocess_emits_policy_as_hook_json(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HOOK_PATH)],
            input=json.dumps(self.event("gpt-5.6-sol")),
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Use Luna xhigh", context)
        self.assertIn("Don't use /solute", context)
        self.assertNotIn("`delegation-guide.md`", context)
        self.assertIn(str(HOOK.guide_path()), context)

    def test_subprocess_is_silent_when_disabled(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HOOK_PATH)],
            input=json.dumps(self.event("gpt-5.6-terra")),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
