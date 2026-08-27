#!/usr/bin/env python3
"""Evaluate preregistered gates against a computed metric summary.
Summary JSON format: {"metrics": {"fabricated_source_rate": 0.0, ...}}
Gate manifest contains release_gates with *_min or *_max keys.
"""
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--summary',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    man=json.loads(Path(a.manifest).read_text(encoding='utf-8')); summ=json.loads(Path(a.summary).read_text(encoding='utf-8'))
    if not man.get('preregistered'): raise SystemExit('manifest is not preregistered; refusing confirmatory gate evaluation')
    metrics=summ.get('metrics',{}); rows=[]; overall=True
    for key,threshold in man['release_gates'].items():
        if key.endswith('_min'): metric=key[:-4]; op='>='; value=metrics.get(metric); passed=value is not None and value>=threshold
        elif key.endswith('_max'): metric=key[:-4]; op='<='; value=metrics.get(metric); passed=value is not None and value<=threshold
        else: metric=key; op='=='; value=metrics.get(metric); passed=value==threshold
        if not passed: overall=False
        rows.append({'gate':key,'metric':metric,'value':value,'operator':op,'threshold':threshold,'pass':passed})
    obj={'experiment_id':man['experiment_id'],'overall':'PASS' if overall else 'FAIL','gates':rows}
    Path(a.out).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(obj,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
