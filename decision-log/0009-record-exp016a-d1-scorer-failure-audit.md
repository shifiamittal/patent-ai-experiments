# Decision 0009: record EXP-016A-D1 scorer failure audit

Record the completed post-hoc failure audit against EXP-016A's frozen output.
EXP-016A remains **REJECT**. D1 is a diagnostic, not a new experiment or component
version, and does not change any score, rank, metric or analyst relevance label.

Among the three deteriorated GOLD records, extraction/gating errors affect 3/3,
penalty/cap contributions affect 2/3, and genuine title/abstract evidence limits
affect 2/3. These categories overlap. A pure numerical-weight failure with
otherwise correct extraction is not established. The false storage cap is
non-binding; its domain gate and the applied penalty suppress the score.

EXP-016A failed primarily because the deterministic pattern-based extractor
could not reliably interpret semantic feature relationships and domain
boundaries. The audit does not establish that numerical weights alone caused
the failure. Do not tune weights first or apply this extractor to full text,
where additional text may increase accidental co-occurrence and false relations.

Propose EXP-018 to replace deterministic title/abstract extraction with structured
semantic/LLM evidence extraction, freezing EXP-016A's numerical formula, weights,
benchmark, exact 3,238-record universe and title/abstract input. Do not create or
execute EXP-018 in this diagnostic task. No promotion or current-system change.

See [root-cause summary](../experiments/BC001/EXP-016A/diagnostics/root-cause-summary.md)
and [diagnostic provenance](../experiments/BC001/EXP-016A/diagnostics/diagnostic-provenance.md).
