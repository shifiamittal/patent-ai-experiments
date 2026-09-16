# Patent Search Project: Canonical Current State

**As of:** 2026-09-16  
**Case:** BC001 — Traceable biometric smart firearm  
**Purpose:** Repository and dashboard source of truth  
**Scope:** Historical reconciliation only. No new patent search or prompt optimization was performed.

## Provenance rules

1. An analyst-confirmed fact is distinct from an AI-generated interpretation.
2. An executed Orbit result is distinct from a proposed query.
3. A result count belongs only to the exact database snapshot, fields, query semantics, and run date that produced it.
4. Family-level and publication-level identifiers must not be mixed without an explicit family mapping.
5. H, M+, M, L, and N are analyst screening labels, not legal conclusions on patentability.
6. Recall values below use the frozen GOLD-10 reference set. They do not establish exhaustive prior-art recall.
7. Precision@20 remains unavailable until the previously unjudged V1 top-20 families receive analyst labels.

---

# 1. Reconstructed experiment history

## Summary register

| Proposed ID | Order | Experiment / iteration | Primary status |
|---|---:|---|---|
| HIST-000 | 0 | Original analyst patentability search | BASELINE |
| EXP-001 | 1 | Claude disclosure decomposition and feature extraction | DIAGNOSTIC |
| EXP-002 | 2 | Claude clarification-question generation | REJECTED |
| EXP-003 | 3 | Analyst SOP and Orbit grammar capture | DIAGNOSTIC |
| EXP-004 | 4 | Claude concept blocks and 15-query ladder | REJECTED |
| EXP-005 | 5 | Claude terminology table and Query B formulation | REJECTED as a query-planner candidate |
| RUN-005A | 6 | Initial Query B Orbit/FAMPAT execution | SUPERSEDED as the live export; retained as historical diagnostic |
| RUN-006 | 7 | Human Query A Orbit/FAMPAT execution | BASELINE comparator |
| EXP-007 | 8 | Query A / Query B overlap and GOLD-10 recovery | DIAGNOSTIC |
| EXP-008 | 9 | Seed-patent-grounded terminology expansion | DIAGNOSTIC |
| EXP-009 | 10 | Web-grounded terminology expansion | DIAGNOSTIC |
| EXP-010 | 11 | Web-enriched five-query portfolio | REJECTED |
| EXP-011 | 12 | Codex full-text assessment of 20 analyst-selected patents | DIAGNOSTIC; evidence-assistance pattern partially validated |
| RUN-012 | 13 | Query B-like rerun, 3,238-family export, and V0 rank baseline | BASELINE |
| EXP-013 | 14 | Blind title/abstract reranking of all 3,238 families | INCONCLUSIVE pending top-20 adjudication |

## HIST-000 — Original analyst patentability search

- **Objective / hypothesis:** Conduct a professional patentability search for a traceable smart firearm with biometric unlocking and related controls.
- **Inputs:** Two client-supplied images and an inventor video discussion. The analyst stated that the video added no technical facts beyond the images. Drawing labels such as AI threat assessment, thermal/IR sensing, drone dock, haptic trigger feedback, and kinetic charging were outside the search scope.
- **Tooling:** Orbit Intelligence by Questel v2.0.0, plus PatSeer, PatSnap, Amplified, Ambercite, Google/Google Patents, Espacenet, semantic search, classifications, citations, and similar-patent searching.
- **Strategy:** Understand invention; decompose features; gather Google/technical vocabulary; create broad keyword queries; find seed patents; extract CPC/IPC and patent language; iterate queries; inspect claims, descriptions, citations, similar patents, inventors, and assignees; prepare report.
- **Run details:** Approximately 12–15 queries across several tools/databases. The analyst estimated 2,000–3,000 patents/families reviewed.
- **Effort:** Approximately five days: four days of iterative search/review and one day of report preparation.
- **Ground truth generated:** The analyst's ordered top ten, additional report patents visible in screenshots, and five rejected/out-of-scope patents.
- **Observable result:** Historical report screenshots and reference lists exist, but the complete final report and complete search history are not in this conversation.
- **Learning:** Query construction and patent review were the main bottlenecks. Final technical opinion required the most expert judgment.
- **Status rationale:** This is the human-process baseline, but it is not a single-query retrieval baseline.

## EXP-001 — Claude feature decomposition

- **Objective / hypothesis:** Test whether an LLM could turn the disclosure into search-ready elements, combinations, and ambiguities.
- **Inputs:** Original images, video-derived notes, scope exclusions, and the statement that the video added no new technical facts.
- **Prompt/model/tool:** Claude; exact model/version and complete prompt were not separately frozen. Response: `Pasted markdown(20260912-105854).md`.
- **Output:** E1–E16 feature elements, proposed combinations, ambiguities, emphasis, and essentiality.
- **Analyst feedback:** No searched concept was omitted. E13 was invented and had to be removed. E1/E2 and E11/E12 should be merged for search purposes. E14–E16 were benefits/background or drawing-only rather than standalone search concepts. The important E1+E2+E3+E4 combination was missing. Several priority and essentiality labels were corrected.
- **Observable result:** Strong factual decomposition after corrections, but no analyst time saving; the analyst considered this task easy.
- **Change from prior state:** First structured machine representation of the disclosure.
- **Learning:** An LLM can assist with decomposition, but needs scope controls and analyst-derived priority rules. Decomposition quality does not establish search quality.
- **Status:** DIAGNOSTIC. The corrected output informed the later F1–F8 benchmark specification, but that normalization was AI-authored and not separately signed off as a full specification.

