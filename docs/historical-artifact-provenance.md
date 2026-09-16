# Historical artifact import provenance

Import date: 2026-09-16.

Canonical baseline: `7b0ad86f5c8b63301d680385a9a720bf78f0ca44`, tagged
`bc001-v0.1-provisional`. The authoritative reconciliation remains
`docs/canonical-current-state-2026-09-16.md`, unchanged.

## Scope and preservation

This import adds 48 existing artifacts: seven EXP-013 implementation/working
files, one ranked workbook, 20 saved Google Patents HTML pages, and 20 focused
body-text extracts. The accompanying manifest records each original absolute
local path, repository-relative destination, SHA-256, artifact type, associated
experiment/run, provenance confidence, and rationale. Every imported artifact
was copied byte-for-byte and checked against its source hash.

Original files in `bc001_work/`, `outputs/`, and `patent_sources/` remain
untouched and untracked. Of the 73 original files, 48 have imported copies and
25 are deliberately excluded: 18 whole-page text extracts, the workbook
inspection dump, three preview PNGs, and all three US20170180030A1 files.
Thus all 73 original files remain untracked; 25 have no imported counterpart.
These artifact counts exclude the existing `bc001_work/node_modules` dependency
link and its external target. That link and the dependency files are untouched
and are not part of this import.

No experiments were run. No existing canonical files, benchmark labels,
metrics, or adjudication entries were changed. No component or experiment is
promoted. EXP-013 remains INCONCLUSIVE pending PA-001, EXP-011 evidence-assisted
review remains PARTIALLY_VALIDATED, and no champion is designated.

## RUN-012 to EXP-013 source-chain gap

The canonical reconciliation describes RUN-012 as the 3,238-family FAMPAT
AND-variant export and EXP-013 as its blinded title/abstract reranking.
The recovered input contains 3,238 anonymous records. Input, screening, and
ranked JSON agree on record IDs and title/abstract contents. The workbook's
3,238 ranking rows and 100 evidence rows match the stored ranked JSON and
the builder's field transformations.

These internal relationships support association with EXP-013, but the
original `3238 (1).xlsx`, blinded-input workbook, private mapping/evaluation
key, and frozen prompt were not present in the three inventoried folders.
A record-by-record reconciliation to the original retrieval export therefore
remains unavailable. `input.json` is a prepared historical input, not the
original Orbit export, and it does not establish source order or family mapping.

Nothing in this import establishes equivalence to RUN-005A, the separate
3,091-result snapshot described as 10D. RUN-005A and RUN-012 remain distinct;
historical A/B counts must not be recomputed using the imported reranking data.

## Undocumented 1818 placeholder transformation

The recovered input contains the string `1818` in three title fields and 55
abstract fields. These counts match the canonical reconciliation's reported
three blank titles and 55 blank abstracts in the source export. This is
consistent with a missing-value transformation, but counts alone do not prove
the transformation, its author, or its implementation. No transformation log
or original export was available for verification. All values are preserved
unchanged; do not interpret `1818` as substantive patent evidence or silently
convert it to a blank.

## Recovered scoring implementation

`analyze.py` contains preliminary screening rules and candidate generation.
`rank.py` contains baseline scoring rules, record-specific feature annotations,
scores and explanations, and content-based sorting after a
`random.SystemRandom().shuffle` call. Exact-content ties can therefore retain
different relative order across executions. The stored `ranked.json` and
workbook preserve the historical ordering.

The script's annotations refer to positions in the content-sorted screening
array, making the preserved screening and candidate artifacts useful context.
Their wording or scores must not be attributed to an analyst merely because
they appear as fixed values in code. The canonical reconciliation states that
the scoring formula was not frozen at reconciliation time. This recovered code
adds implementation evidence; it does not retroactively establish an execution
log, model version, complete environment, or exact reproduction guarantee.
The original reconciliation is retained unchanged.

The imported scripts are archival implementation evidence, not analyst-approved
logic and not a production pipeline. They were read but not executed during
inventory or import. Original relative-path assumptions are retained: the new
archival layout does not preserve the scripts' original sibling-file layout,
and no executable packaging, path repair, or dependency lock was introduced.
AI scores, E/I/A feature judgments, reasons, and predicted relevance labels
are outputs, not benchmark ground truth.

## Patent capture provenance limitations

The 20 imported HTML files cover the publication identities in GOLD-10,
ADDITIONAL-JUDGED-5, and NEG-5. Embedded Google Patents canonical URLs and page
titles identify the publications. Association with EXP-011's public-patent
review is inferred from this coverage and the canonical narrative; a per-file
record proving experiment consumption was not found.

The inventory found each nonblank normalized body-extract line in its saved
HTML counterpart. This supports content lineage, not a complete extraction
procedure or proof that the exact extract was supplied to a model. Capture
dates, retrieval tools, extraction commands, translation history, and exact
model-consumption history remain unverified. Filesystem timestamps are not
treated as authoritative capture dates.

Saved HTML is retained as raw page evidence under the benchmark's source
directory. Prepared body extracts are stored separately under EXP-011.
Neither is an analyst relevance judgment or an original Orbit retrieval export.
The 18 excluded whole-page text extracts normalized to their corresponding
HTML text during inventory and add little beyond the retained pages and
focused extracts.

## Incorrect US20170180030A1 identifier history

The local US20170180030A1 HTML and extracts identify a wireless communication
device and signal-measuring method. This publication is absent from all three
canonical reference sets. The canonical EXP-011 account documents an identifier
correction to US20170160030A1, whose saved page concerns controlling firearm use.
The extra wireless publication is consistent with that historical misreading,
but its exact role is inferred rather than proven by an execution log.

All three US20170180030A1 files are excluded from this import and left untouched
locally. They are not aliases for US20170160030A1, additional benchmark records,
or newly judged negatives. The corrected publication's HTML and body extract
are imported under their own unchanged identifiers. No labels are changed.

## Remaining provenance work

Future reconciliation can compare the prepared input against the original
RUN-012 export and private mapping, recover the frozen prompt and environment,
and establish capture/extraction history if those records become available.
This import itself neither performs that work nor resolves PA-001.
