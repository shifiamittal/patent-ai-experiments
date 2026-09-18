# EXP-016A-D1 diagnostic provenance

Recorded 2026-09-18 (Asia/Calcutta). The user supplied the completed post-hoc
diagnoses and requested their verification and recording. Diagnostic statements
are attributed to that request and this frozen-artifact audit, not new analyst
relevance labels.

Repository: https://github.com/shifiamittal/patent-ai-experiments, branch main.
`git pull --ff-only origin main` reported already up to date at
`71e2439b61706774eae96eb865be0b620d2c2750`.
Authoritative implementation: `6f90e9a2e936cd95a78a8394d71586a0a34bf18d`.
Authoritative evaluation: `71e2439b61706774eae96eb865be0b620d2c2750`.
Decision-log number 0009 was available; existing duplicate 0008 entries were
preserved without renumbering.

## Sources read and unchanged SHA-256 hashes

| Source | SHA-256 |
|---|---|
| `experiments/BC001/EXP-016A/outputs/full-ranking.csv` | `3c9d95c4fce15f2794585637b2963893c437c9487b944d31070170ee1edbde4d` |
| `experiments/BC001/EXP-016A/evaluation/gold-rank-movements.csv` | `918e73f59ae3ee6b535e85bfe746058514caeb7101991fb5b572f01e660aa8d7` |
| `experiments/BC001/EXP-016A/scoring-spec.yaml` | `a576cb7df984bd7e9d2a9281ab8b82ffdbae80b6689df53ffa3009bbe5cb28f2` |
| `components/relevance-scorer/rs_v0.3_feature_aware_ta/scorer.py` | `735839bddb6c1dc6b6f1dbde1a3e0cb41b74e0cc126dc66bb0c9459e4532bd6a` |
| `components/relevance-scorer/rs_v0.3_feature_aware_ta/extraction-schema.json` | `af85f537d506ba095ae2f1bdcc6af8f0b056f6430a4f040b73dab5e28bb974b0` |
| `experiments/BC001/EXP-013/working-artifacts/input.json` | `3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508` |
| `experiments/BC001/EXP-016A/outputs/validation.json` | `29b6975616d5f277d23cbead7cb8b8e81c060b5564923050332c1ccef21efbb8` |

The frozen ranking hash is
`3c9d95c4fce15f2794585637b2963893c437c9487b944d31070170ee1edbde4d`;
the unchanged blind input hash is
`3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508`.
No private remapping or source-export access was needed: the existing six-row
GOLD movement file supplies the publication-to-Record-ID join. No web, claims,
full text, classification codes or citations were consulted.

## Method and validation

- Joined all six movement rows to the frozen CSV by Record ID; checked the
  stored EXP-016A rank and final score exactly. Existing EXP-013 ranks were copied,
  not recomputed. All original frozen fields are retained in the GOLD CSV.
- Parsed schema and scoring specification read-only. The schema enforces
  states/source/excerpts/reasoning, but cannot establish semantic causality or
  distinguish a physical safe from adjectival safe. This explains why structural
  validation did not detect the demonstrated semantic errors.
- For all 3,238 frozen rows, checked title/abstract equality with the original
  input and verified feature/relationship point multipliers. Summed component
  points using Decimal and checked penalties, strictest cap, rounding, floor
  and final score. This is arithmetic reconciliation of existing fields; it
  does not call extract(), score(), rank_records() or run_blind.py on the corpus.
- Verified 5246 nonempty stored/diagnostic excerpt occurrences,
  including domain, feature, relationship, gate and penalty evidence, as exact
  substrings of their declared original title/abstract field. Diagnostic quote
  columns identify source separately. No supporting words were fabricated for
  fields that were A in the original extraction.
- Reproduced 2,269 zero scores, F4 E=3/I=0, F2→F3 E=22/I=2/C=24, and the score-52
  rank interval 12–19. For that interval verified equal substantive tie fields
  and ascending lexical IDs. No ranking was generated or written.
- Statically read regex constants using Python AST and searched the specified
  texts: AUTH has zero matches for US10591237B1, STORAGE matches safe for
  US20140259847A1, and TARGET has zero matches for US20240384959A1. The production
  scorer was not imported for this diagnostic inspection or modified.
- Compared all 190 pairs within the frozen top 20 after NFKC, casefold and
  whitespace normalization. SequenceMatcher with autojunk=False and a 0.80
  review threshold found ranks 8/9 (1.0) and 13/15 (0.844104).
  Manually checked the two pairs' text. Similarity is a content diagnostic, not
  family identity or a new ranking/deduplication rule.
- Reproduced overlapping counts by filtering the diagnostic CSV to the three
  deteriorated records: extraction/gating 3/3; penalty/cap contribution 2/3;
  title/abstract limitation 2/3. These flags encode the supplied diagnoses,
  supported by the audit, rather than pretending to be mechanically measured
  ground truth. A pure weight-only failure is not established.

No alternative features, weights, scores, ranks, recall metrics or relevance
labels were assigned. The no-rerun restriction applies to the corpus; existing
unit tests exercise synthetic fixtures only. The preexisting tests are run
unchanged as requested; they are not evidence that semantic extraction is valid.

## Repository scope

Created exactly four files under diagnostics: the GOLD decomposition, top-20
pattern audit, root-cause summary and this provenance. Added decision-log 0009.
Modified only the EXP-016A README, its existing registry Learning/Notes fields,
and the dashboard's EXP-016A learning/diagnostic note. No D1 registry row or new
component version was created. EXP-016A remains REJECT; EXP-018 is a proposal only.

## Completed validation

- **Six GOLD rows and 20 top-20 rows:** every copied frozen column equals the
  authoritative ranking row exactly, including statuses, evidence, component
  points, penalties, caps, raw/final scores and ranks. All six existing rank
  movements reconcile. All-corpus arithmetic and excerpt checks passed as
  described above; counts agree with the supplied audit.
- **Tests:** 18/18 unchanged scorer tests and 6/6 unchanged evaluation-rule
  tests passed with Python 3.12.14. Commands, from the appropriate directories:
  `python -B -m unittest discover -s tests -v` (component directory) and
  `python -B -m unittest discover -s experiments/BC001/EXP-016A/evaluation -p test_evaluation.py -v`
  (repository root). Only synthetic fixtures ran; no corpus ranking was rerun.
- **Protected artifacts:** SHA-256 snapshots before editing and after validation
  agree for all 140 preexisting tracked files outside the three authorized
  modified files. Rankings, prior outputs and metrics, hashes, scorer/schema/spec,
  all benchmark files/GOLD identities, component registry and CURRENT_SYSTEM.yaml
  are byte-for-byte unchanged.
- **Registry:** row count and all fields except the existing EXP-016A Learning
  and Notes values are unchanged. No D1 row was added; Decision remains REJECT.
- **Dashboard:** Artifact Tool changed only `Dashboard!A98`,
  `'Experiment Log'!T19` and `'Experiment Log'!V19`. Read-only comparison of
  5,902 cells confirmed all other values, formulas and cached values, all cell
  styles, sheet names, row/column dimensions, merges, tables and data validations
  are preserved. Both affected views were rendered and visually checked; the
  formula-error scan reported zero matches. Existing metric cells are unchanged.
- **Scope:** no EXP-018 directory or component was created. The original
  untracked bc001_work, outputs and patent_sources directories remain untouched.

The post-hoc findings do not retroactively alter the blinded execution or its
decision. Any semantic-extractor experiment remains a separate future request.