## EXP-002 — Claude clarification questions

- **Objective / hypothesis:** Test whether the LLM could identify ambiguities that must be resolved before searching.
- **Inputs:** The same disclosure and decomposition context.
- **Prompt/model/tool:** Claude; exact model/version and full prompt not independently frozen. Response: `Pasted markdown(20260912-115539).md`.
- **Output:** Five inventor questions, including one labelled critical before searching.
- **Analyst feedback:** The analyst would ask none of them; none represented a real search-blocking ambiguity; all could be handled during searching; no question would reduce the five-day effort. Overall rating: mostly unnecessary.
- **Learning:** Generic ambiguity generation created avoidable inventor effort. Search-impact gating is required.
- **Status:** REJECTED.

## EXP-003 — Analyst SOP and Orbit grammar capture

- **Objective / hypothesis:** Document the expert workflow and the actual search language constraints needed by later AI components.
- **Inputs:** Analyst's walkthrough of the original case and generic Orbit examples.
- **Tool:** Structured interview in chat; no model-generated search run.
- **Output:** Broad-to-narrow workflow, individual-feature then combination search, seed-patent iteration, CPC/IPC use, citation/similar searching, field selection, proximity logic, stop criteria, expected result bands, and Orbit operator examples.
- **Analyst-confirmed operating bands:** Under 100 results was considered too few, 100–500 manageable, and over 1,000 too many for a normal individual query.
- **Learning:** Query planning is an iterative control process, not one static Boolean string. The analyst uses result volume and patent language to adjust proximity and vocabulary.
- **Status:** DIAGNOSTIC. This is a system-requirements artifact, not an implemented Search Controller.

## EXP-004 — Claude concept blocks and 15-query ladder

- **Objective / hypothesis:** Test whether Claude could translate the decomposition and SOP into an Orbit-ready staged portfolio.
- **Inputs:** Corrected case context, analyst's Orbit examples, and search requirements.
- **Prompt/model/tool:** Claude; exact model/version and full prompt not frozen. Response: `Pasted markdown(20260912-132933).md`.
- **Output:** CB1–CB9 concept blocks, six combination ideas, fifteen proposed queries, and a classification-discovery plan.
- **Execution:** Not run in Orbit.
- **Analyst feedback:** Most logic overused document-level AND, important synonyms were missing, 15D was too wide, some proposed syntax was unsupported, ADJ was invalid, an OR group could not be placed on each side of 15D as written, and “same claim” was not an operator.
- **Learning:** A syntactically plausible query is not necessarily valid in the analyst's actual Orbit workflow or useful for retrieval.
- **Status:** REJECTED.

## EXP-005 — Claude terminology table and Query B formulation

- **Objective / hypothesis:** Produce a narrower firearm + biometric authentication + operational-control query using proximity.
- **Inputs:** Disclosure, corrected scope, and the preceding query feedback.
- **Prompt/model/tool:** Claude; exact model/version and full prompt not frozen. Response: `Pasted markdown(20260912-141859).md`.
- **Proposed query:** Firearm terminology AND an authentication group within 10D of a control/locking group.
- **Analyst feedback:** Conceptual structure was usable, but the draft was weak; synonyms were incomplete; 10D should be 5D; some phrase/truncation syntax needed repair; predicted useful-open rate was only 1–5%; approximately ten minutes would be required to repair it, effectively rebuilding much of it.
- **Change from EXP-004:** Reduced the portfolio to one focused query and used proximity for authentication/control.
- **Learning:** The LLM's principal failure was not lack of generic words alone; it did not produce the analyst's breadth, morphology, and Orbit-specific expression of those words.
- **Status:** REJECTED as a promoted Query Planner. It nevertheless became the source of the first AI retrieval run.

## RUN-005A — Initial Query B execution

- **Objective / hypothesis:** Test the retrieval coverage of the Claude query despite the analyst's quality concerns.
- **Inputs:** EXP-005 query, with `"prevent+ discharge"` mechanically changed to `"prevent discharge"`.
- **Tool/database:** Orbit/FAMPAT.
- **Recorded execution metadata:** Title, abstract, and claims; 10D; no other filters; approximately two minutes.
- **Results:** 3,091 families at the time of the run.
- **Ground truth:** Analyst GOLD-10.
- **Observable result:** Recovered 5/10 GOLD patents.
- **Limitation:** No ordered export from this 3,091-result snapshot is preserved. The exact Orbit search-history statement is not available as a machine-readable artifact.
- **Status:** SUPERSEDED as the exportable baseline by RUN-012, but retained because it is the snapshot used in the A/B overlap calculations.

