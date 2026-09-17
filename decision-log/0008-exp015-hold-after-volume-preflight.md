# Decision 0008: EXP-015 HOLD after volume preflight

Date: 2026-09-17

EXP-015 placed on HOLD after feature-specific query volume preflight.

Status: HOLD — DESIGN REVISION REQUIRED AFTER VOLUME PREFLIGHT.

The analyst executed EXP015-015A-Q1 and Q2 in Orbit/FAMPAT, Title, Abstract and Claims only, without other filters. Counts were 23,935 and 493,993 FAMPAT families respectively. Neither was exported. All remaining queries are paused and the same-session baseline was not rerun. Final retrieval metrics remain N/A.

This is a query-design volume failure, not a confirmed Orbit syntax failure. The original planning ranges were materially inaccurate. Broad document-level AND retrieval needs Search Controller volume checks, proximity or functional relationships, and controlled handling of high-collision terms. The current Q1/Q2 operational form failed; feature-specific retrieval as a principle remains open.

No component is promoted or rejected as a whole. No replacement queries are generated. CURRENT_SYSTEM.yaml, benchmark files, RUN-012 and prior experiments remain unchanged.

Evidence and query statuses: [EXP-015 record](../experiments/BC001/EXP-015/README.md). Screenshots are external and were not supplied to Codex.
