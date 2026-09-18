"""Stage exact allowlisted input, test and freeze without evaluator reads."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parent
COMP = ROOT/'components/relevance-scorer/rs_v0.4_extraction_gate_repair_ta'
INPUT = ROOT/'experiments/BC001/EXP-013/working-artifacts/input.json'
EXPECTED = '3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, v): p.write_text(json.dumps(v, indent=2)+'\n')

assert sha(INPUT) == EXPECTED
sys.path.insert(0, str(COMP))
import scorer
records = json.loads(INPUT.read_text())[1:]
# Only the three user-disclosed boundary IDs are selected before freeze.
for rid, title, abstract in records:
    if rid in {'BC001-5946DA63E67B','BC001-A01F02870DCB','BC001-3F53B09CDA35'}:
        row = scorer.score(scorer.extract(title, abstract), title, abstract)
        print(rid, row['features']['F3']['status'], row['relationships']['F2_to_F3']['status'], row['noise_flags'])
        assert row['features']['F3']['status'] == ('E' if rid == 'BC001-5946DA63E67B' else 'A')
        if rid == 'BC001-5946DA63E67B': assert row['relationships']['F2_to_F3']['status'] == 'E'
        if rid == 'BC001-3F53B09CDA35': assert 'holster_only' in row['noise_flags']
        if rid == 'BC001-A01F02870DCB': assert 'storage_only' in row['noise_flags']

tests = []
for cwd, args in [(COMP, ['-m','unittest','discover','-s','tests','-v']), (COMP.parent/'rs_v0.3_feature_aware_ta', ['-m','unittest','discover','-s','tests','-v']), (ROOT, ['-m','unittest','discover','-s','experiments/BC001/EXP-016A/evaluation','-p','test_evaluation.py','-v'])]:
    p = subprocess.run([sys.executable,'-B',*args], cwd=cwd, capture_output=True, text=True)
    tests.append({'cwd':str(cwd.relative_to(ROOT)), 'command':args, 'exit_code':p.returncode, 'output':p.stdout+p.stderr})
    assert p.returncode == 0, p.stdout+p.stderr
write(EXP/'tests.json', tests)
p = subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(EXP/'tests'),'-v'],cwd=ROOT,capture_output=True,text=True)
assert p.returncode == 0, p.stdout+p.stderr
tests.append({'suite':'EXP-018A decision rules','exit_code':p.returncode,'output':p.stdout+p.stderr})
write(EXP/'tests.json', tests)
stage = Path(tempfile.mkdtemp(prefix='exp018a-blind-'))
shutil.copyfile(INPUT, stage/'input.json')
for name in ('scorer.py','engine.py','bc001_config.py','run_blind.py','scoring-spec.yaml','extraction-schema.json'):
    shutil.copyfile(COMP/name,stage/name)
shutil.copyfile(ROOT/'experiments/BC001/EXP-016A/frozen-disclosure.md',stage/'frozen-disclosure.md')
p = subprocess.run([sys.executable,'-B',str(stage/'run_blind.py')], capture_output=True, text=True)
assert p.returncode == 0, p.stdout+p.stderr
print(p.stdout)
shutil.copytree(stage/'outputs', EXP/'outputs', dirs_exist_ok=True)
# Freeze sequential attribution variants before any mapping access.
variants = {}
active = set()
for name in ['baseline','outcomes','relationships','mechanism','storage']:
    if name != 'baseline': active.add(name)
    scorer.CORRECTIONS = active.copy()
    rows = scorer.rank_records(records)
    variants[name] = {r['record_id']:{'rank':r['rank'],'score':r['final_score'],'features':{k:v['status'] for k,v in r['features'].items()},'relationships':{k:v['status'] for k,v in r['relationships'].items()},'flags':r['noise_flags'],'domain':r['domain_category']} for r in rows}
write(EXP/'outputs/correction-variants.json',variants)
write(EXP/'manifest.json', {'experiment':'EXP-018A','baseline':'EXP-013','comparator':'EXP-016A','source_diagnosis':'EXP-016A-D1 and user request','component':COMP.name,'record_count':3238,'input':str(INPUT.relative_to(ROOT)),'input_sha256':EXPECTED,'output_sha256':{p.name:sha(p) for p in (EXP/'outputs').iterdir()},'generalization':'Mechanism-general; validated on BC001 only.','scoring_policy':'unchanged; specification copied byte-for-byte from rs_v0.3','private_mapping_access':'not accessed before ranking freeze commit','prior_exposure':'D1 public diagnostic publication identities and user-disclosed boundary IDs; no private mapping read','attribution':'sequential marginal extraction/status, score and rank effects; variants frozen before evaluation','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