## RUN-006 — Human Query A execution

- **Objective / hypothesis:** Compare a human-built query with the AI query.
- **Inputs:** Analyst-generated terminology and combinations.
- **Tool/database:** Orbit/FAMPAT.
- **Query strategy:** Four document-level blocks: lock/firearm proximity, biometric/recognition proximity, geography/tracking, and data gathering/storage.
- **Results:** 799.
- **Ground truth:** GOLD-10.
- **Observable result:** Recovered 6/10 GOLD patents.
- **Artifacts:** Query screenshot and result count. No ordered 799-result export exists in the chat.
- **Metadata limitation:** The query text contains `/TI/AB/CLMS/TX`, while the UI screenshot also displays “Title - Abstract - Claims,” and the analyst separately described the field as full text. Field provenance therefore remains internally inconsistent.
- **Status:** BASELINE comparator, not the complete historical analyst workflow.

## EXP-007 — A/B overlap and recovery diagnostic

- **Objective / hypothesis:** Determine whether Query B added useful retrieval coverage beyond Query A.
- **Inputs:** RUN-005A's 3,091-result set, RUN-006's 799-result set, GOLD-10, and H/M+ subsets.
- **Tool:** Orbit set operations; analyst manually supplied counts and member identities for the small intersections.
- **Results:** A∩B = 142; A only = 657; B only = 2,949; A∪B = 3,748. A recovered 6/10 GOLD; B recovered 5/10; the union recovered 7/10. A and B each recovered 1/1 known H in the then-used subset. A recovered 5 M+ and B recovered 4 M+.
- **Learning:** Query B added one known-good family not found by A, but at the cost of a much larger review set. Neither query represented the full 12–15-query analyst search.
- **Status:** DIAGNOSTIC.
- **Important scope:** These figures apply only to the original 3,091-result B snapshot, not the later 3,238-result export.

## EXP-008 — Seed-patent-grounded terminology expansion

- **Objective / hypothesis:** Test whether terminology mined from relevant patents is more useful than one-shot generic generation.
- **Inputs:** US11792283B2, US10591237B1, US20210080208A1, and US10107579B2.
- **Prompt/model/tool:** Claude; exact model/version and complete prompt not frozen. Response: `Pasted markdown(20260913-161127).md`.
- **Output:** P1–P12 patent-grounded terms.
- **Execution:** No new Orbit retrieval run used this table.
- **Analyst feedback:** Most terms could be useful in an initial search. “Docking station” was noisy/irrelevant. The strongest proposed additions included trigger-lock assembly, predetermined usage boundary, biometric scanning device, unauthorized-use notification, and vein recognition. The analyst judged seed patents more productive than the web list.
- **Learning:** Patent language is a stronger source of search vocabulary than a generic LLM list, but retrieval impact remains unmeasured.
- **Status:** DIAGNOSTIC; best-supported current terminology method, not a validated terminology engine.

## EXP-009 — Web-grounded terminology expansion

- **Objective / hypothesis:** Test whether a broad web-first pass improves initial synonym breadth before seed-patent iteration.
- **Inputs:** Disclosure plus web sources collected by Claude.
- **Prompt/model/tool:** Claude with web research; exact model/version and complete prompt not frozen. Response: `Pasted markdown(20260913-162213).md`.
- **Output:** W1–W12 web-derived term groups.
- **Execution:** No direct Orbit retrieval run of the table.
- **Analyst feedback:** Web terms would partially broaden the initial search. Some were suitable only for narrow queries; electronic fire-control was irrelevant; telemetry/usage logging was secondary; heart-rate variability/physiological distress was noisy. Seed-patent terms were more useful overall.
- **Learning:** Web expansion is useful as a first vocabulary source but is insufficient by itself and requires expert filtering.
- **Status:** DIAGNOSTIC.

## EXP-010 — Web-enriched five-query portfolio

- **Objective / hypothesis:** Convert web-enriched terms into five Orbit-ready searches.
- **Inputs:** EXP-009 terminology and case scope.
- **Prompt/model/tool:** Claude; exact model/version and full prompt not frozen. Response: `Pasted markdown(20260913-164611).md`.
- **Execution:** Not run in Orbit.
- **Analyst feedback:** Q1 and Q2 required major rebuilding; Q3–Q5 required minor edits. Across all five, synonyms remained incomplete, some syntax was unsupported, and proximity distances were too large. The analyst said correction would take longer than building from scratch; estimated rebuild time was 5–10 minutes.
- **Learning:** More terms did not fix query-planning and syntax-control failures.
- **Status:** REJECTED.

## EXP-011 — Codex assessment of 20 analyst-selected patents

