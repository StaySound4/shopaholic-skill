#!/usr/bin/env python3
"""Baseline hash verification and integrity check.
Ensures that the frozen uploaded baseline (B1_uploaded_current) has not been tampered with.
"""
import argparse, hashlib, json, sys
from pathlib import Path

def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_baseline(root: Path) -> dict:
    manifest_path = root / 'SNAPSHOT_MANIFEST.json'
    if not manifest_path.is_file():
        return {'status': 'FAIL', 'error': 'SNAPSHOT_MANIFEST.json not found'}
    
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except Exception as e:
        return {'status': 'FAIL', 'error': f'Failed to parse SNAPSHOT_MANIFEST.json: {e}'}
    
    snapshot_dir = root / 'current-skill-snapshot'
    if not snapshot_dir.is_dir():
        return {'status': 'FAIL', 'error': 'current-skill-snapshot directory not found'}
    
    files_checked = []
    overall_pass = True
    
    for item in manifest.get('files', []):
        rel_path = item.get('path')
        expected_hash = item.get('sha256')
        expected_bytes = item.get('bytes')
        target_file = snapshot_dir / rel_path
        
        if not target_file.is_file():
            files_checked.append({
                'path': rel_path,
                'status': 'MISSING',
                'expected_hash': expected_hash,
                'actual_hash': None
            })
            overall_pass = False
            continue
            
        actual_hash = compute_sha256(target_file)
        actual_bytes = target_file.stat().st_size
        
        if actual_hash != expected_hash or actual_bytes != expected_bytes:
            files_checked.append({
                'path': rel_path,
                'status': 'MISMATCH',
                'expected_hash': expected_hash,
                'actual_hash': actual_hash,
                'expected_bytes': expected_bytes,
                'actual_bytes': actual_bytes
            })
            overall_pass = False
        else:
            files_checked.append({
                'path': rel_path,
                'status': 'MATCH',
                'hash': actual_hash,
                'bytes': actual_bytes
            })
            
    return {
        'status': 'PASS' if overall_pass else 'FAIL',
        'condition': 'B1_uploaded_current',
        'files_checked': files_checked
    }

def main():
    p = argparse.ArgumentParser(description='Verify baseline snapshot hashes')
    p.add_argument('--root', default='engineering', help='Root directory containing SNAPSHOT_MANIFEST.json')
    p.add_argument('--json', action='store_true', help='Output in JSON format')
    args = p.parse_args()
    
    res = verify_baseline(Path(args.root))
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        if res['status'] == 'PASS':
            print(f"PASS: Baseline B1_uploaded_current verified ({len(res['files_checked'])} files matched).")
        else:
            print(f"FAIL: Baseline integrity check failed: {res.get('error', 'Hash mismatch detected')}")
            for f in res.get('files_checked', []):
                if f['status'] != 'MATCH':
                    print(f"  - {f['path']}: {f['status']} (expected {f.get('expected_hash')}, got {f.get('actual_hash')})")
    
    if res['status'] != 'PASS':
        sys.exit(1)

if __name__ == '__main__':
    main()
