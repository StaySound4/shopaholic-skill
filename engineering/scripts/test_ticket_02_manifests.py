#!/usr/bin/env python3
"""Test suite for Ticket 02: Define machine-readable evaluation cases and immutable manifests.
Tests both happy path and adversarial conditions:
1. Validate at least 40 seed cases (current 67 cases) strictly adhering to eval-case schema contract.
2. Verify experiment manifest contains case-set hash, conditions, replicates, seed, and release gates.
3. Verify mutating one prompt byte changes the canonical case-set hash.
4. Adversarial path: Reusing a preregistered manifest with a mutated case set triggers INVALID_PROTOCOL error.
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest_tool import compute_case_set_hash, validate_all_cases, validate_manifest

class TestTicket02Manifests(unittest.TestCase):
    def setUp(self):
        self.root = Path("engineering")
        self.cases_file = self.root / "evals/SEED_CASES.jsonl"
        self.manifest_file = self.root / "evals/EXAMPLE_MANIFEST.json"
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_ticket_02_"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_seed_cases_schema_conformance(self):
        """Pass path: All seed cases in SEED_CASES.jsonl conform strictly to schema."""
        ok, errors, count = validate_all_cases(self.cases_file)
        self.assertTrue(ok, f"Case validation failed: {errors}")
        self.assertGreaterEqual(count, 40, f"Expected >= 40 seed cases, got {count}")
        self.assertEqual(len(errors), 0)

    def test_02_manifest_schema_and_hash_integrity(self):
        """Pass path: EXAMPLE_MANIFEST.json conforms to schema and matches canonical hash."""
        ok, errors, manifest = validate_manifest(self.manifest_file, self.cases_file)
        self.assertTrue(ok, f"Manifest validation failed: {errors}")
        self.assertEqual(len(errors), 0)
        self.assertIn("case_set_hash", manifest)
        self.assertEqual(manifest["case_set_hash"], compute_case_set_hash(self.cases_file))
        self.assertGreaterEqual(len(manifest["conditions"]), 2)
        self.assertGreaterEqual(manifest["replicates"], 1)
        self.assertIn("release_gates", manifest)

    def test_03_mutating_prompt_byte_changes_case_set_hash(self):
        """Pass path: Mutating even a single character in any case changes the case_set_hash."""
        original_hash = compute_case_set_hash(self.cases_file)
        
        # Read cases and mutate the first case prompt
        lines = self.cases_file.read_text(encoding="utf-8").splitlines()
        first_case = json.loads(lines[0])
        first_case["prompt"] += " [mutated]"
        lines[0] = json.dumps(first_case, ensure_ascii=False)
        
        mutated_file = self.temp_dir / "MUTATED_CASES.jsonl"
        mutated_file.write_text("\n".join(lines), encoding="utf-8")
        
        mutated_hash = compute_case_set_hash(mutated_file)
        self.assertNotEqual(original_hash, mutated_hash, "Hash should change when prompt is mutated")

    def test_04_adversarial_reusing_preregistered_manifest_fails_with_invalid_protocol(self):
        """Adversarial path: Using a modified case set with an existing manifest produces INVALID_PROTOCOL."""
        # Create mutated cases
        lines = self.cases_file.read_text(encoding="utf-8").splitlines()
        first_case = json.loads(lines[0])
        first_case["prompt"] += " [adversarial modification]"
        lines[0] = json.dumps(first_case, ensure_ascii=False)
        
        mutated_file = self.temp_dir / "ADVERSARIAL_CASES.jsonl"
        mutated_file.write_text("\n".join(lines), encoding="utf-8")
        
        ok, errors, _ = validate_manifest(self.manifest_file, mutated_file)
        self.assertFalse(ok, "Manifest validation should fail against mutated case set")
        
        mismatch_errors = [e for e in errors if "INVALID_PROTOCOL" in e and "case_set_hash mismatch" in e]
        self.assertEqual(len(mismatch_errors), 1, f"Expected INVALID_PROTOCOL error, got {errors}")

if __name__ == "__main__":
    unittest.main()