- **Objective / hypothesis:** Test whether AI could map features, rank relevance, and provide evidence that reduced full-text review effort.
- **Inputs:** Twenty patents already selected by the analyst from the historical search; the disclosure; F1–F8; public patent text. The AI did not retrieve these twenty patents.
- **Prompt/model/tool:** Codex plus public patent pages; exact model/version and full conversation prompt were not separately frozen. Primary response: `Pasted markdown(20260915-081449).md`, followed by corrected identifiers and revised assessments.
- **Output:** E/I/A feature mapping, H/M+/M/L/N predictions, ranking, cited passages, and short explanations.
- **Corrections:** Two screenshot identifiers were initially misread and later corrected to US20170160030A1 and US11326847B1.
- **Analyst validation sample:** US11792283B2, US10996012B2, US11326847B1, US20180149440A1, and US5202523A.
- **Observed validation:** Cited passages were accurate/relevant for all five. Four summaries were fully accurate and one partially accurate. Four of five exact relevance labels matched after the analyst's corrections; US20180149440 was M rather than Codex's M+. The analyst classified US10996012 as H rather than the earlier Codex M+.
- **Effort result:** Comparable analyst work normally took about 30 minutes for five patents; reviewing the AI assessments took about 10–15 minutes despite incomplete trust, a 50–67% observed time reduction on this five-patent sample.
- **Analyst requirement:** Use full description as well as claims. Every inferential feature needs the passage/paragraph and the reasoning for the inference.
- **Learning:** Evidence-first assistance is promising. The experiment does not establish raw-corpus retrieval or top-of-funnel ranking quality.
- **Status:** DIAGNOSTIC. The evidence-extraction pattern is partially validated; the relevance scorer is not yet validated at corpus scale.

## RUN-012 — 3,238-family rerun/export and V0 baseline

- **Objective / hypothesis:** Obtain a complete ordered retrieval set that can support rank-based metrics and blind reranking.
- **Input:** Query entered by the analyst and shown in the 2026-09-16 screenshot; FAMPAT; title, abstract, and claims; Orbit-provided order.
- **Results:** 3,238 families on 2026-09-16. Export: `3238 (1).xlsx`.
- **Data fields:** Representative publication, title, abstract, Questel unique family identifier, and family publication details. The export does not contain a FAMPAT family identifier.
- **Data quality:** 3,238 data rows. Three source titles and 55 abstracts were blank in the source export.
- **GOLD-10 recovery:** 6/10 over the full set.
- **Orbit/V0 ranks:** US11792283B2 family 4; US10591237B1 42; US10107579B2 family 142; US20210080208A1 842; US20240384959A1 901; US20140259847A1 1,007. Four GOLD families were absent.
- **V0 metrics:** Recall@20 1/10; Recall@50 2/10; Recall@100 2/10; Recall@200 3/10; Recall@500 3/10; Recall@1,000 5/10; full-set recovery 6/10.
- **Critical query-provenance distinction:** The screenshot for this rerun shows document-level `AND` between the authentication group and the control group. EXP-005 proposed `10D`, and RUN-005A was described as a 10D execution. The 3,238 export must therefore be versioned as a separate executed query variant unless an Orbit search-history record proves equivalence.
- **Status:** BASELINE for the current reranking benchmark. It supersedes the older live result count, but not the historical A/B experiment.

## EXP-013 — Blind 3,238-family reranking

- **Objective / hypothesis:** Test whether AI can improve review order over Orbit's order using only titles and abstracts.
- **Inputs:** All 3,238 families from RUN-012, shuffled and anonymized; frozen disclosure and F1–F8; no publication IDs, source rank, or GOLD labels.
- **Prompt/model/tool:** Fresh Codex session; exact model version not recorded. Exact prompt is preserved as `BC001_Fresh_Codex_Reranking_Prompt.md`.
- **Output:** `BC001_V1_Ranked_Output.xlsx`, with a complete 1–3,238 ranking and top-100 evidence sheet.
- **Scoring approach:** Content-based 0–100 relevance score; primary-feature combinations and textual evidence used for ranking/tie-breaking. The model did not provide a deterministic term-weight formula, so exact score reproduction is not guaranteed.
- **Results:** Recall@20 2/10; Recall@50 2/10; Recall@100 4/10; Recall@200 5/10; Recall@500 5/10; Recall@1,000 6/10; full-set recovery remained 6/10 because reranking cannot recover absent patents.
- **Rank movements for recovered GOLD:** 142→15, 42→17, 901→83, 842→98, 4→147, and 1,007→555. Median rank of the six recovered GOLD families improved from 492 to 90.5.
- **Known limitation:** Only two top-20 families are in GOLD-10; the other 18 are unjudged, not known false positives. True Precision@20 cannot be computed until those 18 are reviewed.
- **Calibration limitation:** The model's predicted H/M+/M/L/N labels did not reliably match analyst labels for the known GOLD records. Title/abstract evidence underrepresented some full-text features.
- **Status:** INCONCLUSIVE. Rank-recall improved, but practical precision and new discovery yield remain unvalidated.

---

# 2. Reconciled BC001 benchmark

## Benchmark item status

