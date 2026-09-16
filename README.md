# Patent Search AI Experiment Repository

Canonical state as of 2026-09-16.

## Source of truth
- Benchmark: BC001-v0.1-provisional
- Current retrieval baseline: RUN-012, 3,238-family FAMPAT export (AND variant)
- Current reranker candidate: EXP-013, rs_v0.2_blind_ta_rerank
- Most validated AI capability: EXP-011 evidence-assisted full-text review
- No champion system has been designated.
- Search Controller is not implemented/validated.

## Provenance rules
1. Analyst-confirmed facts are separate from AI-generated interpretations.
2. Executed Orbit results are separate from proposed queries.
3. Result counts belong only to their exact query/database/run snapshot.
4. 3,091 RUN-005A and 3,238 RUN-012 are separate versions.
5. GOLD-10 is a known-good set, not exhaustive recall ground truth.
6. Precision@20 is pending until PA-001 is complete.

See docs/canonical-current-state-2026-09-16.md.
