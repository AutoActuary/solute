# SOLUTE-MANAGED: repository consistency and uninstall breadcrumbs.

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_identifiers_and_paths_match(self) -> None:
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (ROOT / "plugins/solute/.codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(marketplace["name"], "solute")
        self.assertEqual(marketplace["plugins"][0]["name"], "solute")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/solute")
        self.assertEqual(manifest["name"], "solute")

    def test_uninstall_breadcrumbs_exist_outside_skill_context(self) -> None:
        breadcrumbs = (
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "UNINSTALL.md",
            ROOT / "plugins/solute/hooks/hooks.json",
            ROOT / "plugins/solute/scripts/solute_hook.py",
        )
        for path in breadcrumbs:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8").lower()
                self.assertIn("solute", text)
                self.assertTrue("remove" in text or "uninstall" in text)

    def test_skill_files_do_not_carry_uninstall_breadcrumbs(self) -> None:
        skill_root = ROOT / "plugins/solute/skills/solute"
        for path in skill_root.rglob("*"):
            if path.is_file():
                with self.subTest(path=path):
                    text = path.read_text(encoding="utf-8").lower()
                    self.assertNotIn("uninstall", text)
                    self.assertNotIn("plugin remove", text)

    def test_runtime_policy_stays_compact(self) -> None:
        policy = (
            ROOT / "plugins/solute/skills/solute/references/policy.md"
        ).read_text(encoding="utf-8")
        self.assertLess(len(policy), 1000)
        self.assertIn("Return only outcome", policy)
        self.assertIn("delegation-guide.md", policy)

    def test_longer_guide_is_inside_the_skill_and_not_duplicated(self) -> None:
        guide = (
            ROOT
            / "plugins/solute/skills/solute/references/delegation-guide.md"
        )
        self.assertTrue(guide.is_file())
        self.assertFalse((ROOT / "ECONOMICS.md").exists())


if __name__ == "__main__":
    unittest.main()