| Item | Status | Canonical interpretation / correction |
|---|---|---|
| F1–F8 feature specification | PARTIAL / APPROXIMATE; AI-INFERRED normalization | The underlying concepts and scope exclusions were reviewed through E1–E16, but the F1–F8 schema is a later AI normalization. It has been used consistently in BC001 but was not separately approved line-by-line by the analyst. |
| Primary / secondary / optional labels | PARTIAL / APPROXIMATE | Analyst corrections support the underlying priorities. Current normalization is F1 domain; F2–F5 primary; F6–F7 secondary; F8 optional. This exact F-number mapping was not separately signed off. |
| GOLD-10 patents | CONFIRMED | Analyst's ordered top ten from the historical report, later used in Orbit set operations and the private evaluation key. This is a known-good benchmark set, not an exhaustive universe of relevant prior art. |
| LOW-5 patents | INCORRECT | “LOW-5” must be retired. Correct set name: **ADDITIONAL-JUDGED-5** or **REPORT-ADDITIONAL-5**. US11326847B1 is H; US20180149440A1 is M; US20110056108A1, CN111457785A, and US12298094B2 were report-included but their exact analyst categories were not frozen. |
| NEG-5 patents | CONFIRMED for set membership; PARTIAL for formal per-item labels | The analyst identified the five as rejected/out-of-scope after final review. US5202523A was individually reconfirmed N. Treat the set as hard negatives; do not claim that every formal N label was separately re-adjudicated in the later five-patent exercise. |
| Human Query A exact query | PARTIAL / APPROXIMATE | Screenshot exists and can be transcribed, but no machine-readable Orbit search-history statement exists. Field presentation is internally inconsistent (`/TI/AB/CLMS/TX`, UI “Title - Abstract - Claims,” and analyst statement “full text”). |
| Human Query A: 799 results | CONFIRMED | FAMPAT screenshot shows 799. |
| Human Query A: 6/10 GOLD recovery | CONFIRMED | Analyst supplied the six identities. |
| AI Query B exact proposed query | CONFIRMED as Claude proposal | Preserved in `Pasted markdown(20260912-141859).md` with 10D. |
| AI Query B exact initial executed query | PARTIAL / APPROXIMATE | Analyst stated the 3,091 run used 10D, T/A/claims, and changed only `prevent+ discharge`; no original machine-readable search history or ordered export is preserved. |
| AI Query B: 3,091 results | CONFIRMED for the original snapshot | Historical count at the time of RUN-005A. It must not be substituted with 3,238 in the A/B calculations. |
| AI Query B: 5/10 GOLD recovery | CONFIRMED for the original 3,091 snapshot | Analyst supplied the five identities. |
| A+B union: 3,748 results | CONFIRMED for original snapshots only | 799 + 3,091 − 142 = 3,748. It is not the union with the 2026-09-16 export. |
| A+B union: 7/10 GOLD recovery | CONFIRMED for original snapshots only | Applies to RUN-006 plus RUN-005A. |
| Historical analyst effort: approximately five days | CONFIRMED | Analyst said four days search/review plus one day report. |
| Historical patents reviewed: approximately 2,000–3,000 | PARTIAL / APPROXIMATE | Analyst estimate, not an audited count. |
| Historical query count: approximately 12–15 | PARTIAL / APPROXIMATE | Analyst estimate, spanning keywords, semantic, classification, citation, similar-patent, and multiple databases. |

## Frozen reference sets

### GOLD-10

| Publication | Analyst label in current key |
|---|---|
| US11792283B2 | H |
| US10996012B2 | H |
| US10591237B1 | M+ |
| US20170248383A1 | M+ |
| US20210080208A1 | M+ |
| US20170160030A1 | M+ |
| US20140259847A1 | M+ |
| US10107579B2 | M+ |
| US6415542B1 | M+ |
| US20240384959A1 | M+ |

The GOLD-10 labels preserve the current benchmark key. Note that later full-text comments may support different within-set severity judgments for individual patents. Any relabeling must be a versioned benchmark change, not a silent edit.

### ADDITIONAL-JUDGED-5

| Publication | Canonical current status |
|---|---|
| US11326847B1 | H, analyst-confirmed |
| US20180149440A1 | M, analyst-confirmed |
| US20110056108A1 | Report-included; exact category not frozen |
| CN111457785A | Report-included; exact category not frozen |
| US12298094B2 | Report-included; exact category not frozen |

### NEG-5 / hard negatives

- US5202523A
- US20180313626A1
- US20120097718A1
- US6276581B1
- US9459072B2

---

# 3. Ground truth versus generated artifacts

## A. Analyst-confirmed ground truth

- Original search type was patentability.
- Both original images were client material.
- Video added no new technical facts beyond the images.
- Drawing-only concepts were outside search scope.
- Analyst corrections to the E1–E16 decomposition, including removal of E13 and priority/essentiality corrections.
- Clarification questions were unnecessary and non-blocking.
- Analyst SOP, Orbit operator examples, result-volume bands, and iterative search approach.
- Historical effort: approximately five days, 2,000–3,000 reviews, and 12–15 queries.
- GOLD-10 identities and historical report ordering.
- ADDITIONAL-JUDGED labels explicitly confirmed for US11326847B1 (H) and US20180149440A1 (M).
- NEG-5 membership as rejected/out-of-scope; US5202523A individually reconfirmed N.
- Query A result count and GOLD recovery.
- Initial Query B result count, fields/proximity description, and GOLD recovery.
- A/B set-operation counts and GOLD recovery.
- Terminology and query-quality feedback on Claude outputs.
- Five-patent review of Codex evidence and the observed 30-minute versus 10–15-minute effort comparison.

