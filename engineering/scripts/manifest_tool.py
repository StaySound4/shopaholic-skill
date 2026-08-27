#!/usr/bin/env python3
"""Evaluation case validation and immutable manifest management.
Computes canonical case-set hashes and verifies experiment manifest contracts.
"""
import argparse, datetime, hashlib, json, re, sys
from pathlib import Path

def compute_case_set_hash(cases_path: Path) -> str:
    """Computes a deterministic canonical SHA-256 hash across all cases in a JSONL file."""
    if not cases_path.is_file():
        raise FileNotFoundError(f"Cases file not found: {cases_path}")
    
    canonical_entries = []
    for line in cases_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        # Sort keys to ensure deterministic serialization
        canonical_str = json.dumps(obj, sort_keys=True, ensure_ascii=False)
        canonical_entries.append(canonical_str)
    
    # Sort all canonical entries by case_id for stable ordering
    canonical_entries.sort()
    full_payload = "\n".join(canonical_entries).encode("utf-8")
    return hashlib.sha256(full_payload).hexdigest()

def validate_case_object(case_obj: dict) -> list[str]:
    """Validates a single evaluation case against eval-case schema contract."""
    errors = []
    cid = case_obj.get("case_id")
    if not cid or not isinstance(cid, str) or not re.match(r'^[DFL]-[0-9]{3}$', cid):
        errors.append(f"Invalid or missing case_id: {cid}")
        
    version = case_obj.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append(f"{cid}: version must be an integer >= 1")
        
    tier = case_obj.get("tier")
    if tier not in ["D", "F", "L"]:
        errors.append(f"{cid}: tier must be one of ['D', 'F', 'L'], got '{tier}'")
        
    category = case_obj.get("category")
    if not category or not isinstance(category, str):
        errors.append(f"{cid}: category must be a non-empty string")
        
    prompt = case_obj.get("prompt")
    if not prompt or not isinstance(prompt, str):
        errors.append(f"{cid}: prompt must be a non-empty string")
        
    assertions = case_obj.get("assertions")
    if not isinstance(assertions, list) or len(assertions) < 1:
        errors.append(f"{cid}: assertions must be a non-empty array")
    else:
        for idx, ass in enumerate(assertions):
            if not isinstance(ass, dict):
                errors.append(f"{cid}: assertion #{idx} must be an object")
                continue
            if "assertion_id" not in ass:
                errors.append(f"{cid}: assertion #{idx} missing assertion_id")
            if "kind" not in ass:
                errors.append(f"{cid}: assertion #{idx} missing kind")
            if "expected" not in ass:
                errors.append(f"{cid}: assertion #{idx} missing expected")
                
    return errors

def validate_all_cases(cases_path: Path) -> tuple[bool, list[str], int]:
    """Validates all cases in a JSONL file."""
    if not cases_path.is_file():
        return False, [f"Cases file not found: {cases_path}"], 0
        
    all_errors = []
    seen_ids = set()
    count = 0
    
    for line_num, line in enumerate(cases_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        count += 1
        try:
            obj = json.loads(line)
        except Exception as e:
            all_errors.append(f"Line {line_num}: JSON decode error: {e}")
            continue
            
        cid = obj.get("case_id")
        if cid in seen_ids:
            all_errors.append(f"Line {line_num}: Duplicate case_id '{cid}'")
        seen_ids.add(cid)
        
        errs = validate_case_object(obj)
        all_errors.extend(errs)
        
    return (len(all_errors) == 0, all_errors, count)

def validate_manifest(manifest_path: Path, cases_path: Path | None = None) -> tuple[bool, list[str], dict]:
    """Validates experiment manifest schema and verifies case_set_hash integrity."""
    if not manifest_path.is_file():
        return False, [f"Manifest not found: {manifest_path}"], {}
        
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, [f"Manifest JSON decode error: {e}"], {}
        
    errors = []
    required = ["experiment_id", "protocol_version", "created_at", "case_set_hash", "conditions", "replicates", "random_seed", "release_gates"]
    for req in required:
        if req not in manifest or manifest[req] is None:
            errors.append(f"Missing required manifest property: {req}")
            
    conditions = manifest.get("conditions", [])
    if not isinstance(conditions, list) or len(conditions) < 2:
        errors.append("Field 'conditions' must contain at least 2 distinct conditions")
    elif len(conditions) != len(set(conditions)):
        errors.append("Field 'conditions' must not contain duplicates")
        
    reps = manifest.get("replicates")
    if not isinstance(reps, int) or reps < 1:
        errors.append("Field 'replicates' must be an integer >= 1")
        
    gates = manifest.get("release_gates")
    if not isinstance(gates, dict) or len(gates) < 1:
        errors.append("Field 'release_gates' must be a non-empty object")
        
    if cases_path is not None and cases_path.is_file():
        actual_hash = compute_case_set_hash(cases_path)
        expected_hash = manifest.get("case_set_hash")
        if actual_hash != expected_hash:
            errors.append(
                f"INVALID_PROTOCOL: case_set_hash mismatch. Manifest specifies '{expected_hash}', but current cases hash is '{actual_hash}'"
            )
            
    return (len(errors) == 0, errors, manifest)

def main():
    p = argparse.ArgumentParser(description="Evaluation case validation and manifest tooling")
    p.add_argument("--cases", help="Path to SEED_CASES.jsonl")
    p.add_argument("--manifest", help="Path to experiment manifest JSON")
    p.add_argument("--compute-hash", action="store_true", help="Print canonical case-set hash")
    p.add_argument("--verify-cases", action="store_true", help="Validate all cases in the file")
    p.add_argument("--verify-manifest", action="store_true", help="Validate manifest against schema and cases")
    args = p.parse_args()
    
    if args.compute_hash and args.cases:
        print(compute_case_set_hash(Path(args.cases)))
        return
        
    if args.verify_cases and args.cases:
        ok, errs, count = validate_all_cases(Path(args.cases))
        if ok:
            print(f"PASS: {count} evaluation cases verified successfully.")
        else:
            print(f"FAIL: {len(errs)} case validation errors detected:")
            for e in errs:
                print(f"  - {e}")
            sys.exit(1)
            
    if args.verify_manifest and args.manifest:
        cases_p = Path(args.cases) if args.cases else None
        ok, errs, _ = validate_manifest(Path(args.manifest), cases_p)
        if ok:
            print(f"PASS: Manifest {args.manifest} verified successfully.")
        else:
            print(f"FAIL: Manifest verification failed:")
            for e in errs:
                print(f"  - {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
