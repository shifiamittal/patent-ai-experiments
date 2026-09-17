# EXP-016A preregistered definition

Change only the Relevance Scorer to rs_v0.3_feature_aware_ta. The universe is the
exact 3,238 anonymous title/abstract records used in EXP-013. Input SHA-256:
`3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508`.
Stop if it differs. Frozen disclosure and F1–F8 are in `frozen-disclosure.md`.
The approved numerical weights are a challenger hypothesis, not analyst truth.

Ranking inputs are limited to the blind input, frozen disclosure/specification,
and ranking implementation/schema. The parent reviewed repository governance;
the child process receives a fresh allowlisted workspace outside Git. It cannot
read the parent checkout through its restricted file-access policy.

Phase 1: extract evidence, calculate through code, validate exactly-once coverage
and deterministic ordering, write and SHA-256 freeze all three CSVs. Phase 2:
verify those hashes, then read private mapping and GOLD key and EXP-013 ranks.
No changes to scorer or frozen outputs after that boundary.

Recall denominators are GOLD-10, not the six retrieved families. Compute
Recall@20/50/100/200 and the median of six retrieved GOLD ranks. Never calculate
Precision@20. Identity ambiguity must be exposed rather than assigned arbitrarily.

PROMOTE requires Recall@100 ≥ 5/10 OR median rank ≤ 75, AND Recall@20 ≥ 2/10,
Recall@50 ≥ 2/10, Recall@200 ≥ 5/10, no identity/GOLD/prior-rank leakage and
exactly-once coverage. REJECT if an early recall guardrail fails, median exceeds
99.55 (90.5 × 1.10), identity/GOLD/prior-rank leakage occurs, or no meaningful
improvement accompanies worse reproducibility. Otherwise HOLD / INCONCLUSIVE.
Evaluate REJECT conditions first if predicates conflict. This disambiguates
precedence without weakening any rejection rule. A PROMOTE decision alone does
not authorize a CURRENT_SYSTEM.yaml update or designation as champion.

The user supplied aggregate comparator totals in the approved request before
execution. They were not passed to the runner. They contain no record identities
or individual ranks. Private evaluation artifacts remain sealed until freeze.