## B. Historical factual system outputs

- Orbit Query A screenshot showing 799 FAMPAT results.
- Orbit Query B initial count of 3,091, as reported by the analyst.
- Orbit set counts: intersection 142, A-only 657, B-only 2,949, union 3,748.
- Orbit Query B-like rerun screenshot and complete 3,238-row export dated 2026-09-16.
- Orbit order and family metadata in `3238 (1).xlsx`.
- V0 GOLD family ranks in that export.
- Complete blinded input, private mapping, and evaluation key derived from the 3,238 export.
- Complete V1 ranked workbook with all 3,238 anonymous IDs and sequential ranks.

## C. AI-generated artifacts

- Claude E1–E16 decomposition, combinations, ambiguities, and clarification questions.
- Claude concept blocks and 15-query ladder.
- Claude generic, seed-patent, and web terminology tables.
- Claude Query B and five-query web-enriched portfolio.
- F1–F8 normalized feature schema.
- Codex feature mappings, evidence passages, relevance labels, and ranking for the curated 20 patents.
- Blind-input construction and private evaluation workbook.
- Codex V1 title/abstract scores, predicted labels, reasons, and top-100 evidence.
- All calculated recall and rank-improvement metrics derived from frozen files.

## D. Pending validation

- Relevance labels for 18 previously unjudged V1 top-20 families.
- True Precision@20 and analyst-open-worthy yield for V1.
- Whether V1's newly elevated families add relevant art beyond the historical analyst report.
- Exact analyst categories for US20110056108A1, CN111457785A, and US12298094B2 if they are to become graded benchmark labels.
- Exact machine-readable Query A search history and reconciled field setting.
- Whether the 3,238 rerun's document-level AND query should be considered equivalent to the original 3,091 run described as 10D. Current policy: do not assume equivalence; version them separately.
- Exhaustiveness of GOLD-10. It is a known-good set, not a complete relevance set.
- Exact reproducibility of the V1 0–100 scoring function; the prompt is frozen, but the model/version and deterministic scoring formula are not.

---

# 4. Current best version of each component

No component is designated “champion.” The evidence does not yet support that term.

| Component | Proposed version | Source | Validation status | Known limitations |
|---|---|---|---|---|
| Feature Extractor | `fe_v0.2_bc001_corrected` | EXP-001 plus analyst corrections; normalized into F1–F8 | Partially validated | Analyst found no missing searched concept, but one hallucinated feature was removed; exact F1–F8 wording/labels were not separately signed off; no cross-case test. |
| Terminology Engine | `te_v0.3_seed_grounded_candidate` | EXP-008 | Analyst-preferred method, retrieval-unvalidated | Strong terms identified, but no controlled Orbit run measured incremental recall/precision; depends on access to relevant seeds. |
| Query Planner | `qp_v0.2_query_b_baseline` | EXP-005 / RUN-005A | Executed but analyst-rated weak | Incomplete synonyms, syntax repair, poor noise control, and query provenance mismatch between the 3,091 and 3,238 runs. Baseline only. |
| Retrieval | `retrieval_v0.1_fampat_20260916_and_variant` | RUN-012 | Fully executed and frozen | 3,238 families, 6/10 GOLD recovery; only one query; four GOLD absent; live database changes; Query B semantics differ from proposed 10D version. |
| Relevance Scorer | `rs_v0.2_blind_ta_rerank` | EXP-013 | Metrics computed; practical precision pending | Uses title/abstract only; model/version not frozen; score function not deterministic; top 18 non-GOLD records unjudged; label calibration weak. |
| Evidence Extractor | `ee_v0.1_fulltext_passage_assist` | EXP-011 | Partially validated on five patents | Citations were useful and reduced review time, but inference needs paragraph identifiers and explicit reasoning; only five-patent validation sample. |
| Search Controller | `sc_v0.0_analyst_sop_spec` | EXP-003 | Requirements captured; not implemented | No autonomous loop has selected seeds, expanded vocabulary, adjusted result volume, followed citations, or decided when to stop. |

### Current best validated system state

The strongest supported capability is **evidence-assisted analyst review**, not autonomous end-to-end search. The retrieval baseline is real and reproducible from its own screenshot/export, and the reranker has measurable recall improvements, but the reranker's practical precision is not yet known.

---

# 5. Pending analyst asks

## BLOCKING

### PA-001 — Adjudicate the 18 previously unjudged V1 top-20 families

- **Already sent:** Yes.
- **Needed for:** True Precision@20, top-20 analyst yield, and whether V1 discovered useful art beyond GOLD-10.
- **Requested fields:** H/M+/M/L/N, include in report Yes/No, and a short note only if uncertain.
- **Families:** CN107578493A, CN107421388A, CN110822986A, CN210718818U, CN206862203U, US9470485B1, US9891030B1, US20040099134A1, CN107764127A, CN207662266U, CN207144670U, IN202511109936A, IN201931009978A, US20160054081A1, TR2023006305U5, IN202241014106A, KZ6216U, and WO0186376A2.
- **Scope:** Blocking only for Precision@20 and promotion/rejection of the reranker. It does not block the already computed recall/rank metrics.

