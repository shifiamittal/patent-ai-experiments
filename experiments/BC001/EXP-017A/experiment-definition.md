# EXP-017A — Experiment definition

Status: **AWAITING_ORBIT_PREFLIGHT**  
Registration date: 2026-09-18  
Executor: analyst, manually in Orbit  
Stage: retrieval-volume preflight only

## Objective and hypothesis

Test whether unordered 5D between the firearm group and each feature group reduces the two failed EXP-015 result volumes to an operationally manageable scale for the planned export-and-evaluation workflow. Manageability and the size of the reduction are unknown until analyst execution.

## Baselines and provenance

| New query | EXP-015 baseline query | Concept | Recorded FAMPAT families |
| --- | --- | --- | ---: |
| Q1P | EXP015-015A-Q1 | Biometric/authentication | 23,935 |
| Q2P | EXP015-015A-Q2 | Locking/control | 493,993 |

Historical execution date: 2026-09-17. Source: [EXP-015 recorded preflight](../EXP-015/preflight/volume-preflight-results.csv). Both exports were blocked by excessive volume. EXP-015 remains HOLD — DESIGN REVISION REQUIRED AFTER VOLUME PREFLIGHT and is not altered by this registration. Historical baselines are not new same-session runs; record the proximity run date so database timing differences remain visible.

## Single primary change

Replace the cross-concept AND between the firearm group and feature group with unordered 5D. Preserve all OR terms, truncation, phrases and field scope. The exact statements are in [query-manifest.csv](query-manifest.csv) and the run sheet.

## Fixed controls

FAMPAT; Title, Abstract and Claims (/TI/AB/CLMS); existing current-vocabulary term groups. No date, jurisdiction or classification filters; no CPC/IPC expansion; no citation expansion; no Similarity Search; no full-text-field expansion; no seed-patent terminology intervention; no benchmark or GOLD changes.

Do not create tighter replacement queries. A substantive change to vocabulary, distance, ordering, fields, filters or structure is outside this preflight. Record any Orbit syntax modification and its reason; retain the registered statement and exact executed statement separately. Cosmetic/parser-only corrections must preserve the registered meaning. If substantive repair is necessary, stop that query and record HOLD / REDESIGN rather than silently substituting a new query.

## Measurements

For each query record the historical baseline count, observed proximity FAMPAT-family count, absolute reduction, percentage reduction, operational status, syntax modifications and analyst notes. Also record executor, run date, accepted syntax and evidence reference. Unobserved fields remain null, not zero.

Only after a valid count is supplied: absolute reduction = baseline count - proximity count; percentage reduction = 100 * absolute reduction / baseline count. Keep negative reductions if the count increases. These are volume comparisons only. Do not calculate GOLD recovery, recall, precision or candidate-family metrics, combine query counts into a deduplicated union, or perform retrieval/export evaluation at this stage.

## Preregistered decision rule

- PROCEED TO RETRIEVAL DESIGN if both counts are operationally manageable.
- PARTIAL if only one is manageable.
- HOLD / REDESIGN if either remains at an impractical scale requiring a substantive query change.

Record partial manageability separately from the overall action: if only one query is manageable and the other requires substantive change, record PARTIAL as the outcome and HOLD / REDESIGN as the action. No numeric cutoff was supplied; the analyst must document the export/evaluation capacity rationale. Do not infer manageability from percentage reduction alone.

No decision has been made. Missing counts or rejected syntax do not count as a successful preflight. A subsequent retrieval design requires its own specification; this registration does not promote a component or change the current system.
