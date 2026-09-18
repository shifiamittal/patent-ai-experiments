# EXP-017A — Analyst run sheet

Status: **AWAITING_ORBIT_PREFLIGHT**. Manual analyst execution only; no queries have been run during setup.

## Before execution

1. Record analyst name, run date/time and practical export/evaluation capacity criterion with rationale before assessing counts. No numeric cutoff has been preregistered.
2. Select FAMPAT and Title, Abstract and Claims. Confirm no active date, jurisdiction or classification filters.
3. Keep these controls fixed: FAMPAT; Title, Abstract and Claims (/TI/AB/CLMS); existing current-vocabulary term groups. No date, jurisdiction or classification filters; no CPC/IPC expansion; no citation expansion; no Similarity Search; no full-text-field expansion; no seed-patent terminology intervention; no benchmark or GOLD changes.
4. Copy the exact queries below. Do not tighten or replace them.

### Q1P

```text
((FIREARM+ OR GUN+ OR WEAPON+ OR PISTOL+ OR HANDGUN+ OR RIFLE+ OR "SMART GUN") 5D (BIOMETRIC+ OR FINGERPRINT+ OR "FACIAL RECOGNITION" OR "PALM VEIN" OR "HEART RATE" OR KEYCARD+ OR SIGNATURE+ OR IDENTIT+ OR AUTHENTICAT+ OR "AUTHORIZED USER" OR "USER IDENTIFICATION" OR VERIF+))/TI/AB/CLMS
```

### Q2P

```text
((FIREARM+ OR GUN+ OR WEAPON+ OR PISTOL+ OR HANDGUN+ OR RIFLE+ OR "SMART GUN") 5D (LOCK+ OR UNLOCK+ OR DISABLE+ OR ENABLE+ OR "PREVENT DISCHARGE" OR FIRE+ OR DISCHARG+ OR OPERAT+ OR "RESTRICT USE" OR INTERLOCK+))/TI/AB/CLMS
```

## Capture each result

Record Orbit syntax acceptance, the exact executed statement, displayed FAMPAT-family count and evidence reference (for example, a screenshot location). Record any syntax modifications verbatim and why they were needed; enter "None" only after confirming none were made. Do not treat a syntax error as zero results. Stop if a substantive query change is needed.

| Field | Q1P | Q2P |
| --- | --- | --- |
| Historical baseline count | 23,935 | 493,993 |
| Analyst / run date-time | Pending | Pending |
| Syntax accepted | Pending | Pending |
| Exact executed query | Pending | Pending |
| Proximity query count (FAMPAT families) | Pending | Pending |
| Absolute reduction | Pending | Pending |
| Percentage reduction | Pending | Pending |
| Operational status / manageability rationale | Pending | Pending |
| Substantive query change required | Pending | Pending |
| Syntax modifications and reason | Pending | Pending |
| Evidence reference | Pending | Pending |
| Analyst notes | Pending | Pending |

Transfer observations to preflight-metrics.json. Calculate reductions only after valid counts are recorded using the definition's formulas. No exports, GOLD recovery, recall, precision or candidate-family metrics are part of this count-only preflight.

## Decision after observation

- PROCEED TO RETRIEVAL DESIGN if both counts are operationally manageable.
- PARTIAL if only one is manageable.
- HOLD / REDESIGN if either remains at an impractical scale requiring a substantive query change.

Record partial manageability separately from the overall action: if only one query is manageable and the other requires substantive change, record PARTIAL as the outcome and HOLD / REDESIGN as the action. No numeric cutoff was supplied; the analyst must document the export/evaluation capacity rationale. Do not infer manageability from percentage reduction alone.

Record outcome, overall action and rationale. Keep the registration awaiting preflight until observations are provided. Do not alter EXP-015, CURRENT_SYSTEM.yaml, benchmark labels, prior outputs or rankings.