## USEFUL BUT NON-BLOCKING

### PA-002 — Freeze exact labels for three additional report patents

- US20110056108A1, CN111457785A, and US12298094B2.
- Needed only if the benchmark is expanded beyond GOLD-10 and hard negatives into graded relevance metrics.

### PA-003 — Obtain native Orbit search-history text for Query A

- Would resolve the current field ambiguity and eliminate screenshot transcription risk.
- Not needed to preserve Query A as a historical comparator.

### PA-004 — Obtain native Orbit search-history text for the original 3,091 Query B snapshot

- Would determine whether the first run actually used 10D and allow an exact comparison with the 3,238 AND-variant export.
- Not needed if the repository treats the two runs as distinct, which is the recommended policy.

## NO LONGER NEEDED

- Further analyst review of Claude's five clarification questions.
- Further review of the first E1–E16 draft as a whole.
- Re-review of the five Codex evidence-assessment patents already completed.
- Asking the analyst to prove that all final report patents came from Query A; the analyst already confirmed the historical search used multiple queries and tools.
- Asking the analyst to export all historical results; the current benchmark can proceed with the 3,238 frozen export.
- Asking the analyst to review all 3,238 records to compute recall against GOLD-10.

---

# 6. Recommended Git repository import

```text
patent-search/
├── README.md
├── benchmarks/
│   └── BC001-smartgun/
│       ├── benchmark.yaml
│       ├── disclosure/
│       │   ├── original-feature-slide.jpg
│       │   ├── original-concept-drawing.jpg
│       │   ├── video-notes-1.jpg
│       │   ├── video-notes-2.jpg
│       │   └── scope-notes.md
│       ├── features/
│       │   ├── e1-e16-claude-raw.md
│       │   ├── e1-e16-analyst-corrections.md
│       │   └── f1-f8-v0.1-provisional.yaml
│       ├── ground-truth/
│       │   ├── gold10.csv
│       │   ├── additional-judged.csv
│       │   ├── hard-negatives.csv
│       │   └── provenance.md
│       ├── retrieval/
│       │   ├── query-a/
│       │   │   ├── screenshot.jpg
│       │   │   └── metadata.yaml
│       │   ├── query-b-initial-3091/
│       │   │   ├── proposed-query.md
│       │   │   └── metadata.yaml
│       │   └── query-b-and-variant-20260916/
│       │       ├── executed-query-screenshot.jpg
│       │       ├── source-export.xlsx
│       │       └── metadata.yaml
│       ├── reranking/
│       │   ├── v0-orbit-order-metrics.json
│       │   └── v1/
│       │       ├── blind-input.xlsx
│       │       ├── prompt.md
│       │       ├── ranked-output.xlsx
│       │       ├── private-evaluation-key.xlsx
│       │       └── metrics.json
│       └── pending-validation/
│           └── v1-top20-adjudication.csv
├── components/
│   ├── feature-extractor/fe_v0.2_bc001_corrected/
│   ├── terminology/te_v0.1_generic_claude/
│   ├── terminology/te_v0.2_web/
│   ├── terminology/te_v0.3_seed_grounded_candidate/
│   ├── query-planner/qp_v0.1_ladder_rejected/
│   ├── query-planner/qp_v0.2_query_b_baseline/
│   ├── relevance-scorer/rs_v0.1_curated20_fulltext/
│   ├── relevance-scorer/rs_v0.2_blind_ta_rerank/
│   ├── evidence-extractor/ee_v0.1_fulltext_passage_assist/
│   └── search-controller/sc_v0.0_analyst_sop_spec/
├── experiments/
│   └── BC001/
│       ├── HIST-000/
│       ├── EXP-001/
│       ├── EXP-002/
│       ├── EXP-003/
│       ├── EXP-004/
│       ├── EXP-005/
│       ├── RUN-005A/
│       ├── RUN-006/
│       ├── EXP-007/
│       ├── EXP-008/
│       ├── EXP-009/
│       ├── EXP-010/
│       ├── EXP-011/
│       ├── RUN-012/
│       └── EXP-013/
├── decision-log/
│   ├── 0001-separate-ground-truth-from-ai-artifacts.md
│   ├── 0002-retire-low5-label.md
│   ├── 0003-separate-3091-and-3238-query-snapshots.md
│   ├── 0004-gold10-is-known-good-not-exhaustive.md
│   └── 0005-no-champion-before-top20-adjudication.md
└── docs/
    └── canonical-current-state-2026-09-16.md
```

## Exact existing artifact mapping

