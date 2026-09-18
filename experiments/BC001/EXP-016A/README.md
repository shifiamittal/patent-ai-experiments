# EXP-016A

Result: **REJECT**. Recall@20/50/100/200: **1/10, 2/10, 3/10, 3/10**.
Median rank of six retrieved GOLD: **142.5** (EXP-013: 90.5).
The early-recall guardrail and median-rank rejection condition failed.

Feature-aware title/abstract challenger ranking of the unchanged 3,238 RUN-012
anonymous records. See `experiment-definition.md`, `scoring-spec.yaml`, and
`provenance.md`. Final ranking and evidence are under `outputs/`; post-freeze
comparison and decision are under `evaluation/` and `decision.md`.

The scorer is `components/relevance-scorer/rs_v0.3_feature_aware_ta/`. The
experiment preserves all earlier artifacts, benchmark labels and CURRENT_SYSTEM.
The exact approved user specification is preserved as `authoritative-request.txt`;
that complete file includes evaluation information and is never a runner input.

`prepare.py` stages the blind workspace (its source-attachment path is local
provenance; future runs can copy the six canonical files directly). The runner
validates the input hash and does not overwrite frozen outputs. Reproduction
must use a fresh staging directory and must not replace this experiment's freeze.

## D1 post-hoc scorer failure audit

[EXP-016A-D1](diagnostics/root-cause-summary.md) records six GOLD score
decompositions and a frozen top-20 pattern audit. Among the three deteriorated
GOLD records, extraction/gating errors affect 3/3, penalties/caps contribute to
2/3, and title/abstract evidence limitations affect 2/3 (overlapping counts).
The audit identifies semantic relationship and domain-boundary failures; it does
not establish a weight-only failure. EXP-016A remains **REJECT**.

Do not tune weights first or extend the current pattern extractor to full text.
EXP-018 is proposed only: semantic/LLM title/abstract extraction with the formula,
weights, benchmark, 3,238-record universe and input frozen. D1 neither creates
nor runs it, changes a ranking, nor assigns new analyst relevance labels.
