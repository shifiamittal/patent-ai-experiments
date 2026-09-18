"""Evaluate only the committed ranking; never imports or modifies the scorer."""
import csv
import hashlib
import io
import json
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from decision_rule import decide

EXP = Path(__file__).resolve().parent
ROOT = EXP.parents[2]
FREEZE = '0303428d542c279410b9166bf02822cf5f084f22'
OUT = EXP/'evaluation'
OUT.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def dump(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def csvout(p,rs):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
def blob(p): return subprocess.check_output(['git','show',FREEZE+':'+p.relative_to(ROOT).as_posix()],cwd=ROOT)

subprocess.run(['git','merge-base','--is-ancestor',FREEZE,'HEAD'],cwd=ROOT,check=True)
manifest=json.loads((EXP/'manifest.json').read_text())
validation=json.loads((EXP/'outputs/validation.json').read_text())
assert all(validation['checks'].values())
assert sha(ROOT/manifest['input']) == manifest['input_sha256']
commit_hashes={}
for name,digest in manifest['output_sha256'].items():
    p=EXP/'outputs'/name
    assert sha(p)==digest
    content=blob(p)
    assert content.replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n')
    commit_hashes[name]=hashlib.sha256(content).hexdigest()
assert commit_hashes['full-ranking.csv']==validation['ranking_sha256']
mapping_path=ROOT/'benchmarks/BC001-smartgun/restricted-evaluation/EXP-013/reconstructed-evaluation-mapping.csv'
gold_path=ROOT/'benchmarks/BC001-smartgun/ground-truth/gold10.csv'
first_mapping_read=datetime.now(timezone.utc).isoformat()
mapping=read(mapping_path)
gold={r['publication'] for r in read(gold_path)}
new={r['Record ID']:r for r in read(EXP/'outputs/full-ranking.csv')}
old={r['Record ID']:r for r in read(ROOT/'experiments/BC001/EXP-016A/outputs/full-ranking.csv')}
assert len(new)==len(old)==len(mapping)==3238
assert set(new)==set(old)=={r['record_id'] for r in mapping}
movements=[]
for r in mapping:
    cs=json.loads(r['source_candidates_json'])
    hits=[(c,set(c['family_publications'])&gold) for c in cs if set(c['family_publications'])&gold]
    if not hits: continue
    assert r['mapping_status']=='exact' and len(cs)==len(hits)==1
    c,g=hits[0]
    assert len(g)==1 and g==set(c['existing_gold_publications'])
    rid=r['record_id']; n=new[rid]; o=old[rid]
    movements.append(dict(publication=next(iter(g)),record_id=rid,family_id=c['questel_family_id_fan'],exp013_rank=int(r['v1_rank']),exp016a_rank=int(o['rank']),exp018a_rank=int(n['rank']),exp013_improvement=int(r['v1_rank'])-int(n['rank']),exp016a_improvement=int(o['rank'])-int(n['rank']),exp016a_score=float(o['final_score']),exp018a_score=float(n['final_score'])))
movements.sort(key=lambda r:r['exp013_rank'])
assert len(movements)==len({r['family_id'] for r in movements})==6 and len(gold)==10
metrics={}
for version in ('exp013','exp016a','exp018a'):
    ranks=[r[version+'_rank'] for r in movements]
    metrics[version]={**{'r'+str(k):sum(r<=k for r in ranks) for k in (20,50,100,200)},'median':statistics.median(ranks)}
assert metrics['exp013']==dict(r20=2,r50=2,r100=4,r200=5,median=90.5)
assert metrics['exp016a']==dict(r20=1,r50=2,r100=3,r200=3,median=142.5)
pub={r['publication']:new[r['record_id']] for r in movements}
preservation={
 'invalid_fingerprint_explicit':all(pub['US10591237B1'][k+'_status']=='E' for k in ('F2','F3','F2_to_F3')),
 'architecture_mechanism_repaired':'generic_without_mechanism' not in json.loads(pub['US11792283B2']['noise_flags']),
 'architecture_no_biometric_credit':pub['US11792283B2']['F2_status']=='A' and float(pub['US11792283B2']['F2_to_F3_points'])==0,
 'architecture_functional_control':pub['US11792283B2']['F3_status']=='I',
 'adjective_safe_not_storage':'storage_only' not in json.loads(pub['US20140259847A1']['noise_flags']),
 'failed_identification_preserved':new['BC001-5946DA63E67B']['F2_to_F3_status']=='E',
 'cabinet_no_operation':new['BC001-A01F02870DCB']['F3_status']=='A' and 'storage_only' in json.loads(new['BC001-A01F02870DCB']['noise_flags']),
 'holster_no_operation':new['BC001-3F53B09CDA35']['F3_status']=='A' and 'holster_only' in json.loads(new['BC001-3F53B09CDA35']['noise_flags'])}
decision=decide(metrics['exp018a'],metrics['exp013'],metrics['exp016a'],all(preservation.values()))
top=lambda rs:{rid for rid,r in rs.items() if int(r['rank'])<=20}
old13top={r['record_id'] for r in mapping if int(r['v1_rank'])<=20}
overlap={'exp013':len(top(new)&old13top),'exp016a':len(top(new)&top(old))}
result={'experiment':'EXP-018A','freeze_commit':FREEZE,'decision':decision,'gold_denominator':10,'retrievable_denominator':6,'metrics':metrics,'top20_overlap_counts':overlap,'preservation_checks':preservation,'ranking_sha256':validation['ranking_sha256'],'not_retrieved':sorted(gold-set(pub)),'precision_at_20':'not calculated'}
dump(OUT/'metrics.json',result)
csvout(OUT/'gold-rank-movements.csv',movements)
decomp=[]
for m in movements:
    for version,data in [('EXP-016A',old),('EXP-018A',new)]:
        decomp.append({'publication':m['publication'],'experiment':version,'deteriorated_in_exp016a':m['exp016a_rank']>m['exp013_rank'],**data[m['record_id']]})
csvout(OUT/'gold-score-decomposition.csv',decomp)
csvout(OUT/'three-deteriorated-before-after.csv',[r for r in decomp if r['deteriorated_in_exp016a']])
variants=json.loads((EXP/'outputs/correction-variants.json').read_text())
goldids={r['record_id'] for r in movements}
impact=[]; detail=[]; examples=[]
prev='baseline'
for correction in ('outcomes','relationships','mechanism','storage'):
    a,b=variants[prev],variants[correction]
    changed=[]
    for rid in a:
        statechange=any(a[rid][k]!=b[rid][k] for k in ('features','relationships','flags','domain'))
        scored=a[rid]['score']!=b[rid]['score']
        if statechange or scored:
            d={'correction':correction,'record_id':rid,'title':new[rid]['title'],'known_gold':rid in goldids,'state_changed':statechange,'before_score':a[rid]['score'],'after_score':b[rid]['score'],'score_delta':b[rid]['score']-a[rid]['score'],'before_rank':a[rid]['rank'],'after_rank':b[rid]['rank'],'rank_improvement':a[rid]['rank']-b[rid]['rank'],'before_state':json.dumps(a[rid]),'after_state':json.dumps(b[rid])}
            changed.append(d);detail.append(d)
    non=[r for r in changed if not r['known_gold']]
    for direction,predicate in [('promoted',lambda r:r['rank_improvement']>0),('demoted',lambda r:r['rank_improvement']<0),('unchanged_rank',lambda r:r['rank_improvement']==0)]:
        subset=sorted([r for r in non if predicate(r)],key=lambda r:abs(r['score_delta']),reverse=True)[:2]
        examples.extend([dict(direction=direction,**r) for r in subset])
    impact.append({'correction':correction,'interpretation_state_changed':len(changed),'score_changed':sum(r['before_score']!=r['after_score'] for r in changed),'rank_changed_including_displacement':sum(a[r]['rank']!=b[r]['rank'] for r in a),'affected_non_gold':len(non),'direct_promoted':sum(r['rank_improvement']>0 for r in changed),'direct_demoted':sum(r['rank_improvement']<0 for r in changed),'classification':'Reusable engine logic plus BC001 configuration/feature adapter'})
    prev=correction
csvout(OUT/'correction-impact.csv',impact)
csvout(OUT/'affected-records.csv',detail)
csvout(OUT/'non-gold-examples.csv',examples)
dump(OUT/'access-provenance.json',{'freeze_commit':FREEZE,'freeze_committed_at':subprocess.check_output(['git','show','-s','--format=%cI',FREEZE],cwd=ROOT,text=True).strip(),'first_direct_mapping_read_at':first_mapping_read,'prior_evaluation_derivative_read':'EXP-016A movement and metrics read only after successful freeze commit, before 2026-09-18T12:08:30Z','ranking_commit_bytes_exact':True,'worktree_output_hashes':manifest['output_sha256'],'committed_output_hashes':commit_hashes,'line_endings':'Git normalized CRLF to LF for JSON artifacts; normalized bytes verified equal. All ranking CSV hashes match committed bytes exactly. No semantic or ranking changes after freeze.','sources':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in (mapping_path,gold_path)],'mapping_ambiguous_non_gold':sum(r['mapping_status']!='exact' for r in mapping),'gold_mapping_exact':6,'prior_knowledge':'D1 and user-disclosed diagnoses; no private mapping before freeze; diagnosis-informed experiment, not zero-prior-knowledge blinding'})
print(json.dumps({'metrics':result,'movements':movements,'impact':impact},indent=2))
