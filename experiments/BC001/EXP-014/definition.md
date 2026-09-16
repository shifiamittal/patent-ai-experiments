# EXP-014 experiment definition

* Experiment ID: `EXP-014`
* Component evaluated: Relevance Scorer
* Experiment type: ranking evaluation; no model or system change
* Baseline: RUN-012 Orbit ordering of the 3,238-family export
* Challenger: `rs_v0.2_blind_ta_rerank`
* Retrieval universe: the same frozen 3,238 records
* Single primary change: ordering method
* Fixed:
  * BC001 disclosure
  * `bc001-v0.1-provisional`
  * RUN-012 retrieval universe
  * Query and database snapshot
  * analyst relevance standard
  * existing ground truth
  * V0 and V1 rankings
  * family reconciliation policy
* Primary metric: number of analyst-includable unique report-family groups found within the first 20 publication slots
* Secondary metrics:
  * publication Precision@20
  * family-deduplicated report-inclusion yield@20
  * overlap between V0 and V1 top 20
  * analyst review minutes
* Guardrails:
  * V1 Recall@50 must be at least V0 Recall@50
  * V1 Recall@100 must exceed V0 Recall@100
* Pre-registered decision rule:
  * PROMOTE if V1 contains at least two more includable unique report-family groups than V0 and passes both recall guardrails
  * REJECT if V1 contains fewer includable unique report-family groups than V0 or violates a recall guardrail
  * HOLD if V1 is equal to or only one includable family better than V0

Status: `AWAITING_ADJUDICATION`. No final decision is calculated in this setup.
The guardrail-violation REJECT condition applies regardless of family-count
difference; the HOLD comparison is considered only when both guardrails pass.

Hypothesis: V1 finds at least two more analyst-includable unique report-family
groups within the first 20 publication slots than V0 while passing both recall
guardrails. This is an evaluation of frozen orderings, not a new scorer or search.
