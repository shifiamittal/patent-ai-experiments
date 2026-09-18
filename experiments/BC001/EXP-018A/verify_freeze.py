"""Verify ranking, attribution endpoints and unchanged policy without labels."""
import ast
import csv
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return {r['Record ID']:r for r in csv.DictReader(p.open(encoding='utf-8',newline=''))}
m = json.loads((EXP/'manifest.json').read_text())
for name, digest in m['output_sha256'].items(): assert sha(EXP/'outputs'/name) == digest, name
assert sha(ROOT/m['input']) == m['input_sha256']
old = ROOT/'components/relevance-scorer/rs_v0.3_feature_aware_ta'
new = ROOT/'components/relevance-scorer/rs_v0.4_extraction_gate_repair_ta'
v = json.loads((EXP/'outputs/validation.json').read_text())
for name in ('scorer.py','engine.py','bc001_config.py','scoring-spec.yaml','extraction-schema.json','run_blind.py'):
    assert sha(new/name) == v['allowlisted_input_hashes'][name], name
for name in ('scoring-spec.yaml','extraction-schema.json'): assert sha(old/name) == sha(new/name)
def policy(path):
    tree = ast.parse(path.read_text())
    return {n.targets[0].id:ast.dump(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in {'FEATURES','RELATIONS','WEIGHTS','FM','RM','DOMAIN','CAPS','PENALTIES'}}
assert policy(old/'scorer.py') == policy(new/'scorer.py')
variants = json.loads((EXP/'outputs/correction-variants.json').read_text())
for name, path in [('baseline',ROOT/'experiments/BC001/EXP-016A/outputs/full-ranking.csv'),('storage',EXP/'outputs/full-ranking.csv')]:
    actual = rows(path)
    assert set(actual) == set(variants[name]) and len(actual) == 3238
    for rid, r in actual.items():
        a = variants[name][rid]
        assert a['rank'] == int(r['rank']) and a['score'] == float(r['final_score']), (name,rid)
        assert a['flags'] == json.loads(r['noise_flags']) and a['domain'] == r['domain_category']
        assert all(r[k+'_status'] == status for k,status in {**a['features'],**a['relationships']}.items())
print('PASS: all hashes, policy constants, staged code, exact baseline and final attribution endpoints')
