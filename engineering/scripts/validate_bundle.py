#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_baseline import verify_baseline

def fail(msg, errors): errors.append(msg)
def main():
    p=argparse.ArgumentParser(); p.add_argument('root'); a=p.parse_args(); root=Path(a.root); errors=[]
    required=['README.md','SPEC.md','TEST_SEAMS.md','CURRENT_STATE_AUDIT.md','ARCHITECTURE_DECISIONS.md','SOURCE_REGISTRY.md','TICKET_INDEX.md','TRACEABILITY_MATRIX.md','evals/EXPERIMENT_PROTOCOL.md','evals/SCORING_RUBRIC.md','evals/AI_EXECUTION_RUNBOOK.md','evals/SEED_CASES.jsonl']
    for r in required:
        if not (root/r).is_file(): fail(f'missing {r}',errors)
    # verify baseline integrity
    baseline_res = verify_baseline(root)
    if baseline_res.get('status') != 'PASS':
        fail(f"Baseline integrity failure: {baseline_res.get('error', 'Hash mismatch')}", errors)
    case_ids=[]
    if (root/'evals/SEED_CASES.jsonl').is_file():
        for n,line in enumerate((root/'evals/SEED_CASES.jsonl').read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): continue
            try: obj=json.loads(line)
            except Exception as e: fail(f'case line {n} invalid json: {e}',errors); continue
            cid=obj.get('case_id'); case_ids.append(cid)
            if not re.match(r'^[DFL]-\d{3}$',str(cid)): fail(f'bad case id {cid}',errors)
            if not obj.get('assertions'): fail(f'{cid}: no assertions',errors)
        if len(case_ids)!=len(set(case_ids)): fail('duplicate case IDs',errors)
        if len(case_ids)<40: fail('fewer than 40 seed cases',errors)
    # tickets and blockers
    tickets=sorted((root/'tickets').glob('*.md')) if (root/'tickets').exists() else []
    if len(tickets)<30: fail(f'expected >=30 tickets, found {len(tickets)}',errors)
    numbers=set()
    for t in tickets:
        m=re.match(r'(\d+)-',t.name)
        if m: numbers.add(int(m.group(1)))
        txt=t.read_text(encoding='utf-8')
        for field in ['**What to build:**','**Blocked by:**','**Status:** ready-for-agent','## Acceptance criteria','## Verification procedure','## Evidence to attach','## Stop conditions']:
            if field not in txt: fail(f'{t.name}: missing {field}',errors)
    # detect obvious fake preassigned experiment scores
    bad=[]
    for f in list((root/'evals').glob('*'))+list((root/'scripts').glob('*')):
        if not f.is_file(): continue
        text=f.read_text(encoding='utf-8',errors='ignore')
        if f.name != 'validate_bundle.py' and re.search(r'oracle.{0,80}(score|100)',text,re.I|re.S): bad.append(f.name)
    if bad: fail('possible preassigned oracle score artifacts: '+','.join(bad),errors)
    if errors:
        print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
    print(json.dumps({'status':'PASS','seed_cases':len(case_ids),'tickets':len(tickets)},ensure_ascii=False))
if __name__=='__main__': main()
