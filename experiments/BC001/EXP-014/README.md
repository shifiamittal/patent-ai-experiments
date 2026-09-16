# EXP-014 setup: Orbit versus frozen AI ordering

Status: **AWAITING_ADJUDICATION**. No final decision has been calculated.

This setup starts from `233ec43ef129ca042a90aa9cea67d5fbaad2bbc9` in a clean
worktree matching origin/main. It performs no new search, scorer execution,
reranking, prompt change, benchmark modification, or promotion. The exact
experiment definition and pre-registered rule are in `definition.md`.

## Frozen source and reconciliation

Orbit ranks 1–20 are the first 20 data rows, without sorting, in the preserved
RUN-012 Questel export. They are 20 publication slots from the same 3,238-record
universe as EXP-013. The export's identifier header is `Questel unique family ID
(FAN)`; FAN values are preserved separately from analyst report-family groups.

`v0-top20-reconciliation.csv` records all 20 slots and explicitly checks source
family publication details against GOLD-10, ADDITIONAL-JUDGED-5, hard negatives,
the five EXP-011 analyst-validated publications documented in the canonical
reconciliation, completed EXP-013 decisions, reconstructed mapping, and existing
analyst report groups. Blank match fields mean no applicable identity match was
found in that source. AI predictions and titles are not used as analyst labels.

Two applicable judgments are reused:

| Orbit slot | Representative | Existing judgment | Basis |
|---|---|---|---|
| 4 | WO2021194584A2 | H / Include Yes; report group US11792283B2 | FAN 94738062's frozen family details explicitly list US11792283B2. GOLD-10 records H and historical report inclusion; EXP-011 independently documents analyst validation. This is reuse at the family level, not a new representative-specific full-text review. |
| 19 | CN207144670U | L / Include No; report group CN207144670U | Direct completed EXP-013 analyst decision; FAN 79213611. |

No additional applicable judgment was found among ADDITIONAL-JUDGED-5 or the
hard negatives. No other EXP-011 validated identity matches these slots. The
reconstructed mapping is evaluator-only identity evidence, not a relevance
judgment. Existing source references are recorded for every reused decision.

## Honest setup counts

- V0 publication slots: 20; resolved: 2; unresolved: 18.
- Already-known report groups: 2, comprising one includable and one excluded.
- Exact V0/V1 top-20 publication overlap: 1, CN207144670U; FAN overlap is also 1.
- Currently identifiable shared analyst report group: CN207144670U. Unknown
  report-family relationships must not be assumed distinct or equivalent.
- V0 final includable-group count, publication Precision@20, report-family
  inclusion yield, and review minutes remain N/A.
- Frozen V1 reference values are reused unchanged: seven includable groups,
  9/20 publication Precision@20, and 7/17 report-family inclusion yield.
- Existing recall guardrails pass on the frozen metrics: Recall@50 is 2/10
  versus 2/10; Recall@100 is 4/10 versus 2/10. This is not an EXP-014 decision.

The 18 unresolved slots are not assigned labels, inclusion decisions, or report
groups. Different FAN IDs do not prove different analyst report groups. Apparent
off-topic titles do not substitute for adjudication. The analyst packet therefore
contains exactly these 18 publications, with no repeated review of known cases.

## Analyst distribution and evaluator separation

Give the analyst **only** `analyst-packet.csv` and `analyst-instructions.md`,
copied into a neutral folder. Do not provide this README, definition, source
manifest, metrics, reconciliation, repository history, dashboard, or packet key.
The packet has neutral IDs and is randomly shuffled; IDs denote packet position,
not a search or AI rank. Its stored order differs at every position from source
order. No score, predicted label, rank, or ordering-system indicator is present.

The evaluator key is stored separately at
`benchmarks/BC001-smartgun/restricted-evaluation/EXP-014/analyst-packet-key.csv`.
The saved packet/key pair freezes the generated order; no seed or re-shuffling
is required to use it. Keep this key out of analyst and future blind-run
workspaces. The directory is a workflow boundary, not a filesystem ACL.

Google Patents access links are generated from the publication identifiers.
They are not a claim that full text or translations were fetched or verified.
The packet requests one total active-review time excluding document-access
delays. Frozen V1 review minutes remain unavailable; the new packet's time
must not be misrepresented as a matched V0/V1 timing comparison.

## Completion procedure, not executed

After receiving all remaining decisions, reconcile any newly recognized report
families against packet items and known report groups without altering FAN IDs
or merging source slots. Resolve conflicting group-level decisions explicitly.
Then calculate V0's includable unique report groups in its first 20 publication
slots and the two distinct secondary denominators: 20 publication slots and
the reconciled count of analyst report groups. Only after complete adjudication
and reconciliation may the pre-registered rule be evaluated.

`metrics.json` uses null for unavailable values (display as N/A), not zero.
The registry's Decision cell carries the workflow status AWAITING_ADJUDICATION;
it is not a PROMOTE/REJECT/HOLD result. No prior EXP-013 result or decision is
changed. Frozen ground truth, F1–F8, rankings, CURRENT_SYSTEM.yaml, and all
previous experiment artifacts remain intact.

No blocking identity/data issue was found for setup. Analyst responses and
family reconciliation remain necessary for final evaluation. Access to linked
documents has not been tested.
