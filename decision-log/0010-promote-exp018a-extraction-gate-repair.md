# EXP-018A decision

**PROMOTE** as the BC001 title/abstract reranker under the supplied experiment rule. Recall@20/50/100/200 matches EXP-013 (2/10, 2/10, 4/10, 5/10); median improves 90.5→55. All preservation checks pass.

The promotion is formally recorded in this evaluation commit. CURRENT_SYSTEM.yaml updates only the reranker/champion designation and scope notes. Retrieval and evidence-assistant versions, benchmark and validation limitations remain unchanged. This is not an end-to-end or cross-domain validation. See evaluation/evaluation.md and evaluation/diagnostic-comparison.md for individual regressions, corpus effects and limitations.

Ranking-freeze commit: 0303428d542c279410b9166bf02822cf5f084f22. Input and output SHA-256 hashes and mapping-access chronology are recorded in EXP-018A. No code/ranking retuning after evaluation.
