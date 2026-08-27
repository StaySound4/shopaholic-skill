#!/usr/bin/env python3
"""Reference deterministic solver for a two-criterion, two-candidate linear flip point."""
import argparse, json

def score(v,w): return (1-w)*v[0] + w*v[1]
def solve(a,b):
    # (1-w)a0+w a1 = (1-w)b0+w b1
    num=b[0]-a[0]
    den=(a[1]-a[0])-(b[1]-b[0])
    if abs(den)<1e-12: return None
    w=num/den
    return w if 0<=w<=1 else None

def format_slider(w, label0, label1, cand_a, cand_b):
    if w is None: return "No valid flip point in [0, 1]."
    pct1 = round(w * 100)
    pct0 = 100 - pct1
    return f"When {label0} >= {pct0}%, {cand_a} is preferred; when {label1} >= {pct1}%, recommendation flips to {cand_b}."

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--a', required=True, help='criterion0,criterion1')
    p.add_argument('--b', required=True)
    p.add_argument('--weight', type=float, default=.5)
    p.add_argument('--label0', default='Criterion0')
    p.add_argument('--label1', default='Criterion1')
    p.add_argument('--name_a', default='Candidate A')
    p.add_argument('--name_b', default='Candidate B')
    args = p.parse_args()
    
    A = [float(x) for x in args.a.split(',')]
    B = [float(x) for x in args.b.split(',')]
    if len(A) != 2 or len(B) != 2: raise SystemExit('exactly two criteria required')
    
    w_flip = solve(A, B)
    result = {
        'current_weight_criterion1': args.weight,
        'score_a': score(A, args.weight),
        'score_b': score(B, args.weight),
        'flip_weight_criterion1': w_flip,
        'contextual_slider': format_slider(w_flip, args.label0, args.label1, args.name_a, args.name_b)
    }
    print(json.dumps(result, indent=2))

if __name__ == '__main__': main()
