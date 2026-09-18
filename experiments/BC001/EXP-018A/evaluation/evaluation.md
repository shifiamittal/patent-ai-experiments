# EXP-018A evaluation

**PROMOTE** under the user's rule. All four recall metrics equal EXP-013 and median retrieved-GOLD rank improves by 35.5 (90.5 to 55). Relative to EXP-016A, Recall@20 improves by 1/10, Recall@100 by 1/10, Recall@200 by 2/10 and median improves by 87.5. All eight preservation checks pass. Promotion is scoped to the BC001 title/abstract reranker on RUN-012; it does not validate an end-to-end search system.

| Metric | EXP-013 | EXP-016A | EXP-018A |
|---|---:|---:|---:|
| Recall@20 | 2/10 | 1/10 | 2/10 |
| Recall@50 | 2/10 | 2/10 | 2/10 |
| Recall@100 | 4/10 | 3/10 | 4/10 |
| Recall@200 | 5/10 | 3/10 | 5/10 |
| Median retrieved GOLD rank | 90.5 | 142.5 | 55.0 |

Recall uses GOLD-10, including four unretrieved families. Conditional recall among the six retrievable families is 2/6, 2/6, 4/6 and 5/6 at the four cutoffs. Median uses those six only. This is known-positive benchmark recall, not exhaustive patent recall. Precision@20 was not calculated; EXP-013 adjudication was not transferred to EXP-018A.

Top-20 overlap: **8/20 (40%) with EXP-013**, **13/20 (65%) with EXP-016A**. Identical-content records remain separate, with original IDs and tie rules.

## Every retrieved GOLD

Positive improvement means earlier rank.

| Publication | EXP-013 | EXP-016A | EXP-018A | Improvement vs 013 | Improvement vs 016A |
|---|---:|---:|---:|---:|---:|
| US10107579B2 | 15 | 1 | 1 | 14 | 0 |
| US10591237B1 | 17 | 221 | 6 | 11 | 215 |
| US20240384959A1 | 83 | 64 | 124 | -41 | -60 |
| US20210080208A1 | 98 | 49 | 56 | 42 | -7 |
| US11792283B2 | 147 | 226 | 54 | 93 | 172 |
| US20140259847A1 | 555 | 2967 | 973 | -418 | 1994 |

## Complete score decomposition

All evidence excerpts, states and inference rationales are in `gold-score-decomposition.csv`. `three-deteriorated-before-after.csv` selects both rows for each of the three D1 deteriorated GOLD. The arithmetic is raw minus penalty, floor zero, bounded by the unchanged strictest cap.

| Publication | Version | Domain | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F2→F3 | F4→F3 | F5→F6 | Multi | Raw | Penalty | Cap | Final |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US10107579B2 | EXP-016A | 10.0 | 12.0 | 16.0 | 0.0 | 10.0 | 4.0 | 0.0 | 0.0 | 14.0 | 0.0 | 1.0 | 2.0 | 69.0 | 0 | 100 | 69.0 |
| US10107579B2 | EXP-018A | 10.0 | 12.0 | 16.0 | 0.0 | 10.0 | 4.0 | 0.0 | 0.0 | 14.0 | 0.0 | 1.0 | 2.0 | 69.0 | 0 | 100 | 69.0 |
| US10591237B1 | EXP-016A | 8.0 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 18.0 | 0 | 100 | 18.0 |
| US10591237B1 | EXP-018A | 8.0 | 12.0 | 16.0 | 0.0 | 10.0 | 0.0 | 0.0 | 0.0 | 14.0 | 0.0 | 0.0 | 2.0 | 62.0 | 0 | 100 | 62.0 |
| US20240384959A1 | EXP-016A | 10.0 | 12.0 | 5.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 27.6 | 0 | 100 | 27.6 |
| US20240384959A1 | EXP-018A | 10.0 | 12.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 22.0 | 0 | 100 | 22.0 |
| US20210080208A1 | EXP-016A | 10.0 | 0.0 | 16.0 | 0.0 | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 29.5 | 0 | 100 | 29.5 |
| US20210080208A1 | EXP-018A | 10.0 | 0.0 | 16.0 | 0.0 | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 29.5 | 0 | 100 | 29.5 |
| US11792283B2 | EXP-016A | 10.0 | 0.0 | 0.0 | 0.0 | 10.0 | 4.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 25.0 | 8 | 100 | 17.0 |
| US11792283B2 | EXP-018A | 10.0 | 0.0 | 5.6 | 0.0 | 10.0 | 4.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 30.6 | 0 | 100 | 30.6 |
| US20140259847A1 | EXP-016A | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 | 8 | 15 | 0.0 |
| US20140259847A1 | EXP-018A | 10.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 | 8 | 100 | 2.0 |

