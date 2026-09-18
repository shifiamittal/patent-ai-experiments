# Correction-by-correction diagnostic comparison

Mechanism-general; validated on BC001 only. Examples are known non-GOLD, not analyst relevance negatives. Ranks/scores below are sequential marginal effects; final ranking may include additional corrections.

## outcomes

Classification: Reusable outcome detection; BC001 BIO/auth adapter.

False-positive/negative risks: Credential-adjacent validity can refer to another device; outcome-only over-credit is filtered by relationship rules.

Positive / negative regressions: test_failed_biometric, test_success, test_failed_identification_preserved / test_invalid_noncredential, test_generic_auth_no_biometric.

| Direction | Non-GOLD record | Title | Score before → after | Rank before → after |
|---|---|---|---:|---:|
| promoted | BC001-7B35C6C39C7E | Fingerprint safety stun gun | 10.0 → 26.0 | 514 → 82 |
| promoted | BC001-E04CB84E23D7 | Firearm with user information input means | 10.0 → 26.0 | 599 → 92 |

No directly demoted record exists for this correction in its marginal variant. Other records can fall through displacement; those are not direct correction examples.

The two illustrated outcome-only firing promotions are canceled by the relationship step (final score 10 each), exposing why the fixes must be combined. Two additional surviving non-GOLD outcome changes are BC001-C45844564B37 (cabinet, F2 detection, 12→15) and BC001-F30F8987C7B9 (pistol box, F2 detection, 10→22); neither receives F3 in the final ranking.
## relationships

Classification: Reusable controlled-action and causal/adjacent-sentence linking; BC001 firearm-lock architecture inference and F2/F3 mapping.

False-positive/negative risks: Ambiguous pronouns, component lists and multiple authenticators may still imply a dependency incorrectly; distant paraphrases can be missed.

Positive / negative regressions: test_cross_sentence_explicit, test_cross_sentence_inferred, test_architecture_inference_without_biometrics / test_unsupported_absent, test_holster_trigger_access.

| Direction | Non-GOLD record | Title | Score before → after | Rank before → after |
|---|---|---|---:|---:|
| promoted | BC001-F135B46A4984 | Biometric gun lock | 22.0 → 52.0 | 155 → 17 |
| promoted | BC001-16E1EB95170A | Electronic gun lock bracket and unlocking and locking method thereof | 22.0 → 41.5 | 122 → 28 |
| demoted | BC001-3F53B09CDA35 | Safety system with biometric locking applied in holders for size and controlled storage of firearms | 64.0 → 32.0 | 4 → 37 |
| demoted | BC001-EAD37A2B9B33 | Remote managing method and apparatus for firearm | 64.0 → 32.0 | 6 → 47 |
## mechanism

Classification: Reusable functional component detector; BC001 relevant-function vocabulary.

False-positive/negative risks: Nearby function words can describe another component; named functional devices may be underspecified. Existing mechanism whitelist behavior is preserved.

Positive / negative regressions: test_functional_architecture / test_bare_architecture.

| Direction | Non-GOLD record | Title | Score before → after | Rank before → after |
|---|---|---|---:|---:|
| promoted | BC001-8D96485A81C2 | Magazine based, firearm safety apparatus for modifying existing firearms employing a digital, close proximity communications system and a low power electro-permanent magnet interlock system | 21.5 → 29.5 | 140 → 51 |
| promoted | BC001-87916D7FFA87 | Identification control of firearm | 18.0 → 26.0 | 206 → 65 |

No directly demoted record exists for this correction in its marginal variant. Other records can fall through displacement; those are not direct correction examples.
## storage

Classification: Reusable word-sense masking and object/action checks; BC001 container, adjective and holster boundaries.

False-positive/negative risks: Translated casing/box senses and dual-purpose objects remain ambiguous. The observed table-corner pistol box is still not recognized as storage because box is outside the bounded container vocabulary; it receives no F3 credit.

Positive / negative regressions: test_physical_storage, test_adjective_safe, test_dual_system / test_extinguishing, test_holster_trigger_access, test_holster_passive_protection.

| Direction | Non-GOLD record | Title | Score before → after | Rank before → after |
|---|---|---|---:|---:|
| promoted | BC001-2ED97E01F6A5 | Bullet cabinet intelligent alarm system | 15.0 → 56.0 | 234 → 9 |
| promoted | BC001-F3A3A67D5AA3 | Gun safe | 15.0 → 56.0 | 248 → 10 |
| demoted | BC001-4D743CC32344 | Method and apparatus for gunnery training, especially for infrared gunnery | 20.0 → 2.0 | 160 → 768 |
| demoted | BC001-3F53B09CDA35 | Safety system with biometric locking applied in holders for size and controlled storage of firearms | 32.0 → 15.0 | 37 → 235 |
| unchanged_rank | BC001-20EA53D4CF92 | Disconnect -type electric automobile fills electric pile | 2.0 → 2.0 | 715 → 715 |
| unchanged_rank | BC001-22CE6D308812 | Biometric electro-mechanical locking system | 0.0 → 0.0 | 3231 → 3231 |
