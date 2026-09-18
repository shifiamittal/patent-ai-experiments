# EXP-016A-D1: post-hoc scorer failure audit

EXP-016A remains **REJECT**. D1 documents the completed failure audit; it is not
a new ranking experiment or a new analyst relevance adjudication. The supplied
diagnoses were reconciled against the frozen rows, approved specification and
implementation. All reported ranks, states and scores remain the original values.

## GOLD score decomposition

| Publication | EXP-013 → EXP-016A rank | Raw | Penalty | Cap | Final | Primary diagnosis |
|---|---:|---:|---:|---:|---:|---|
| US10107579B2 | 15 → 1 | 69.0 | 0 | 100 | 69.0 | Correct feature/relationship recognition |
| US10591237B1 | 17 → 221 | 18.0 | 0 | 100 | 18.0 | Clear semantic extraction false negative |
| US20240384959A1 | 83 → 64 | 27.6 | 0 | 100 | 27.6 | Positive feature detection with a penalty-extraction miss |
| US20210080208A1 | 98 → 49 | 29.5 | 0 | 100 | 29.5 | Reasonable title/abstract scoring |
| US11792283B2 | 147 → 226 | 25.0 | 8 | 100 | 17.0 | Extraction/relationship miss plus false penalty |
| US20140259847A1 | 555 → 2967 | 2.0 | 8 | 15 | 0.0 | Insufficient title/abstract evidence compounded by a false storage gate and penalty |

The CSV retains every frozen scoring field and exact original evidence excerpts,
plus separately identified diagnostic explanations and title/abstract quotes.

1. **US10107579B2:** Correct F2/F3 and explicit F2→F3 recognition, with supported
   F5 collection of situational data. F6=4 and inferred F5→F6=1 may over-credit a
   broadcast unauthorized-use notification because no centralized recipient is
   named. This is a secondary-feature concern, not a new relevance label.
2. **US10591237B1:** Clear semantic extraction false negative. The abstract says
   an invalid fingerprint disables the firearm trigger, but F2/F3/F2→F3 are
   A/zero. Static inspection confirms AUTH has no match in this title/abstract:
   invalid fingerprint is not interpreted as a failed authorization result.
3. **US20240384959A1:** F2=E and F3=I coexist with a missed targeting penalty.
   The quoted friend/foe wording and AI firing do not match TARGET at all.
   The F3 excerpt itself concerns target identity. Better rank does not establish
   correct extraction or penalties throughout the record.
4. **US20210080208A1:** Reasonable title/abstract scoring with an evidence ceiling.
   F3=E and F5=I describe user-data matching, firing control and incident capture.
   The frozen title/abstract do not explicitly identify biometrics, so F2=A is
   not a claim about what may exist elsewhere in the patent.
5. **US11792283B2:** Tracking and central architecture were recognized, but
   authentication-dependent firearm control was not. The minus-8 generic penalty
   is unjustified given the named central server, secure management station,
   docking station, firearm lock/authentication device and enrollment station.
   These device terms are absent from the mechanism whitelist. Biometric detail
   is unavailable in this title/abstract; no explicit biometric relationship is
   newly asserted. Frozen arithmetic: 25 − 8 = 17.
6. **US20140259847A1:** Sparse evidence is compounded by an objectively false
   storage gate: STORAGE matches the adjective safe in safe use of a firearm.
   The domain becomes incidental/ambiguous (2 points), and minus 8 floors the
   result to zero. The 15-point storage cap is present but **non-binding**.
   The generic penalty contributes to suppression; unlike the false storage
   classification, its semantic invalidity is less certain because the abstract
   really gives little mechanism detail. No counterfactual ranking was computed.

## Overlapping root-cause counts

Denominator: the three deteriorated GOLD records, US10591237B1, US11792283B2
and US20140259847A1. These are overlapping diagnostic categories, not exclusive
bins or new analyst relevance labels.

| Root cause | Count | Records |
|---|---:|---|
| Extraction or gating error | 3/3 | All three |
| Penalty/cap contribution | 2/3 | US11792283B2; US20140259847A1 |
| Genuine title/abstract evidence limitation | 2/3 | US11792283B2; US20140259847A1 |
| Pure numerical-weight failure with otherwise correct extraction | Not established | No isolated weight-only causal finding |