US10591237B1 now receives explicit F2/F3/F2→F3 from its stated invalid-fingerprint trigger disablement. Its 18→62 change includes the existing multi-primary bonus when the corrected features satisfy the unchanged rule.

US11792283B2 gains inferred F3 (5.6) from registered profiles accessing firearm-coupled authentication devices plus the stated firearm lock. Both facts and the inference are recorded. Its functional architecture removes the false 8-point penalty: 17→30.6. F2 and F2→F3 stay absent/zero; no biometric evidence is invented.

US20140259847A1 loses the false storage classification and regains firearm domain points (2→10). Its sparse safety description still lacks a qualifying mechanism, so the unchanged 8-point penalty remains. Final score 0→2 and rank 2967→973, still worse than EXP-013's 555. Removing this remaining penalty merely to improve its rank would exceed the demonstrated evidence.

US20240384959A1 loses unsupported inferred F3 (5.6): the selected evidence concerns target identity without a supported authentication-to-operation dependency. It falls 64→124. The known targeting-penalty extraction issue was outside the approved four corrections and remains unaltered. US20210080208A1 keeps its score and moves 49→56 through displacement.

BC001-5946DA63E67B preserves explicit failed-identification/trigger-blocking evidence and score 52. BC001-A01F02870DCB is a cabinet in the frozen text, not a holster; fire extinguishing supplies no firing credit, and its final score is 14 under the storage gate. BC001-3F53B09CDA35 is the holster boundary; F3 and its biometric-operation relationship are absent, and both holster/storage gates apply with the existing strictest cap 15.

## Corpus impact

Sequential marginal attribution order: outcomes → relationships → mechanism → storage. All variants were frozen before private mapping access. Counts overlap and are order-dependent. Interpretation means a feature/relationship state, flag or domain changed; verbatim-evidence-only edits are not counted here. Score changes and all rank changes (including displacement) are separate.

| Correction | Interpretation changed / 3238 | Score changed / 3238 | Affected non-GOLD | Rank changed including displacement |
|---|---:|---:|---:|---:|
| outcomes | 7 | 7 | 6 | 609 |
| relationships | 61 | 61 | 59 | 3220 |
| mechanism | 111 | 40 | 110 | 3179 |
| storage | 63 | 60 | 62 | 2953 |

Some outcome-only operational credits are removed by the subsequent relationship correction. Intermediate variants are attribution artifacts, not endorsed alternative rankings. The mechanism correction changes 111 records but only 40 scores: score floors/caps can hide a penalty removal; penalty tie-breaking can still change rank. Full per-record changes are in `affected-records.csv`.

## Scope, validation and generalization

66 tests pass: 36 new-version scorer tests (18 inherited plus 18 repair tests), 18 unchanged rs_v0.3 tests, six unchanged EXP-016A decision tests and six EXP-018A decision tests. Full-corpus checks cover 3,238 unique unchanged identities, exact title/abstract equality, supported excerpts, reasoned inferences, recomputed scores, valid bounds and ranks, and identical shuffled-input ranking. AST comparison preserves scoring/sanitization/tie functions; constants and the specification/schema are unchanged. Attribution baseline exactly reproduces EXP-016A and its final endpoint exactly reproduces EXP-018A.

No approved correction required a scoring-policy change. The remaining sparse-evidence penalty is retained. Numeric weights, evidence multipliers, penalties, caps, tie breaks, labels, retrieval universe and terminology source remain fixed. rs_v0.3 is unchanged.

Mechanism-general; validated on BC001 only. These deterministic rules are not cross-domain validated or exhaustive semantic interpretation. D1 and the request exposed diagnostic identities; private mapping access followed freeze commit `0303428d542c279410b9166bf02822cf5f084f22`. The isolated ranking runner received only allowlisted title/abstract inputs and policy/code. All six reconstructed GOLD mappings are exact; 23 ambiguous non-GOLD mappings remain unresolved. The original private key is unavailable. No scorer or ranking changes followed unblinding.

`access-provenance.json` records source hashes and both worktree/commit hashes. Git normalized JSON line endings; normalized contents match the freeze, and every ranking CSV matches its committed SHA-256 exactly.
