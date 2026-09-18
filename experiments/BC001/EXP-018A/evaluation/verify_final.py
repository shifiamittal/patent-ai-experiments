"""Independent reconciliation of evaluation outputs and authorized repository scope."""
import csv
import hashlib
import json
import statistics
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
E=EXP/'evaluation'
FREEZE='0303428d542c279410b9166bf02822cf5f084f22'
SOURCE='48ea254ec5f6200f8bbe5c73e9e9cab2152b8bef'
def read(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
subprocess.run([__import__('sys').executable,'-B',str(EXP/'verify_freeze.py')],cwd=ROOT,check=True)
assert not git('diff',FREEZE,'--','components/relevance-scorer/rs_v0.4_extraction_gate_repair_ta','experiments/BC001/EXP-018A/outputs')
assert not git('diff',SOURCE,'--','components/relevance-scorer/rs_v0.3_feature_aware_ta','benchmarks','experiments/BC001/EXP-016A','experiments/BC001/EXP-013')
m=json.loads((E/'metrics.json').read_text()); mov=read(E/'gold-rank-movements.csv')
for v in ('exp013','exp016a','exp018a'):
    ranks=[int(r[v+'_rank']) for r in mov]
    assert statistics.median(ranks)==m['metrics'][v]['median']
    for k in (20,50,100,200): assert sum(r<=k for r in ranks)==m['metrics'][v]['r'+str(k)]
assert all(m['preservation_checks'].values()) and m['decision']=='PROMOTE'
old={r['Record ID']:r for r in read(ROOT/'experiments/BC001/EXP-016A/outputs/full-ranking.csv')}
new={r['Record ID']:r for r in read(EXP/'outputs/full-ranking.csv')}
decomp=read(E/'gold-score-decomposition.csv'); deteriorated=read(E/'three-deteriorated-before-after.csv')
assert len(decomp)==12 and len(deteriorated)==6
for r in decomp:
    source=(old if r['experiment']=='EXP-016A' else new)[r['Record ID']]
    assert all(r[k]==v for k,v in source.items())
registry=read(ROOT/'experiment_registry.csv'); entry=[r for r in registry if r['Experiment ID']=='EXP-018A']
assert len(entry)==1 and entry[0]['Decision']=='PROMOTE' and float(entry[0]['Median Rank of Retrieved GOLD'])==55
assert entry[0]['Precision@20']=='N/A'
impact=read(E/'correction-impact.csv'); details=read(E/'affected-records.csv')
for r in impact:
    rs=[d for d in details if d['correction']==r['correction']]
    assert len(rs)==int(r['interpretation_state_changed'])
    assert sum(d['before_score']!=d['after_score'] for d in rs)==int(r['score_changed'])
    assert sum(d['known_gold']=='False' for d in rs)==int(r['affected_non_gold'])
tests=json.loads((EXP/'tests.json').read_text())
assert all(t['exit_code']==0 for t in tests)
import re
assert sum(int(re.search(r'Ran (\d+) tests',t['output']).group(1)) for t in tests)==66
baseline_paths=set(git('ls-tree','-r','--name-only',SOURCE).splitlines())
allowed={'.gitattributes','CURRENT_SYSTEM.yaml','README.md','Patent_AI_Experiment_Dashboard_Canonical.xlsx','components/component_registry.csv','experiment_registry.csv'}
changed=set(git('diff','--name-only',SOURCE).splitlines())
assert (changed & baseline_paths) <= allowed, changed & baseline_paths - allowed
result={'status':'PASS','tests_passed':66,'full_ranking_rows':len(new),'ranking_sha256':sha(EXP/'outputs/full-ranking.csv'),'input_sha256':json.loads((EXP/'manifest.json').read_text())['input_sha256'],'all_eight_preservation_checks':True,'all_twelve_gold_decompositions_exact':True,'three_deteriorated_before_after_rows':6,'metrics_independently_reconciled':True,'frozen_code_and_ranking_unchanged_since_first_commit':True,'old_scorer_benchmark_and_experiments_unchanged':True,'only_authorized_preexisting_files_changed':sorted(changed&baseline_paths),'dashboard_validation':json.loads((E/'dashboard-validation.json').read_text()),'evaluation_file_hashes':{p.name:sha(p) for p in E.iterdir() if p.suffix in ('.csv','.md','.json') and p.name!='final-validation.json'}}
(E/'final-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('evaluation_file_hashes','dashboard_validation')},indent=2))
