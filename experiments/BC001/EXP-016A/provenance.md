# EXP-016A provenance

Canonical base: `37123c707b095757844d632c5b5cfd1b3a61239e` on main; origin/main
was fetched and matched before implementation. No earlier experiment, label,
retrieval artifact, current-system file, or unrelated untracked file was edited.

Authority: the user's two attached requests, with the second providing the
missing approved disclosure, F1–F8, scoring formula and decision rule. The
second is preserved verbatim in `authoritative-request.txt`. Its ranking-only
sections and disclosure were separately copied to the blind workspace.

Before execution the parent read repository README and provenance/governance
instructions and only selected governance/disclosure headings from the canonical
state document. Those documents contain aggregate historical facts. No private
mapping, GOLD key, analyst adjudication, prior individual ranks, or prior scoring
implementation was read. The user's aggregate comparator totals were also
visible but were excluded from runner inputs. No web browsing was used.

## Phase 1 implementation and execution

The scorer was authored in this task using content-only samples and anonymous
dry-run evidence. No record-specific patches or identifier-based extraction were
used. Pre-freeze QA found long-sentence GPS/locking co-occurrence, non-firearm
charging/scanning terminology, and storage withdrawal translated as discharge;
the general extraction rules and synthetic regression tests were corrected.
An initial geofence synthetic test failed and was fixed. One dry-run console
serialization failed on Windows cp1252; ASCII-escaped JSON diagnostics fixed it.
Neither was a completed/frozen ranking or an evaluation-informed retry.

Only the approved input, disclosure, scoring specification, extraction schema,
and two implementation files enter a fresh temporary directory. A Python audit
hook restricts subsequent opens to this directory and denies network and process
creation. Python standard-library modules and the scorer are loaded before the
hook; no evaluator modules are imported. This is application-level isolation,
not an OS filesystem mount/container barrier, and is disclosed as a governance
implementation limitation. Validation records the allowlist hashes/accessed paths.

Every credited excerpt is checked against its original title or abstract. The
full dataset is reranked after a deterministic input shuffle, and complete
output equality is required. These checks establish execution consistency, not
human/analyst validation of semantic extraction accuracy.

Execution timestamps, Python version, hashes, row counts, feature counts, and
available runtime details are recorded in `outputs/validation.json`. No model
API is called during extraction/scoring. Exact author-model deployment, authoring
token usage/cost, and temperature are unavailable and reported N/A.

## Declared interpretations / limitations

The supplied formula, weights, multipliers and caps are preserved. Extraction
uses AI-authored deterministic rules rather than per-record generative-model
judgments. The approved specification does not mandate a particular extraction
engine. Primary relationships mean F2→F3 and F4→F3; rounding is decimal half-up;
three-primary coverage is interpreted as at least three when the four-point
condition is unmet. See the component README for extraction conventions.

The repository's evaluator mapping is a post-experiment reconstruction, not the
missing original key. Its ambiguous candidate sets must be preserved during
evaluation. No original one-to-one private key is fabricated.

Phase 2 access and output hashes are recorded by the evaluator after the freeze.
