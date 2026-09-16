# EXP-013 partial top-20 adjudication

Status: **HOLD / INCONCLUSIVE**. This records partial PA-001 analyst feedback,
not a new experiment or a promotion decision. No EXP-014 is created.

## Analyst evidence and scope

`partial-top20-adjudication.csv` preserves 14 analyst labels, Include Yes/No
decisions, reasons, and three stated family relationships, plus four records
pending because usable full text was unavailable. Reasons such as "same as"
remain verbatim and reference the named preceding publication. Analyst family
statements are recorded separately from the reasons and source family IDs.

The user-supplied request and read-only reconciliation sources are identified
by absolute path and SHA-256 in `partial-top20-source-manifest.csv`. The
adjudication receipt date is not inferred to be the analyst's review date.

The original pending template and V1 outputs remain unchanged. The template's
`US20160054081A` is recorded as an identifier discrepancy: the analyst's
`US20160054081A1` exactly matches the source export, and its title/abstract
uniquely matches V1 rank 14. No frozen benchmark label is changed.

## Identity reconciliation and outstanding private mapping

The Downloads copy of `BC001_Blind_Reranking_Input.xlsx` has the same complete
Blind Records matrix as the preserved `input.json`. In `3238 (1).xlsx`, the
source title and abstract contain leading parenthesized publication prefixes.
Removing that prefix and trimming surrounding whitespace supports exact
title/abstract comparisons to the preserved V1 ranked JSON. This comparison
does not use analyst labels to select a match.

All 18 submitted identities map to the top-20 set. Sixteen have unique content
matches. US9470485B1 and US9891030B1 both match the identical content at ranks
6 and 7 (BC001-C3791D5EE3E9 and BC001-D3C36118E9E6). Without the private family
mapping, their individual rank/anonymous-ID assignment cannot be established.
Both are L / Include No, so the supplied provisional totals are unaffected.
The reconciliation CSV retains both candidates instead of guessing an order.

The remaining two top-20 records are the existing GOLD records:

- Rank 15, BC001-7B265B30DE83: source representative US20180031345A1,
  Questel ID 78611350; source family details explicitly contain GOLD member
  US10107579B2 (M+).
- Rank 17, BC001-91D38DDF387D: US10591237B1 (M+), Questel ID 87877222.

These two existing GOLD positives are counted as instructed, not newly assigned
Include Yes decisions. Their ground-truth files are unchanged. The private key
was not found in the repository or the searched Downloads/ChatGPT document
locations. Exact private-mapping validation remains pending; commit and push
must wait until the requested identity validation can be completed.

## Analyst family groups versus Questel IDs

| Analyst-stated pair | Questel ID of first publication | Questel ID of second publication |
|---|---|---|
| CN110822986A / CN210718818U | 87709259 | 89160010 |
| US9470485B1 / US9891030B1 | 74453517 | 78745238 |
| CN107764127A / CN207662266U | 78965882 | 80722199 |

All three analyst-stated pairs have different Questel identifiers in the source
export. These are recorded discrepancies, not grounds to overwrite identifiers
or silently merge rows. Broader family relationships and Questel grouping may
differ; no external family-equivalence claim is inferred here. The analyst's
one-representative instruction for CN110822986A / CN210718818U is preserved;
no representative is selected by this update.

Only the analyst grouping is used for the provisional 11-group denominator.
The 20-record ranking remains intact. Record-level bounds are not deduplicated
family-level precision.

## Provisional results

| Measure | Result |
|---|---|
| Newly adjudicated publications | 14 |
| Include Yes / Include No | 6 / 8 |
| Inclusion yield among newly adjudicated publications | 6/14 = 42.9% |
| Analyst-identified family groups | 11 |
| Includable / excluded family groups | 4 / 7 |
| Provisional analyst-family inclusion yield | 4/11 = 36.4% |
| Top-20 adjudicated, including two existing GOLD records | 16/20 |
| Positive adjudicated publications, including GOLD | 8/16 |
| Final Precision@20 | N/A |
| Record-level Precision@20 lower bound | 8/20 = 40% |
| Record-level Precision@20 upper bound | 12/20 = 60% |
| Completed top-20 report-inclusion yield | N/A pending completion |
| Net-new relevant-family yield | N/A pending historical-report reconciliation |
| Analyst minutes | N/A pending completion |

The four pending publications are IN202511109936A, IN201931009978A,
IN202241014106A, and KZ6216U. The upper bound treats all four as potentially
positive; the lower bound adds none. Missing full text is not a negative label.

The four includable groups are **newly adjudicated includable candidate
families**, not established net-new relevant families. The complete historical
report and existing mappings must be reconciled before making a discovery claim.

## Schema issue and preservation

The analyst repeatedly treated theft/unauthorized-handling-triggered automatic
firearm locking as a primary feature. It may not be represented distinctly in
the provisional F1–F8 schema. This is a pending-validation issue only; F1–F8 is
not modified and prior AI feature judgments are not rewritten.

GOLD-10, ADDITIONAL-JUDGED-5, hard negatives, CURRENT_SYSTEM.yaml, original V1
ranking, historical outputs, and prior metrics are preserved. RUN-005A (3,091)
and RUN-012 (3,238) remain distinct. EXP-013 stays HOLD / INCONCLUSIVE and no
champion or component promotion is designated.
