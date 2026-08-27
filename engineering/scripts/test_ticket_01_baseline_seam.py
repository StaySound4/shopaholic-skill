#!/usr/bin/env python3
"""Test suite for Ticket 01: Freeze uploaded baseline and create the executable evaluation seam.
Tests both happy path and adversarial conditions:
1. Hash-addressed baseline verification (B1_uploaded_current)
2. Adversarial tampering detection
3. Deterministic evaluation seam recording with schema conformance
4. Non-fabrication of scores (no pre-assigned ratings)
"""
import json, os, shutil, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_baseline import verify_baseline
from run_case_seam import create_run_record, validate_against_schema

class TestTicket01BaselineSeam(unittest.TestCase):
    def setUp(self):
        self.root = Path("engineering")
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_ticket_01_"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_baseline_hash_verification_pass(self):
        """Pass path: Real baseline files match SNAPSHOT_MANIFEST.json exactly."""
        res = verify_baseline(self.root)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["condition"], "B1_uploaded_current")
        self.assertGreaterEqual(len(res["files_checked"]), 4)
        for f in res["files_checked"]:
            self.assertEqual(f["status"], "MATCH")

    def test_02_adversarial_tampering_fails(self):
        """Adversarial path: Tampered baseline file is immediately caught by verification."""
        # Create a mock engineering directory
        mock_eng = self.temp_dir / "engineering"
        mock_eng.mkdir()
        shutil.copy(self.root / "SNAPSHOT_MANIFEST.json", mock_eng / "SNAPSHOT_MANIFEST.json")
        
        # Copy snapshot files
        mock_snapshot = mock_eng / "current-skill-snapshot"
        shutil.copytree(self.root / "current-skill-snapshot", mock_snapshot)
        
        # Tamper with SKILL.md
        skill_file = mock_snapshot / "SKILL.md"
        skill_file.write_text(skill_file.read_text(encoding="utf-8") + "\n# Tampered line", encoding="utf-8")
        
        res = verify_baseline(mock_eng)
        self.assertEqual(res["status"], "FAIL")
        tampered_entries = [f for f in res["files_checked"] if f["path"] == "SKILL.md"]
        self.assertEqual(len(tampered_entries), 1)
        self.assertEqual(tampered_entries[0]["status"], "MISMATCH")

    def test_03_run_case_seam_generates_distinct_immutable_runs(self):
        """Pass path: Two runs of the same case produce distinct run IDs, preserve raw output, and have no score fields."""
        raw_output_text = (
            "Recommended candidate: Product X (CNY 1500)\n"
            "Satisfies all physical constraints.\n"
            "<decision_record>\n"
            "{\n"
            '  "case_id": "D-001",\n'
            '  "final_recommendations": [{"name": "Product X", "price": 1500}]\n'
            "}\n"
            "</decision_record>"
        )
        
        run_1 = create_run_record(
            case_id="D-001",
            condition="B1_uploaded_current",
            replicate=1,
            raw_output=raw_output_text,
            output_dir=self.temp_dir,
            status="complete"
        )
        
        run_2 = create_run_record(
            case_id="D-001",
            condition="B1_uploaded_current",
            replicate=2,
            raw_output=raw_output_text,
            output_dir=self.temp_dir,
            status="complete"
        )
        
        # Assertions
        self.assertNotEqual(run_1["run_id"], run_2["run_id"])
        self.assertEqual(run_1["case_id"], "D-001")
        self.assertEqual(run_2["case_id"], "D-001")
        self.assertEqual(run_1["condition"], "B1_uploaded_current")
        self.assertEqual(run_1["status"], "complete")
        
        # Verify raw output file is preserved verbatim
        raw_path_1 = Path(run_1["raw_output_path"])
        self.assertTrue(raw_path_1.is_file())
        self.assertEqual(raw_path_1.read_text(encoding="utf-8"), raw_output_text)
        
        # Verify decision_record.json was extracted from XML block
        dec_path_1 = Path(run_1["decision_record_path"])
        self.assertTrue(dec_path_1.is_file())
        dec_json = json.loads(dec_path_1.read_text(encoding="utf-8"))
        self.assertEqual(dec_json["case_id"], "D-001")
        
        # Ensure no pre-assigned or hardcoded quality score exists in run record
        self.assertNotIn("score", run_1)
        self.assertNotIn("quality_rating", run_1)
        self.assertNotIn("synthetic_rating", run_1)

    def test_04_schema_conformance(self):
        """Verifies that the run record adheres to run-record.schema.json."""
        sample_record = {
            "run_id": "run_D-001_B1_r1_12345678",
            "case_id": "D-001",
            "condition": "B1_uploaded_current",
            "replicate": 1,
            "started_at": "2026-08-28T00:00:00Z",
            "status": "complete",
            "raw_output_path": "/path/to/raw_output.txt"
        }
        schema_path = self.root / "schemas/run-record.schema.json"
        errors = validate_against_schema(sample_record, schema_path)
        self.assertEqual(errors, [])

if __name__ == "__main__":
    unittest.main()
