# Decision 0008: reject EXP-016A

The frozen rs_v0.3_feature_aware_ta challenger fails the preregistered rule.
Recall@20 declined from 2/10 to 1/10, and median rank of six retrieved GOLD
families worsened from 90.5 to 142.5, exceeding the 10% rejection threshold.
Recall@50 is 2/10, Recall@100 is 3/10, and Recall@200 is 3/10.

The ranking contains all 3,238 anonymous records exactly once, with deterministic
ordering and code-calculated scores. The private mapping and GOLD key were read
only after the ranking was frozen and hashed. All six relevant reconstructed
mapping entries are exact; no ambiguous source candidate was arbitrarily chosen.

This rejects this implemented challenger. It does not isolate whether the
numerical weight hypothesis or the deterministic extraction rules caused the
loss, and it does not establish analyst relevance accuracy. Preserve the frozen
outputs for diagnosis; do not retune EXP-016A using these results.

The component remains recorded as a rejected challenger. No champion or
current-system change is made. Earlier experiments and benchmark labels remain
unchanged. See `experiments/BC001/EXP-016A/evaluation/evaluation.md`.
