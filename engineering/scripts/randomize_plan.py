#!/usr/bin/env python3
import argparse, hashlib, json, random
from pathlib import Path

def load_jsonl(path):
    rows=[]
    for i,line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            rows.append(json.loads(line))
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cases', required=True)
    p.add_argument('--conditions', required=True, help='comma-separated')
    p.add_argument('--replicates', type=int, default=3)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--out', required=True)
    a=p.parse_args()
    cases=load_jsonl(a.cases)
    conds=[x.strip() for x in a.conditions.split(',') if x.strip()]
    if len(conds)<2: raise SystemExit('need at least two conditions')
    rng=random.Random(a.seed)
    plan=[]
    for c in cases:
        reps=1 if c['tier']=='D' else a.replicates
        for r in range(1,reps+1):
            order=conds[:]
            rng.shuffle(order)
            for pos,cond in enumerate(order):
                raw=f"{c['case_id']}|{cond}|{r}|{a.seed}"
                run_id=hashlib.sha256(raw.encode()).hexdigest()[:16]
                plan.append({'run_id':run_id,'case_id':c['case_id'],'tier':c['tier'],'condition':cond,'replicate':r,'order_in_block':pos})
    Path(a.out).write_text('\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in plan)+'\n',encoding='utf-8')
    print(json.dumps({'runs':len(plan),'seed':a.seed,'conditions':conds},ensure_ascii=False))
if __name__=='__main__': main()
