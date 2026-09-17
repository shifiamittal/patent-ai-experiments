# rs_v0.3_feature_aware_ta

EXP-016A challenger: title/abstract-only deterministic feature extraction followed
by the user's approved arithmetic. This component is not the current system or
champion. Evidence judgments are AI-authored rule outputs, not analyst labels.

`scorer.py` takes only title and abstract in `extract()`. It emits structured
E/I/A features and E/I/C/A relationships with verbatim excerpts, source fields,
and inference explanations. The scorer sanitizes unsupported evidence before
applying decimal multipliers, additive penalties, strictest caps, and total
deterministic ordering. Record IDs enter only coverage checks and the final tie.

`scoring-spec.yaml` is JSON-compatible YAML and includes the approved scoring
text. `extraction-schema.json` specifies the extraction fields. No patent text,
identity lookup, model API, retrieval change, or prior ranking is used.

Run tests from this directory: `python -B -m unittest discover -s tests -v`.
For execution, stage only the six files listed in `run_blind.py` in a fresh
directory outside the checkout. Invoke `python -I -B run_blind.py` there.
The runner enforces its workspace allowlist and uses a Python audit hook to
deny file access outside the workspace, networking, and child processes.
This is a restricted application process, not an OS/container security boundary.
It refuses an existing output directory. `--dry-run` permits content-only QA.

## Extraction limitations and declared conventions

The extractor is a deterministic lexical/sentence-rule implementation. It is
not an LLM per-record semantic review. Conservative rules may miss paraphrases,
translation variants and cross-sentence relationships, and co-occurrence rules
may still misclassify evidence. Evidence presence and score validation cannot
prove semantic correctness. No record-specific score overrides are permitted.

Primary relationships for tie-breaking mean F2→F3 and F4→F3. F5→F6 includes a
secondary feature. Multi-primary awards two points for at least three established
features with two explicit when the four-point criterion is unmet. Decimal
half-up resolves the otherwise unspecified rounding half-tie convention.
Geographic control can establish F4→F3 independently of biometric/authentication
F3: the relationship definition names geographic control of operability.

Generic safety/monitoring is penalized only without a stated mechanism in the
record. Dominant targeting means the title identifies it or at least half of
the title/abstract sentence units discuss it. Missing-value `1818` is preserved
in output, excluded from evidence. These extraction/convention choices were
fixed before evaluation and are implementation interpretations, not new ground truth.