| Existing artifact | Repository destination |
|---|---|
| `WhatsApp Image 2026-09-12 at 3.44.42 PM.jpeg` | `benchmarks/BC001-smartgun/disclosure/original-feature-slide.jpg` |
| `WhatsApp Image 2026-09-12 at 3.46.31 PM.jpeg` | `benchmarks/BC001-smartgun/disclosure/original-concept-drawing.jpg` |
| `WhatsApp Image 2026-09-12 at 4.19.54 PM (1).jpeg` and `...4.19.54 PM.jpeg` | `benchmarks/BC001-smartgun/disclosure/video-notes-*.jpg` |
| `Pasted markdown(20260912-105854).md` | EXP-001 raw output and feature-extractor source |
| `Pasted markdown(20260912-115539).md` | EXP-002 raw output |
| `Pasted markdown(20260912-132933).md` | EXP-004 raw output and rejected query-planner version |
| `Pasted markdown(20260912-141859).md` | EXP-005 raw output and proposed Query B |
| `Pasted markdown(20260913-161127).md` | EXP-008 seed terminology artifact |
| `Pasted markdown(20260913-162213).md` | EXP-009 web terminology artifact |
| `Pasted markdown(20260913-164611).md` | EXP-010 web-enriched query artifact |
| `Pasted markdown(20260915-081449).md` | EXP-011 initial Codex 20-patent assessment; store later ID corrections and analyst validation beside it |
| `WhatsApp Image 2026-09-13 at 6.44.48 PM (1).jpeg` | RUN-006 Query A screenshot |
| `WhatsApp Image 2026-09-13 at 7.08.25 PM.jpeg` and `...7.08.36 PM.jpeg` | Historical report top-ten screenshots |
| `WhatsApp Image 2026-09-14 at 7.01.30 PM.jpeg` and `...7.01.38 PM.jpeg` | Historical report additional-reference screenshots |
| `WhatsApp Image 2026-09-16 at 12.12.01 AM.jpeg` | RUN-012 executed query screenshot |
| `3238 (1).xlsx` | RUN-012 source export |
| `BC001_Blind_Reranking_Input.xlsx` | EXP-013 blind input |
| `BC001_Fresh_Codex_Reranking_Prompt.md` | EXP-013 frozen prompt |
| `BC001_V1_Ranked_Output.xlsx` | EXP-013 output |
| `BC001_Private_Evaluation_Key.xlsx` | BC001 private benchmark key; access-restrict in the repo/workflow |

## Files that must be created from this chat before import

- `benchmark.yaml` with version, cutoff date, database, query variant, fields, and provenance.
- `scope-notes.md` recording video/no-new-facts and drawing exclusions.
- `e1-e16-analyst-corrections.md` from the analyst's element-by-element feedback.
- `gold10.csv`, `additional-judged.csv`, and `hard-negatives.csv` with publication/family alias handling.
- `metadata.yaml` for each executed run.
- Machine-readable V0 and V1 metrics JSON.
- Top-20 adjudication template with 18 pending rows and the two already-known GOLD rows prefilled.
- Decision log entries listed above.

---

# 7. Canonical CURRENT STATE

- **Current benchmark version:** `BC001-v0.1-provisional`. Disclosure, scope exclusions, GOLD-10, hard-negative membership, and the 2026-09-16 export are usable. F1–F8 is frozen as the current experimental schema but remains an AI-normalized, partially validated specification.
- **Current baseline:** `retrieval_v0.1_fampat_20260916_and_variant` in Orbit order, 3,238 families, title/abstract/claims retrieval, with title and abstract exported for reranking.
- **Current best validated system state:** A real single-query retrieval baseline plus a partially validated full-text evidence assistant. The V1 title/abstract reranker is a candidate, not a promoted system.
- **Metrics we can honestly claim today:**
  - RUN-012 full-set GOLD recovery: 6/10.
  - V0 Recall@20/50/100/200/500/1,000: 1/10, 2/10, 2/10, 3/10, 3/10, 5/10.
  - V1 Recall@20/50/100/200/500/1,000: 2/10, 2/10, 4/10, 5/10, 5/10, 6/10.
  - Median rank of the six retrievable GOLD families improved from 492 to 90.5.
  - On the five-patent evidence-validation sample, analyst review time decreased from about 30 minutes to 10–15 minutes; cited passages were accepted as accurate/relevant for all five.
  - Historical initial-snapshot comparison: A 799 / 6 GOLD, B 3,091 / 5 GOLD, union 3,748 / 7 GOLD.
- **Metrics we cannot claim:** True Precision@20; exhaustive recall; new-relevant-patent discovery rate; query-generation time savings; end-to-end analyst time savings; cross-domain generalization; calibrated H/M+/M/L/N accuracy at corpus scale; legal patentability accuracy.
- **Next experiment:** Complete the already-requested adjudication of the 18 unjudged V1 top-20 families, then compute true Precision@20, report-inclusion yield, and net-new relevant families. This requires no new search and no prompt change.
- **Single biggest unresolved assumption:** That the V1 records elevated above known GOLD patents are genuinely relevant under full-text analyst review rather than title/abstract false positives. Until that is resolved, the reranker cannot be promoted.
- **Critical provenance warning:** Do not represent the 3,238 export as a simple time-updated copy of the 3,091 10D run. The preserved screenshot shows different query semantics. Version them separately unless native Orbit history proves otherwise.

