# Restricted post-experiment evaluation data

Evaluator-only scope. These files must never be supplied to a blind ranking
agent or copied into a future blind-run workspace:

- `RUN-012/source-export.xlsx`: byte-for-byte copy of the original Questel
  `3238 (1).xlsx` export, including publication identities, source order, and
  Questel family IDs.
- `EXP-013/reconstructed-evaluation-mapping.csv`: a new post-experiment
  reconstruction joining anonymous IDs to candidate source identities. This is
  **not** the unavailable original private evaluation key.
- `EXP-013/top20-evaluation.csv`, validation results, and source manifest.

The canonical reconciliation requires evaluation-key access restriction but
did not implement a restricted directory. This directory establishes a workflow
boundary; a Git directory name does not enforce a filesystem or GitHub ACL.
Limit repository access to authorized evaluators. Blind runners must receive a
separate, explicitly allowlisted workspace, never a full checkout of this repo.

## Future blind-run workspace rule

1. Copy only the approved disclosure/schema and blinded input needed for that
   run into an isolated workspace. Validate that the input omits publication
   identities, source ranks, family IDs, reference labels, and evaluation results.
2. Exclude this entire directory, both the export and reconstructed mapping,
   all private keys, analyst adjudications, GOLD/reference sets, patent-source
   caches, experiment results, and repository history from the runner's inputs.
3. Check the workspace file allowlist before providing access. Removing files
   from the working tree of a full clone is insufficient because Git history
   can retain them. Do not mount evaluator directories into the runner.
4. Keep evaluator-only reconciliation separate and perform it after outputs
   are frozen. Do not use the reconstruction to rerank or tune EXP-013.

## Mapping schema and interpretation

One row per anonymous Record ID retains its original V1 rank. The
`source_candidates_json` array retains each candidate's source row, source rank,
publication, Questel family ID, family publication details, and analyst
report-family group ID where available. Candidate associations inside each
object must remain intact.

`mapping_status` has these meanings:

- `exact`: one source row matches both normalized title and abstract. This
  means exact normalized content, not recovery of the original private key.
- `family-level`: multiple source candidates share one Questel family ID;
  individual source-row identity remains unresolved. No rows currently use it.
- `ambiguous-identical-content`: multiple source rows have identical normalized
  content and different Questel IDs. Every corresponding anonymous ID carries
  the same unordered candidate set. Array order is not an assignment.
- `unresolved`: no supported normalized match. No rows currently use it.

Normalization removes the leading parenthesized publication prefix from source
fields, applies Unicode NFKC, collapses whitespace, and masks publication tokens
following `From ` to the observed `[publication reference]` form. Only when a
direct match fails, a blind-field value exactly equal to `1818` is compared with
a source blank. This is a reconstruction matching rule, not proof of the original
blank-transformation implementation. No inputs or rankings are rewritten.

There are 3,215 exact rows and 23 rows in 11 identical-content groups: ten
two-record groups and one three-record group. All 3,238 source rows are covered,
and source/anonymous cardinalities agree within every content group. No fuzzy
matching or arbitrary one-to-one tie assignment is used.

The source header is **Questel unique family ID (FAN)**. It does not contain a
separate field explicitly named FAMPAT family ID. `questel_family_id_fan`
preserves the provided FAN value from this FAMPAT export; no second identifier
is invented. Analyst report-family IDs are separate grouping assertions used
for client-report evaluation, not replacements for Questel IDs.

See `experiments/BC001/EXP-013/top20-adjudication-provenance.md` for the completed
adjudication and the metric-invariant unordered ranks 6/7 pair.
