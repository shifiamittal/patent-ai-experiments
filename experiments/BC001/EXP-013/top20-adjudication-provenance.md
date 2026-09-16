# EXP-013 completed top-20 adjudication

PA-001: **COMPLETED**. EXP-013 decision/status: **HOLD / INCONCLUSIVE**.
V0's top 20 has not received equivalent analyst adjudication, so no comparative
promotion decision is supported. No component is promoted and no EXP-014 is
created or run.

## Continuation of the partial update

This completion extends the existing uncommitted partial adjudication. Its 14
labels, Include decisions, reasons, and analyst family statements are preserved.
The four previously pending records receive the user's completed adjudications
in `top20-adjudication.csv`. KZ6216U is explicitly an abstract-only L/No judgment;
completion does not imply that full text became available for that record.

The `partial-top20-*` files remain byte-for-byte historical snapshots. Their
pending metrics and private-key blocker are superseded for current evaluation
by this note, `top20-metrics.json`, and the explicitly authorized reconstructed
mapping. The original V1 metrics and ranking remain unchanged.

## Reconstructed identity evaluation

The unavailable original `BC001_Private_Evaluation_Key.xlsx` is not claimed to
have been recovered. The original source export is stored byte-for-byte at
`benchmarks/BC001-smartgun/restricted-evaluation/RUN-012/source-export.xlsx`.
The new mapping is
`benchmarks/BC001-smartgun/restricted-evaluation/EXP-013/reconstructed-evaluation-mapping.csv`.
Its source manifest contains SHA-256 checksums. This is post-experiment matching
and evaluation only; no scores, reasons, ordering, or feature judgments were
regenerated or altered.

The preserved blind input agrees with the downloaded blinded-input workbook,
and all 3,238 ranked workbook rows agree with the historical ranked JSON. Exact
normalized title/abstract matching accounts for 3,215 individual matches plus
23 anonymous records in 11 identical-content groups. All 3,238 source rows are
covered. No unresolved records or forced assignments remain. Matching methods,
status semantics, and the limited `1818` blank fallback are documented beside
the restricted mapping.

### Unordered two-publication/two-ID mapping

The source publications `{US9470485B1, US9891030B1}` map jointly to anonymous IDs
`{BC001-C3791D5EE3E9, BC001-D3C36118E9E6}` at V1 ranks `{6, 7}`. Identical
content prevents individual assignment; no order is asserted. Both publications
have analyst label L, Include No, and report group `analyst-group-2`. Therefore
either bijection produces two excluded publications and one excluded report
group. The ambiguity has no effect on the reported EXP-013 metrics.

All 18 newly adjudicated publications belong to the top-20 set. The remaining
two are the previously known GOLD records: rank 15's source representative
US20180031345A1 explicitly lists GOLD member US10107579B2 in its family details
(FAN 78611350); rank 17 is GOLD US10591237B1 (FAN 87877222). These remain frozen
M+ positives, not newly assigned benchmark labels.

`US20160054081A1` in the analyst feedback and export is retained. The older
pending template's `US20160054081A` is an identifier discrepancy documented in
the partial snapshot, not silently used to change the frozen source files.

## Questel identifiers versus analyst report groups

The export labels its identifier column `Questel unique family ID (FAN)`, not
a separate FAMPAT-ID field. Those exact values remain separate from analyst
report-family grouping throughout the reconstruction and evaluation.

| Analyst report group | Publications | Questel FAN IDs |
|---|---|---|
| analyst-group-1 | CN110822986A / CN210718818U | 87709259 / 89160010 |
| analyst-group-2 | US9470485B1 / US9891030B1 | 74453517 / 78745238 |
| analyst-group-3 | CN107764127A / CN207662266U | 78965882 / 80722199 |

The analyst grouped these pairs for client-report purposes despite different
Questel IDs. No source rows or IDs are merged. The analyst's one-representative
instruction for the first pair remains recorded; this update does not select
that representative. Other reviewed publications retain singleton report
groups; this does not claim verified external family independence.

## Completed evaluation

| Metric | Result |
|---|---|
| Newly adjudicated publications | 18 |
| Include Yes / Include No | 7 / 11 |
| New-publication inclusion yield | 7/18 = 38.9% |
| Top-20 positives including two GOLD records | 9 |
| Publication-level Precision@20 | 9/20 = 45% |
| Analyst report groups among newly adjudicated publications | 15 |
| Includable / excluded newly adjudicated groups | 5 / 10 |
| New-candidate family inclusion yield | 5/15 = 33.3% |
| Analyst report groups across top 20 | 17 |
| Includable / excluded top-20 groups | 7 / 10 |
| Family-deduplicated report-inclusion yield@20 | 7/17 = 41.2% |
| Net-new relevant-family yield | N/A pending complete historical-report comparison |
| Analyst review minutes | N/A until supplied |

Counts are calculated from the completed records and checked against the
requested totals. Publication precision uses 20 original ranked records;
report-inclusion yield uses 17 analyst-defined report groups. These are distinct
denominators and must not be conflated with Questel-family precision. The five
included newly adjudicated groups are candidate groups, not proven net-new art.

## Preserved state and remaining limitations

GOLD-10, ADDITIONAL-JUDGED-5, hard negatives, F1–F8, all prior experiment outputs,
V1 ranking, and CURRENT_SYSTEM.yaml remain unchanged. RUN-005A (3,091) and RUN-012
(3,238) remain separate. The pending theft-triggered automatic-locking schema
note remains pending; no schema correction is inferred from this evaluation.

CURRENT_SYSTEM.yaml and the original pending template are preserved snapshots
as expressly requested; their PA-001 blocking/pending wording is superseded by
`benchmarks/BC001-smartgun/pending-validation/PA-001-status.yaml` for adjudication
status. No change to the current system or champion selection is implied.

Future blind-run workspaces must exclude the original export and reconstructed
mapping, along with all evaluator-only identities and labels. Follow the
restricted-evaluation README's allowlist-based workspace isolation instructions.
