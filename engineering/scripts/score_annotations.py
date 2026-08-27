#!/usr/bin/env python3
"""Aggregate REAL per-run metric rows. This script contains no condition scores.
Input JSONL row example:
{"case_id":"D-001","condition":"B1_uploaded_current","replicate":1,"metrics":{"hard_constraint":1,"usefulness":2}}
"""
import argparse, json, math, random
from collections import defaultdict
from pathlib import Path

def load(path):
    out=[]
    for n,line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        if not {'case_id','condition','replicate','metrics'} <= row.keys():
            raise ValueError(f'line {n}: missing required keys')
        out.append(row)
    return out

def quantile(xs,q):
    xs=sorted(xs)
    if not xs: return None
    pos=(len(xs)-1)*q; lo=int(pos); hi=min(lo+1,len(xs)-1); frac=pos-lo
    return xs[lo]*(1-frac)+xs[hi]*frac

def bootstrap_diff(pairs, seed=20260827, nboot=10000):
    if not pairs: return (None,None)
    rng=random.Random(seed); n=len(pairs); ds=[]
    diffs=[t-b for b,t in pairs]
    for _ in range(nboot):
        ds.append(sum(diffs[rng.randrange(n)] for _ in range(n))/n)
    return quantile(ds,.025),quantile(ds,.975)

def two_sided_sign_p(pairs):
    pos=sum(t>b for b,t in pairs); neg=sum(t<b for b,t in pairs); n=pos+neg
    if n==0: return 1.0
    k=min(pos,neg)
    tail=sum(math.comb(n,i) for i in range(k+1))/(2**n)
    return min(1.0,2*tail)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--baseline',required=True); ap.add_argument('--target',required=True); ap.add_argument('--out',required=True); ap.add_argument('--seed',type=int,default=20260827)
    a=ap.parse_args(); rows=load(a.input)
    # average replicates by case/condition/metric
    acc=defaultdict(list)
    for r in rows:
        for m,v in r['metrics'].items():
            if isinstance(v,(int,float)) and not isinstance(v,bool): acc[(r['case_id'],r['condition'],m)].append(float(v))
    means={k:sum(v)/len(v) for k,v in acc.items()}
    metrics=sorted({k[2] for k in means})
    results=[]
    for m in metrics:
        cases=sorted({k[0] for k in means if k[2]==m})
        pairs=[]
        for c in cases:
            kb=(c,a.baseline,m); kt=(c,a.target,m)
            if kb in means and kt in means: pairs.append((means[kb],means[kt]))
        if not pairs: continue
        bm=sum(x for x,_ in pairs)/len(pairs); tm=sum(y for _,y in pairs)/len(pairs); diff=tm-bm
        lo,hi=bootstrap_diff(pairs,a.seed); p=two_sided_sign_p(pairs)
        results.append({'metric':m,'n_paired_cases':len(pairs),'baseline_mean':bm,'target_mean':tm,'paired_difference':diff,'bootstrap_95_ci':[lo,hi],'two_sided_sign_test_p':p})
    obj={'baseline':a.baseline,'target':a.target,'results':results,'note':'Scores are computed from supplied per-run artifacts; this script contains no preassigned condition outcomes.'}
    Path(a.out).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(obj,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
