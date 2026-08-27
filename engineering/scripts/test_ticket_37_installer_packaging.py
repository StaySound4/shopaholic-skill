#!/usr/bin/env python3
"""Test suite for Ticket 37: Validate target Skill packaging, installer safety, and multi-runtime capability.
Tests:
1. Pass: Skill structure validates cleanly, safe install creates .bak timestamped backups and diff summaries.
2. Pass: Honest multi-runtime capability declarations reflect tool-enabled vs prompt-only fallbacks.
3. Adversarial: Overwriting existing skill directory without backup raises PermissionError.
"""
import unittest, sys, tempfile, shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_packaging_installer import (
    validate_skill_package_structure,
    install_skill_safely,
    get_runtime_capability_declaration
)

class TestTicket37InstallerPackaging(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.src_skill = self.temp_dir / "src_skill"
        self.src_skill.mkdir()
        (self.src_skill / "SKILL.md").write_text("# Shopaholic Skill v1.0")
        (self.src_skill / "references" / "categories").mkdir(parents=True)
        (self.src_skill / "references" / "categories" / "coffee.md").write_text("# Coffee Playbook")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_skill_structure_and_safe_installer(self):
        """Pass path: Structure validates, safe install on existing target creates .bak backup and diff summary."""
        # 1. Validate structure
        val_res = validate_skill_package_structure(self.src_skill)
        self.assertTrue(val_res["is_valid"])
        self.assertEqual(len(val_res["issues"]), 0)

        # 2. Setup existing target with older file
        target_dir = self.temp_dir / "installed" / "skills" / "shopaholic"
        target_dir.mkdir(parents=True)
        (target_dir / "SKILL.md").write_text("# Old Version 0.9")

        # 3. Perform safe install
        install_res = install_skill_safely(self.src_skill, target_dir, allow_backup=True)
        self.assertEqual(install_res["status"], "INSTALLED_SUCCESS")
        self.assertIsNotNone(install_res["backup_path"])
        self.assertIn(".bak_", install_res["backup_path"])
        
        # Verify backup contains old file
        backup_p = Path(install_res["backup_path"])
        self.assertTrue(backup_p.exists())
        self.assertIn("0.9", (backup_p / "SKILL.md").read_text())

        # Verify target is updated
        self.assertIn("1.0", (target_dir / "SKILL.md").read_text())
        self.assertEqual(install_res["diff_summary"]["updated_count"], 1)
        self.assertEqual(install_res["diff_summary"]["created_count"], 1)

    def test_02_honest_runtime_capability_declarations(self):
        """Pass path: Declares tool-enabled runtimes and prompt-only fallbacks honestly."""
        claude = get_runtime_capability_declaration("claude_code")
        self.assertTrue(claude["is_supported"])
        self.assertEqual(claude["runtime_type"], "tool_enabled")
        self.assertIn("web_search", claude["features_available"])

        chatgpt = get_runtime_capability_declaration("chatgpt_web")
        self.assertTrue(chatgpt["is_supported"])
        self.assertEqual(chatgpt["runtime_type"], "prompt_only")
        self.assertEqual(chatgpt["fallback_mode"], "static_rag_degraded")

        unknown = get_runtime_capability_declaration("unverified_future_agent")
        self.assertFalse(unknown["is_supported"])
        self.assertEqual(unknown["status"], "UNVERIFIED_RUNTIME")

    def test_03_adversarial_overwrite_without_backup_blocked(self):
        """Adversarial path: Overwriting existing skill directory without backup raises PermissionError."""
        target_dir = self.temp_dir / "target_nobackup"
        target_dir.mkdir()
        (target_dir / "SKILL.md").write_text("# Important User Skill")

        with self.assertRaises(PermissionError):
            install_skill_safely(self.src_skill, target_dir, allow_backup=False)

if __name__ == "__main__":
    unittest.main()
