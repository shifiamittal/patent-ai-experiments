EVIDENCE MULTIPLIERS

Feature evidence:
- Explicit: 1.00
- Inferred with quoted textual basis and reasoning: 0.35
- Absent/not established: 0

Relationship evidence:
- Explicit causal relationship: 1.00
- Reasonably inferred relationship with quoted basis: 0.25
- Mere co-occurrence: 0
- Absent/not established: 0

Every E or I must contain a supporting title/abstract excerpt.
An unsupported I must be converted to A.

SCORING WEIGHTS

Domain match:
Maximum 10

- 10: firearm itself is the controlled system
- 8: firearm-attached mechanism directly controls firing
- 2: firearm relationship is incidental or ambiguous
- 0: wrong domain

F2:
Maximum 12

F3:
Maximum 16

F4:
Maximum 14

F5:
Maximum 10

F2→F3 relationship:
Maximum 14

Definition:
The authentication result directly controls firearm locking, unlocking,
enablement, disablement or discharge prevention.

F4→F3 relationship:
Maximum 10

Definition:
A geographic location or boundary directly controls firearm operation,
firing, locking or disabling.

F5→F6 relationship:
Maximum 4

Definition:
Firearm usage/event/tracking data is transmitted to a centralized server,
management system, database or external reporting destination.

Multi-primary coverage:
Maximum 4

- 0: fewer than three established F2–F5 features
- 2: three established primary features, with at least two explicit
- 4: all four primary features, with at least three explicit

Weak inferences alone cannot qualify.

F6:
Maximum 4

F7:
Maximum 1

F8:
Maximum 1

Maximum score before penalties:
100

CALCULATION

For F2–F8:

feature_points =
maximum feature weight × applicable feature evidence multiplier

For relationships:

relationship_points =
maximum relationship weight × applicable relationship multiplier

raw_score =
    domain_points
  + F2_points
  + F3_points
  + F4_points
  + F5_points
  + F2_to_F3_points
  + F4_to_F3_points
  + F5_to_F6_points
  + multi_primary_points
  + F6_points
  + F7_points
  + F8_points

penalized_score =
raw_score - applicable noise penalties

final_score =
minimum(
  applicable hard cap,
  maximum(0, minimum(100, round(penalized_score, 1)))
)

If no cap applies, applicable hard cap is 100.

HARD GATES AND CAPS

1. Welding gun, spray gun, nail gun, toy gun or another non-firearm
   meaning:
   final score cap = 5

2. Safe, cabinet, case, rack or storage access only, without control of
   the firearm itself:
   final score cap = 15

3. Holster or casing authentication without control of firearm
   operability:
   final score cap = 20

4. Firearm appears only as an incidental example:
   final score cap = 20

If multiple caps apply, use the strictest cap.

PENALTIES

- Generic “safety,” “monitoring,” “smart” or “authentication” without a
  stated technical mechanism:
  minus 8

- Friend/foe targeting, AI aiming or automatic target-selection content
  dominates the disclosure:
  minus 10

- Generic biometric lock with only incidental firearm language:
  minus 20

- GPS or location tracking without location-dependent operational control:
  F4 must be A and F4→F3 must be zero

- Feature or relationship with no supporting title/abstract excerpt:
  force it to A/zero

Do not award F4 for location tracking alone.

TIE-BREAKERS

Sort by:

1. final score descending
2. number of explicit primary relationships descending
3. number of explicit F2–F5 features descending
4. F3 evidence strength: E before I before A
5. total penalty points ascending
6. Record ID lexical order only as a final deterministic tie-breaker

Record ID must never influence feature extraction or score.

PREDICTED RELEVANCE BANDS

For output comparability only:

- H: 75–100
- M+: 55–74.9
- M: 30–54.9
- L: 10–29.9
- N: 0–9.9

These are model predictions, not analyst ground truth.

BLIND RANKING OUTPUT

For every one of the 3,238 records preserve:

- Record ID
- title
- abstract
- domain category and supporting excerpt
- F2–F8 E/I/A
- supporting excerpt for every E/I
- inference reasoning for every I
- F2→F3 status and evidence
- F4→F3 status and evidence
- F5→F6 status and evidence
- multi-primary status
- noise flags
- hard cap
- penalty points
- points for every scoring dimension
- raw score
- final score
- predicted relevance
- final rank

Final score must be calculated through code from the structured fields.
The model must not directly override the formula.

VALIDATION BEFORE UNBLINDING

Verify:

- exactly 3,238 rows
- exactly 3,238 unique Record IDs
- every input Record ID exactly once
- no unknown Record ID
- sequential ranks 1–3,238
- all scores between 0 and 100
- every E/I has evidence
- every I has reasoning
- F4 is not awarded for tracking alone
- deterministic tie-breaking

Freeze and hash the completed ranking before reading any private
evaluation artifact.

