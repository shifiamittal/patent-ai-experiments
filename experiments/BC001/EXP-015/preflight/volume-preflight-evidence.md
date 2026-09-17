# Volume preflight evidence

## Provenance

Source: the analyst execution report in the user's first EXP-015 instruction, supplied to Codex on 2026-09-17. Codex did not execute these searches. Screenshots are reported to exist outside the repository but were not explicitly provided; no screenshot paths, hashes or independent visual verification are claimed.

## Analyst-reported observations

Both queries ran on 2026-09-17 in Orbit/FAMPAT, Title, Abstract and Claims only, with no other filters.

### EXP015-015A-Q1

Feature path: F1 + F2, firearm plus authentication.

Normalized approved syntax, preserved exactly as supplied:

```text
((FIREARM+ OR GUN+ OR WEAPON+ OR PISTOL+ OR HANDGUN+
  OR RIFLE+ OR "SMART GUN")
 AND
 (BIOMETRIC+ OR FINGERPRINT+ OR "FACIAL RECOGNITION"
  OR "PALM VEIN" OR "HEART RATE" OR KEYCARD+
  OR SIGNATURE+ OR IDENTIT+ OR AUTHENTICAT+
  OR "AUTHORIZED USER" OR "USER IDENTIFICATION" OR VERIF+))
/TI/AB/CLMS
```

Observed: **23,935 FAMPAT families**. Export not performed because of excessive volume. Orbit reformatted field restrictions at block level in search history; native history text was not supplied.

### EXP015-015A-Q2

Feature path: F1 + F3, firearm plus operational control.

Normalized approved syntax, preserved exactly as supplied:

```text
((FIREARM+ OR GUN+ OR WEAPON+ OR PISTOL+ OR HANDGUN+
  OR RIFLE+ OR "SMART GUN")
 AND
 (LOCK+ OR UNLOCK+ OR DISABLE+ OR ENABLE+
  OR "PREVENT DISCHARGE" OR FIRE+ OR DISCHARG+
  OR OPERAT+ OR "RESTRICT USE" OR INTERLOCK+))
/TI/AB/CLMS
```

Observed: **493,993 FAMPAT families**. Export not performed; Orbit cannot practically export this result set according to the analyst report.

## Interpretation and limits

The reported screenshots indicate the intended title/abstract/claims restrictions were applied. Treat this as a query-design volume failure, not a confirmed Orbit syntax failure.

Independent feature retrieval using broad document-level AND logic can create operationally unusable result sets. Broad stems such as GUN+, WEAPON+, LOCK+, ENABLE+, FIRE+ and OPERAT+ produce large amounts of noise. This is the supplied design interpretation; no exported sample was evaluated and no per-term contribution or precision was measured.

“Search important features independently” requires a Search Controller with predeclared result-volume checks, proximity or functional relationships, and controlled handling of high-collision terms. No such revised controller or queries are implemented here.

The evidence rejects the current operational form of EXP015-015A-Q1 and Q2, not feature-specific retrieval as a principle. No union, overlap, GOLD recovery, incremental yield or marginal GOLD rate can be inferred from these counts.