Penalty/cap contribution here means an applied penalty and/or gate affected
scoring. It does not mean two binding hard caps: neither deteriorated record
with this flag has a binding cap. The CSV booleans reproduce 3, 2 and 2 after
filtering deteriorated=True. They encode the supplied post-hoc diagnosis,
supported by the quoted frozen evidence; they are not mechanically inferred
ground-truth labels.

## Frozen top-20 patterns and corpus counts

- **Storage/holster boundaries:** rank 4 (BC001-3F53B09CDA35) describes holster
  storage and access to a covered trigger, yet gets domain 10, F3=16, F2→F3=14
  and no cap. Rank 17 (BC001-A01F02870DCB) is a gun cabinet: fire extinguishing
  satisfies the firing-context regex, defeating storage gating. It receives
  the same full authentication/control dimensions, with no cap. Treating access
  protection as control of firearm operability is the diagnostic failure.
- **Long-sentence causal inflation:** rank 17's translated component list and
  rank 19's lock/control list satisfy sentence-level keyword co-occurrence.
  F2→F3 receives explicit credit without a clean authentication-result-to-firing
  causal statement in the selected excerpt. Rank 3's case terminology is
  ambiguous but also names a gun safety latch; it is flagged for interpretation,
  not asserted to be a definite storage-only false positive. Rank 7 has a more
  explicit fingerprint comparison/trigger-lock dependency despite its long text.
- **Over-broad F5 selection:** rank 4 cites enrollment fingerprints; rank 11
  cites fingerprint input collection; rank 5 cites a GPS merely coupled to a
  firearm. Ranks 8/9/10 reuse GPS/geofence evidence as F5. These selected excerpts
  do not consistently distinguish enrollment, transient input, location sensing
  and actual tracking/logging. The frozen disclosure includes biometric data
  collection, so enrollment credit is not automatically forbidden. Rank 11 also
  has stronger event-reporting text elsewhere, and rank 5 later states location
  determination. The established finding is unreliable semantic scope/evidence
  selection, not that every such F5 point is necessarily wrong.
- **Zero scores:** 2,269 / 3,238 records have final_score=0.
- **F4 sparsity:** 3 / 3,238 established F4 states (3 E, 0 I).
- **F2→F3 sparsity:** 24 / 3,238 credited relationships (22 E, 2 I). A further
  24 have C (co-occurrence) and receive zero; these must not be counted as credit.
- **Score plateau:** exactly eight records score 52 at ranks 12–19. Each has
  one explicit primary relationship, two explicit primary features, F3=E and
  zero penalty. Thus every substantive tie-breaker is equal: lexical Record ID
  actually determines all eight positions, not merely a hypothetical fallback.
- **Early content diversity:** ranks 8/9 have identical normalized title and
  abstract. Ranks 13/15 are near-identical (character similarity 0.844104 with
  NFKC/casefold/whitespace normalization; equivalent mechanism wording reviewed).
  Four slots cover two content pairs. This reduces textual diversity; it does
  not prove common family identity, authorize merging, or justify changing this
  fixed 3,238-record universe.

The score-52 IDs in frozen order are: BC001-1EB69221CE7A, BC001-3DD58E31397D, BC001-5946DA63E67B, BC001-6197DE78098F, BC001-7A2C56F84041, BC001-A01F02870DCB, BC001-C047EC90B27A, BC001-DA1021F1705A.
All 20 rows are described individually in `top20-score-pattern-audit.csv`.

## Conclusion and proposed next experiment

EXP-016A failed primarily because the deterministic pattern-based extractor
could not reliably interpret semantic feature relationships and domain
boundaries. The audit does not establish that numerical weights alone caused
the failure.

Do not tune the weights first. Do not apply the current deterministic extractor
to full text: longer text could increase accidental keyword co-occurrence and
false relationships. Arithmetic consistency and passing synthetic tests do not
establish semantic extraction validity.

The proposed next ranking experiment is **EXP-018**: replace deterministic
title/abstract extraction with structured semantic/LLM evidence extraction while
freezing EXP-016A's numerical scoring formula, weights, benchmark, 3,238-record
universe and exact title/abstract input. This task neither creates nor executes
EXP-018, adds a component version, changes weights, or promotes a component.
