"""Record the frozen evaluation and append registry rows without historical edits."""
import csv
import io
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
E=EXP/'evaluation'
def read(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
m=json.loads((E/'metrics.json').read_text())
mov=read(E/'gold-rank-movements.csv'); impact=read(E/'correction-impact.csv'); examples=read(E/'non-gold-examples.csv')
decomp=read(E/'gold-score-decomposition.csv')
table='\n'.join('| '+label+' | '+' | '.join(str(m['metrics'][v][key])+('/10' if key!='median' else '') for v in ('exp013','exp016a','exp018a'))+' |' for label,key in [('Recall@20','r20'),('Recall@50','r50'),('Recall@100','r100'),('Recall@200','r200'),('Median retrieved GOLD rank','median')])
movement='\n'.join(f"| {r['publication']} | {r['exp013_rank']} | {r['exp016a_rank']} | {r['exp018a_rank']} | {r['exp013_improvement']} | {r['exp016a_improvement']} |" for r in mov)
points=['domain','F2','F3','F4','F5','F6','F7','F8','F2_to_F3','F4_to_F3','F5_to_F6','multi_primary']
scoretable='\n'.join('| '+r['publication']+' | '+r['experiment']+' | '+' | '.join(r[k+'_points'] for k in points)+' | '+r['raw_score']+' | '+r['penalty_points']+' | '+r['hard_cap']+' | '+r['final_score']+' |' for r in decomp)
impacttable='\n'.join(f"| {r['correction']} | {r['interpretation_state_changed']} | {r['score_changed']} | {r['affected_non_gold']} | {r['rank_changed_including_displacement']} |" for r in impact)
text=f'''# EXP-018A evaluation

**PROMOTE** under the user's rule. All four recall metrics equal EXP-013 and median retrieved-GOLD rank improves by 35.5 (90.5 to 55). Relative to EXP-016A, Recall@20 improves by 1/10, Recall@100 by 1/10, Recall@200 by 2/10 and median improves by 87.5. All eight preservation checks pass. Promotion is scoped to the BC001 title/abstract reranker on RUN-012; it does not validate an end-to-end search system.

| Metric | EXP-013 | EXP-016A | EXP-018A |
|---|---:|---:|---:|
{table}

Recall uses GOLD-10, including four unretrieved families. Conditional recall among the six retrievable families is 2/6, 2/6, 4/6 and 5/6 at the four cutoffs. Median uses those six only. This is known-positive benchmark recall, not exhaustive patent recall. Precision@20 was not calculated; EXP-013 adjudication was not transferred to EXP-018A.

Top-20 overlap: **8/20 (40%) with EXP-013**, **13/20 (65%) with EXP-016A**. Identical-content records remain separate, with original IDs and tie rules.

## Every retrieved GOLD

Positive improvement means earlier rank.

| Publication | EXP-013 | EXP-016A | EXP-018A | Improvement vs 013 | Improvement vs 016A |
|---|---:|---:|---:|---:|---:|
{movement}

## Complete score decomposition

All evidence excerpts, states and inference rationales are in `gold-score-decomposition.csv`. `three-deteriorated-before-after.csv` selects both rows for each of the three D1 deteriorated GOLD. The arithmetic is raw minus penalty, floor zero, bounded by the unchanged strictest cap.

| Publication | Version | Domain | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F2→F3 | F4→F3 | F5→F6 | Multi | Raw | Penalty | Cap | Final |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{scoretable}

US10591237B1 now receives explicit F2/F3/F2→F3 from its stated invalid-fingerprint trigger disablement. Its 18→62 change includes the existing multi-primary bonus when the corrected features satisfy the unchanged rule.

US11792283B2 gains inferred F3 (5.6) from registered profiles accessing firearm-coupled authentication devices plus the stated firearm lock. Both facts and the inference are recorded. Its functional architecture removes the false 8-point penalty: 17→30.6. F2 and F2→F3 stay absent/zero; no biometric evidence is invented.

US20140259847A1 loses the false storage classification and regains firearm domain points (2→10). Its sparse safety description still lacks a qualifying mechanism, so the unchanged 8-point penalty remains. Final score 0→2 and rank 2967→973, still worse than EXP-013's 555. Removing this remaining penalty merely to improve its rank would exceed the demonstrated evidence.

US20240384959A1 loses unsupported inferred F3 (5.6): the selected evidence concerns target identity without a supported authentication-to-operation dependency. It falls 64→124. The known targeting-penalty extraction issue was outside the approved four corrections and remains unaltered. US20210080208A1 keeps its score and moves 49→56 through displacement.

BC001-5946DA63E67B preserves explicit failed-identification/trigger-blocking evidence and score 52. BC001-A01F02870DCB is a cabinet in the frozen text, not a holster; fire extinguishing supplies no firing credit, and its final score is 14 under the storage gate. BC001-3F53B09CDA35 is the holster boundary; F3 and its biometric-operation relationship are absent, and both holster/storage gates apply with the existing strictest cap 15.

## Corpus impact

Sequential marginal attribution order: outcomes → relationships → mechanism → storage. All variants were frozen before private mapping access. Counts overlap and are order-dependent. Interpretation means a feature/relationship state, flag or domain changed; verbatim-evidence-only edits are not counted here. Score changes and all rank changes (including displacement) are separate.

| Correction | Interpretation changed / 3238 | Score changed / 3238 | Affected non-GOLD | Rank changed including displacement |
|---|---:|---:|---:|---:|
{impacttable}

Some outcome-only operational credits are removed by the subsequent relationship correction. Intermediate variants are attribution artifacts, not endorsed alternative rankings. The mechanism correction changes 111 records but only 40 scores: score floors/caps can hide a penalty removal; penalty tie-breaking can still change rank. Full per-record changes are in `affected-records.csv`.

## Scope, validation and generalization

66 tests pass: 36 new-version scorer tests (18 inherited plus 18 repair tests), 18 unchanged rs_v0.3 tests, six unchanged EXP-016A decision tests and six EXP-018A decision tests. Full-corpus checks cover 3,238 unique unchanged identities, exact title/abstract equality, supported excerpts, reasoned inferences, recomputed scores, valid bounds and ranks, and identical shuffled-input ranking. AST comparison preserves scoring/sanitization/tie functions; constants and the specification/schema are unchanged. Attribution baseline exactly reproduces EXP-016A and its final endpoint exactly reproduces EXP-018A.

No approved correction required a scoring-policy change. The remaining sparse-evidence penalty is retained. Numeric weights, evidence multipliers, penalties, caps, tie breaks, labels, retrieval universe and terminology source remain fixed. rs_v0.3 is unchanged.

Mechanism-general; validated on BC001 only. These deterministic rules are not cross-domain validated or exhaustive semantic interpretation. D1 and the request exposed diagnostic identities; private mapping access followed freeze commit `{m['freeze_commit']}`. The isolated ranking runner received only allowlisted title/abstract inputs and policy/code. All six reconstructed GOLD mappings are exact; 23 ambiguous non-GOLD mappings remain unresolved. The original private key is unavailable. No scorer or ranking changes followed unblinding.

`access-provenance.json` records source hashes and both worktree/commit hashes. Git normalized JSON line endings; normalized contents match the freeze, and every ranking CSV matches its committed SHA-256 exactly.
'''
(E/'evaluation.md').write_text(text,encoding='utf-8',newline='\n')
risks={
'outcomes':('Reusable outcome detection; BC001 BIO/auth adapter','Credential-adjacent validity can refer to another device; outcome-only over-credit is filtered by relationship rules.','test_failed_biometric, test_success, test_failed_identification_preserved / test_invalid_noncredential, test_generic_auth_no_biometric'),
'relationships':('Reusable controlled-action and causal/adjacent-sentence linking; BC001 firearm-lock architecture inference and F2/F3 mapping','Ambiguous pronouns, component lists and multiple authenticators may still imply a dependency incorrectly; distant paraphrases can be missed.','test_cross_sentence_explicit, test_cross_sentence_inferred, test_architecture_inference_without_biometrics / test_unsupported_absent, test_holster_trigger_access'),
'mechanism':('Reusable functional component detector; BC001 relevant-function vocabulary','Nearby function words can describe another component; named functional devices may be underspecified. Existing mechanism whitelist behavior is preserved.','test_functional_architecture / test_bare_architecture'),
'storage':('Reusable word-sense masking and object/action checks; BC001 container, adjective and holster boundaries','Translated casing/box senses and dual-purpose objects remain ambiguous. The observed table-corner pistol box is still not recognized as storage because box is outside the bounded container vocabulary; it receives no F3 credit.','test_physical_storage, test_adjective_safe, test_dual_system / test_extinguishing, test_holster_trigger_access, test_holster_passive_protection')}
parts=['# Correction-by-correction diagnostic comparison\n\nMechanism-general; validated on BC001 only. Examples are known non-GOLD, not analyst relevance negatives. Ranks/scores below are sequential marginal effects; final ranking may include additional corrections.\n']
for c in risks:
    scope,risk,tests=risks[c]
    parts.append(f'## {c}\n\nClassification: {scope}.\n\nFalse-positive/negative risks: {risk}\n\nPositive / negative regressions: {tests}.\n\n| Direction | Non-GOLD record | Title | Score before → after | Rank before → after |\n|---|---|---|---:|---:|')
    for r in examples:
        if r['correction']==c: parts.append(f"| {r['direction']} | {r['record_id']} | {r['title']} | {r['before_score']} → {r['after_score']} | {r['before_rank']} → {r['after_rank']} |")
    if c in ('outcomes','mechanism'): parts.append('\nNo directly demoted record exists for this correction in its marginal variant. Other records can fall through displacement; those are not direct correction examples.')
    if c=='outcomes': parts.append('\nThe two illustrated outcome-only firing promotions are canceled by the relationship step (final score 10 each), exposing why the fixes must be combined. Two additional surviving non-GOLD outcome changes are BC001-C45844564B37 (cabinet, F2 detection, 12→15) and BC001-F30F8987C7B9 (pistol box, F2 detection, 10→22); neither receives F3 in the final ranking.')
(E/'diagnostic-comparison.md').write_text('\n'.join(parts)+'\n',encoding='utf-8',newline='\n')
(EXP/'decision.md').write_text('# EXP-018A decision\n\n**PROMOTE** as the BC001 title/abstract reranker under the supplied experiment rule. Recall@20/50/100/200 matches EXP-013 (2/10, 2/10, 4/10, 5/10); median improves 90.5→55. All preservation checks pass.\n\nThe promotion is formally recorded in this evaluation commit. CURRENT_SYSTEM.yaml updates only the reranker/champion designation and scope notes. Retrieval and evidence-assistant versions, benchmark and validation limitations remain unchanged. This is not an end-to-end or cross-domain validation. See evaluation/evaluation.md and evaluation/diagnostic-comparison.md for individual regressions, corpus effects and limitations.\n',encoding='utf-8',newline='\n')

registry=ROOT/'experiment_registry.csv'; original=registry.read_bytes()
reader=csv.DictReader(io.StringIO(original.decode('utf-8-sig'))); rows=list(reader)
assert not any(r['Experiment ID']=='EXP-018A' for r in rows)
row=dict.fromkeys(reader.fieldnames,'')
row.update({'Experiment ID':'EXP-018A','Date':'2026-09-18','Benchmark ID':'BC001','Benchmark Version':'0.1-provisional','Base System':'EXP-013 on RUN-012','Challenger System':'rs_v0.4_extraction_gate_repair_ta','Hypothesis / Objective':'Repair extraction/gating with fixed scoring and title/abstract evidence','Primary Component Changed':'Relevance Scorer','From Version':'rs_v0.3_feature_aware_ta','To Version':'rs_v0.4_extraction_gate_repair_ta','What Changed':'Authentication outcomes; causal linking; functional mechanism; storage/object senses','Recall@50':.2,'Recall@100':.4,'Precision@20':'N/A','Gold in Top 10':2,'Median Rank of Retrieved GOLD':55,'Analyst Minutes':'N/A','Model Cost USD':'N/A','Guardrail / Side Effect':'R20 2/10; R200 5/10. Individual ranks mixed.','Learning':'Recall matches EXP-013; median 90.5 to 55. BC001 only.','Decision':'PROMOTE','Notes':'Frozen before private mapping. Fixed scoring. 66 tests. TA reranker scope only.'})
buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=reader.fieldnames,lineterminator='\n');w.writerow(row)
registry.write_bytes(original+buf.getvalue().encode())
(E/'dashboard-row.json').write_text(json.dumps({'headers':reader.fieldnames,'values':[row[k] for k in reader.fieldnames]},indent=2)+'\n',encoding='utf-8')
cpath=ROOT/'components/component_registry.csv';original=cpath.read_bytes();reader=csv.DictReader(io.StringIO(original.decode('utf-8-sig')));list(reader)
buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=reader.fieldnames,lineterminator='\n');w.writerow(dict(component='Relevance Scorer',version='rs_v0.4_extraction_gate_repair_ta',role='BC001 title/abstract champion',experiment='EXP-018A',decision='PROMOTE',current='true',champion='true',implementation='components/relevance-scorer/rs_v0.4_extraction_gate_repair_ta/'))
cpath.write_bytes(original+buf.getvalue().encode())
(ROOT/'decision-log/0010-promote-exp018a-extraction-gate-repair.md').write_text((EXP/'decision.md').read_text()+'\nRanking-freeze commit: '+m['freeze_commit']+'. Input and output SHA-256 hashes and mapping-access chronology are recorded in EXP-018A. No code/ranking retuning after evaluation.\n',encoding='utf-8',newline='\n')
print('Recorded evaluation, diagnostic comparison, formal promotion and registry rows.')
