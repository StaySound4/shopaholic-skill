#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(cmd, ok=True):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if ok and p.returncode!=0: raise AssertionError(f'command failed: {cmd}\n{p.stdout}\n{p.stderr}')
    if not ok and p.returncode==0: raise AssertionError(f'command should fail: {cmd}')
    return p

def main():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # 1 bundle validation
        run([sys.executable,str(ROOT/'scripts/validate_bundle.py'),str(ROOT)])
        # 1b ticket 01 baseline seam test
        run([sys.executable,str(ROOT/'scripts/test_ticket_01_baseline_seam.py')])
        # 1c ticket 02 manifest and cases test
        run([sys.executable,str(ROOT/'scripts/test_ticket_02_manifests.py')])
        # 1d ticket 03 positive and sham controls test
        run([sys.executable,str(ROOT/'scripts/test_ticket_03_controls.py')])
        # 1e ticket 04 three-class constraints test
        run([sys.executable,str(ROOT/'scripts/test_ticket_04_constraints.py')])
        # 1f ticket 05 claim and evidence ledger test
        run([sys.executable,str(ROOT/'scripts/test_ticket_05_claim_ledger.py')])
        # 1g ticket 06 claim-specific evidence roles test
        run([sys.executable,str(ROOT/'scripts/test_ticket_06_evidence_roles.py')])
        # 1h ticket 07 evidence confidence and maturity pools test
        run([sys.executable,str(ROOT/'scripts/test_ticket_07_confidence_maturity.py')])
        # 1i ticket 08 product entity hierarchy and scope isolation test
        run([sys.executable,str(ROOT/'scripts/test_ticket_08_product_entity.py')])
        # 1j ticket 09 provenance and corporate role graph test
        run([sys.executable,str(ROOT/'scripts/test_ticket_09_provenance.py')])
        # 1k ticket 10 origin and temporal semantics test
        run([sys.executable,str(ROOT/'scripts/test_ticket_10_origin_temporal.py')])
        # 1l ticket 11 research budget selection test
        run([sys.executable,str(ROOT/'scripts/test_ticket_11_budget.py')])
        # 1m ticket 12 marginal information stop rule and dynamic candidate test
        run([sys.executable,str(ROOT/'scripts/test_ticket_12_stop_rule.py')])
        # 1n ticket 13 scoped safety signal adjudication test
        run([sys.executable,str(ROOT/'scripts/test_ticket_13_safety.py')])
        # 1o ticket 14 scope separation and global evidence test
        run([sys.executable,str(ROOT/'scripts/test_ticket_14_scope.py')])
        # 1p ticket 15 adaptive round 1 intake and conversation cap test
        run([sys.executable,str(ROOT/'scripts/test_ticket_15_round1.py')])
        # 1q ticket 16 adaptive search-informed round 2 test
        run([sys.executable,str(ROOT/'scripts/test_ticket_16_round2.py')])
        # 1r ticket 17 category-aware used goods and EOL checklist test
        run([sys.executable,str(ROOT/'scripts/test_ticket_17_used_goods.py')])
        # 1s ticket 18 strict price semantics test
        run([sys.executable,str(ROOT/'scripts/test_ticket_18_price_semantics.py')])
        # 1t ticket 19 cross-border landed cost and compatibility test
        run([sys.executable,str(ROOT/'scripts/test_ticket_19_landed_cost.py')])
        # 1u ticket 22 official source routing playbooks test
        run([sys.executable,str(ROOT/'scripts/test_ticket_22_source_routing.py')])
        # 1v ticket 23 commercial relationships and sample provenance test
        run([sys.executable,str(ROOT/'scripts/test_ticket_23_commercial_provenance.py')])
        # 1w ticket 24 pareto first ranking and explicit preference weights test
        run([sys.executable,str(ROOT/'scripts/test_ticket_24_pareto.py')])
        # 1x ticket 25 deterministic sensitivity flip point analysis test
        run([sys.executable,str(ROOT/'scripts/test_ticket_25_sensitivity.py')])
        # 1y ticket 26 conditional cost of pivot analysis test
        run([sys.executable,str(ROOT/'scripts/test_ticket_26_pivot_cost.py')])
        # 1z ticket 20 concise decision first renderer test
        run([sys.executable,str(ROOT/'scripts/test_ticket_20_decision_first.py')])
        # 1aa ticket 21 legacy taxonomy contraction test
        run([sys.executable,str(ROOT/'scripts/test_ticket_21_legacy_contract.py')])
        # 1ab ticket 27 modular category knowledge playbooks test
        run([sys.executable,str(ROOT/'scripts/test_ticket_27_playbooks.py')])
        # 1ac ticket 28 truth-first correction protocol test
        run([sys.executable,str(ROOT/'scripts/test_ticket_28_truth_correction.py')])
        # 1ad ticket 29 untrusted evidence data and prompt injection boundary test
        run([sys.executable,str(ROOT/'scripts/test_ticket_29_evidence_guard.py')])
        # 2 sensitivity reference
        p=run([sys.executable,str(ROOT/'scripts/sensitivity_reference.py'),'--a','90,60','--b','70,90','--weight','0.3'])
        assert abs(json.loads(p.stdout)['flip_weight_criterion1']-0.4)<1e-12
        common=[sys.executable,str(ROOT/'scripts/randomize_plan.py'),'--cases',str(ROOT/'evals/SEED_CASES.jsonl'),'--conditions','B1_uploaded_current,T_full','--replicates','2','--seed','123']
        p1=td/'p1.jsonl';p2=td/'p2.jsonl'
        run(common+['--out',str(p1)]);run(common+['--out',str(p2)])
        assert p1.read_bytes()==p2.read_bytes()
        # 4 aggregation must derive target-baseline difference from rows
        inp=td/'m.jsonl';out=td/'s.json'
        inp.write_text('\n'.join([
          json.dumps({'case_id':'D-001','condition':'B1','replicate':1,'metrics':{'m':0}}),
          json.dumps({'case_id':'D-001','condition':'T','replicate':1,'metrics':{'m':1}}),
          json.dumps({'case_id':'D-002','condition':'B1','replicate':1,'metrics':{'m':1}}),
          json.dumps({'case_id':'D-002','condition':'T','replicate':1,'metrics':{'m':1}}),
        ])+'\n')
        run([sys.executable,str(ROOT/'scripts/score_annotations.py'),'--input',str(inp),'--baseline','B1','--target','T','--out',str(out),'--seed','7'])
        res=json.loads(out.read_text())['results'][0]
        assert abs(res['paired_difference']-0.5)<1e-12
        # 5 gate evaluator must refuse non-preregistered manifest
        summary=td/'summary.json';summary.write_text(json.dumps({'metrics':{}}))
        run([sys.executable,str(ROOT/'scripts/evaluate_gates.py'),'--manifest',str(ROOT/'evals/EXAMPLE_MANIFEST.json'),'--summary',str(summary),'--out',str(td/'g.json')],ok=False)
        # 6 pass/fail gates when preregistered
        man=json.loads((ROOT/'evals/EXAMPLE_MANIFEST.json').read_text());man['preregistered']=True
        mp=td/'manifest.json';mp.write_text(json.dumps(man))
        metrics={
          'fabricated_source_rate':0.0,
          'safety_hard_constraint_violation':0.0,
          'user_hard_constraint_compliance':1.0,
          'identity_accuracy':1.0,
          'high_impact_source_role_appropriateness':1.0,
          'insufficiency_handling':1.0,
          'deterministic_math':1.0,
          'research_budget_compliance':1.0,
          'blind_usefulness_non_tie_win_rate_target':0.7
        }
        summary.write_text(json.dumps({'metrics':metrics}));g=td/'gatepass.json'
        run([sys.executable,str(ROOT/'scripts/evaluate_gates.py'),'--manifest',str(mp),'--summary',str(summary),'--out',str(g)])
        assert json.loads(g.read_text())['overall']=='PASS'
        metrics['fabricated_source_rate']=0.01;summary.write_text(json.dumps({'metrics':metrics}));g2=td/'gatefail.json'
        run([sys.executable,str(ROOT/'scripts/evaluate_gates.py'),'--manifest',str(mp),'--summary',str(summary),'--out',str(g2)])
        assert json.loads(g2.read_text())['overall']=='FAIL'
    print('SELFTEST PASS: validator, sensitivity, randomization, derived scoring, preregistration guard, and release-gate mutation all behave as expected.')
if __name__=='__main__': main()
