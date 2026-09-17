# EXP-016A evaluation

Decision: **REJECT**. early-recall guardrail failed; median rank worsened by more than 10%.

| Metric | EXP-013 | EXP-016A |
|---|---:|---:|
| Recall@20 | 2/10 | 1/10 |
| Recall@50 | 2/10 | 2/10 |
| Recall@100 | 4/10 | 3/10 |
| Recall@200 | 5/10 | 3/10 |
| Median rank of six retrieved GOLD | 90.5 | 142.5 |

Recall uses the ten known-good GOLD families as denominator. The four unretrieved
families remain misses; the median uses only the six retrieved families. This is
known-good benchmark recall, not exhaustive prior-art recall. Precision@20 was
neither calculated nor claimed.

| GOLD publication | EXP-013 rank | EXP-016A rank | Improvement (old minus new) |
|---|---:|---:|---:|
| US10107579B2 | 15 | 1 | +14 |
| US10591237B1 | 17 | 221 | -204 |
| US20240384959A1 | 83 | 64 | +19 |
| US20210080208A1 | 98 | 49 | +49 |
| US11792283B2 | 147 | 226 | -79 |
| US20140259847A1 | 555 | 2967 | -2412 |

All six retrieved GOLD mappings are exact normalized-content matches in the
post-experiment reconstruction. Its 23 ambiguous non-GOLD rows remain unassigned;
they do not affect these GOLD metrics. The original private key is unavailable.
The six old ranks independently reproduce all four canonical comparator recall
values and its 90.5 median.

The first private read was 2026-09-17T17:59:30.1894059Z, after the freeze at
2026-09-17T17:58:29.367987+00:00 and implementation commit `6f90e9a2e936cd95a78a8394d71586a0a34bf18d`.
The parent saw aggregate comparator totals in the user request, but no private
identities, GOLD labels, or prior individual ranks until after freeze. The runner
received no evaluation artifacts. No post-unblinding scorer/ranking edits occurred.

The feature extractor is rule-based and its semantic judgments are not analyst
validated. The 18 synthetic tests, exact coverage, excerpt checks, bounded
arithmetic, and shuffled-input equality passed. Application-level filesystem
restriction was used rather than an OS/container mount boundary. These limits
are preserved in provenance and are not evidence of analyst relevance accuracy.

CURRENT_SYSTEM.yaml, benchmark labels, GOLD-10 and earlier experiments remain
unchanged. This component remains registered as a challenger, regardless of the
decision label, pending any separately authorized promotion action.
