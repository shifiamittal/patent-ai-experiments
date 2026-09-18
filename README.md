# Patent Search AI Experiment Repository

Canonical state as of 2026-09-16.

## Source of truth
- Benchmark: BC001-v0.1-provisional
- Current retrieval baseline: RUN-012, 3,238-family FAMPAT export (AND variant)
- Current reranker: EXP-018A, rs_v0.4_extraction_gate_repair_ta (formally promoted 2026-09-18)
- Most validated AI capability: EXP-011 evidence-assisted full-text review
- BC001 title/abstract reranker champion: EXP-018A. No end-to-end champion system is validated.
- Search Controller is not implemented/validated.

## Provenance rules
1. Analyst-confirmed facts are separate from AI-generated interpretations.
2. Executed Orbit results are separate from proposed queries.
3. Result counts belong only to their exact query/database/run snapshot.
4. 3,091 RUN-005A and 3,238 RUN-012 are separate versions.
5. GOLD-10 is a known-good set, not exhaustive recall ground truth.
6. PA-001 is complete: EXP-013 publication-level Precision@20 is 9/20 (45%); analyst-report-group inclusion yield is 7/17 (41.2%). These denominators are distinct.

## EXP-013 adjudication completion
- Decision remains HOLD / INCONCLUSIVE: V0 top 20 lacks equivalent adjudication.
- Current results: `experiments/BC001/EXP-013/top20-metrics.json` and `top20-adjudication-provenance.md`.
- Net-new relevant-family yield and analyst review minutes remain N/A.
- The original private key is unavailable; the post-experiment reconstructed mapping retains ambiguous identical-content sets without guessing.
- Evaluator-only export and mapping: `benchmarks/BC001-smartgun/restricted-evaluation/`. Follow its README to exclude these files and all evaluation labels from future blind-run workspaces.
- `CURRENT_SYSTEM.yaml`, original pending templates, and partial snapshots are preserved. Current PA-001 status is recorded separately in `benchmarks/BC001-smartgun/pending-validation/PA-001-status.yaml`.

See docs/canonical-current-state-2026-09-16.md.

## EXP-018A extraction/gating repair
- PROMOTE: Recall@20/50/100/200 matches EXP-013 (2/10, 2/10, 4/10, 5/10); median of six retrieved GOLD improves 90.5 to 55.
- Scoring policy and RUN-012 title/abstract input remain fixed; ranking committed before private mapping access.
- See `experiments/BC001/EXP-018A/evaluation/evaluation.md` for individual rank regressions, decomposition, impact counts and limitations.
- Mechanism-general; validated on BC001 only.
