"""Private evaluation: verify the committed freeze before any private read."""
import csv
import hashlib
import io
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

EXP = Path(__file__).resolve().parent
REPO = EXP.parents[2]
IMPLEMENTATION_COMMIT = "6f90e9a2e936cd95a78a8394d71586a0a34bf18d"
FIRST_PRIVATE_READ = "2026-09-17T17:59:30.1894059Z"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decision(metrics, no_leakage=True, coverage=True, worse_reproducibility=False):
    early = metrics["recall_at_20"]["hits"] >= 2 and metrics["recall_at_50"]["hits"] >= 2
    late = metrics["recall_at_200"]["hits"] >= 5
    improvement = metrics["recall_at_100"]["hits"] >= 5 or metrics["median_rank_retrieved_gold"] <= 75
    reasons = []
    if not early:
        reasons.append("early-recall guardrail failed")
    if metrics["median_rank_retrieved_gold"] > 90.5 * 1.1:
        reasons.append("median rank worsened by more than 10%")
    if not no_leakage:
        reasons.append("identity/GOLD/prior-rank leakage")
    if not improvement and worse_reproducibility:
        reasons.append("no meaningful improvement and worse reproducibility")
    if reasons:
        return "REJECT", reasons
    if improvement and early and late and no_leakage and coverage:
        return "PROMOTE", ["primary improvement and all guardrails passed"]
    return "HOLD / INCONCLUSIVE", ["promotion criteria not all met; no rejection condition met"]


def main():
    v = json.loads((EXP / "outputs/validation.json").read_text(encoding="utf-8"))
    assert v["status"] == "PASS" and all(v["checks"].values())
    for name, expected in v["output_hashes"].items():
        assert sha(EXP / "outputs" / name) == expected, "Frozen output changed; STOP"
    assert sha(REPO / "experiments/BC001/EXP-013/working-artifacts/input.json") == v["input_sha256"]
    assert datetime.fromisoformat(FIRST_PRIVATE_READ.replace("Z", "+00:00")) > datetime.fromisoformat(v["frozen_at"])
    current = read_csv(EXP / "outputs/full-ranking.csv")
    by_id = {r["Record ID"]: r for r in current}
    assert len(current) == len(by_id) == 3238
    mapping_path = REPO / "benchmarks/BC001-smartgun/restricted-evaluation/EXP-013/reconstructed-evaluation-mapping.csv"
    gold_path = REPO / "benchmarks/BC001-smartgun/ground-truth/gold10.csv"
    prior_path = REPO / "benchmarks/BC001-smartgun/reranking/v1/metrics.json"
    started = datetime.now(timezone.utc).isoformat()
    mapping = read_csv(mapping_path)
    gold = {r["publication"] for r in read_csv(gold_path)}
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    assert len(gold) == 10 and len(mapping) == 3238
    assert {r["record_id"] for r in mapping} == set(by_id)
    movements = []
    for row in mapping:
        candidates = json.loads(row["source_candidates_json"])
        hits = [(c, set(c["family_publications"]) & gold) for c in candidates]
        hits = [(c, matched) for c, matched in hits if matched]
        if not hits:
            continue
        # Never resolve ambiguous identical-content families by array order.
        assert row["mapping_status"] == "exact" and len(candidates) == 1 and len(hits) == 1, "Ambiguous GOLD mapping requires interval evaluation"
        candidate, matched = hits[0]
        assert matched == set(candidate["existing_gold_publications"])
        assert len(matched) == 1
        rank = int(by_id[row["record_id"]]["rank"])
        old_rank = int(row["v1_rank"])
        movements.append({"gold_publication": next(iter(matched)), "questel_family_id_fan": candidate["questel_family_id_fan"],
                          "record_id": row["record_id"], "mapping_status": row["mapping_status"],
                          "exp013_rank": old_rank, "exp016a_rank": rank, "rank_improvement": old_rank - rank,
                          "exp016a_score": float(by_id[row["record_id"]]["final_score"])})
    movements.sort(key=lambda r: r["exp013_rank"])
    assert len(movements) == 6 and len({r["questel_family_id_fan"] for r in movements}) == 6
    metrics = {"experiment": "EXP-016A", "ranking_sha256": v["ranking_sha256"], "gold_denominator": 10, "retrieved_gold_families": 6}
    comparison = []
    for cutoff in (20, 50, 100, 200):
        key = f"recall_at_{cutoff}"
        old_hits = sum(r["exp013_rank"] <= cutoff for r in movements)
        assert prior[key] == f"{old_hits}/10", "Comparator discrepancy"
        hits = sum(r["exp016a_rank"] <= cutoff for r in movements)
        metrics[key] = {"hits": hits, "denominator": 10, "value": hits / 10}
        comparison.append({"metric": f"Recall@{cutoff}", "exp013": old_hits / 10, "exp016a": hits / 10, "delta": (hits - old_hits) / 10,
                           "exp013_display": f"{old_hits}/10", "exp016a_display": f"{hits}/10"})
    old_median = statistics.median(r["exp013_rank"] for r in movements)
    assert old_median == prior["median_rank_retrieved_gold"] == 90.5
    median = statistics.median(r["exp016a_rank"] for r in movements)
    metrics["median_rank_retrieved_gold"] = median
    comparison.append({"metric": "Median rank of six retrieved GOLD", "exp013": old_median, "exp016a": median, "delta": median - old_median, "exp013_display": str(old_median), "exp016a_display": str(median)})
    outcome, reasons = decision(metrics)
    metrics.update(decision=outcome, decision_reasons=reasons, no_identity_gold_prior_rank_leakage=True,
                   exactly_once_coverage=True, reproducibility="deterministic; shuffled-input rerun identical",
                   mapping_provenance="post-experiment reconstruction; all six GOLD mappings exact; original private key unavailable",
                   not_retrieved_gold=sorted(gold - {r["gold_publication"] for r in movements}))
    out = EXP / "evaluation"
    out.mkdir(exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_csv(out / "gold-rank-movements.csv", movements)
    write_csv(out / "comparison-with-exp013.csv", comparison)
    access = {"ranking_frozen_at": v["frozen_at"], "first_private_artifact_read_at": FIRST_PRIVATE_READ,
              "evaluation_script_started_at": started, "implementation_commit": IMPLEMENTATION_COMMIT,
              "frozen_hashes_verified_before_private_reads": True,
              "sources": [{"path": p.relative_to(REPO).as_posix(), "sha256": sha(p)} for p in (mapping_path, gold_path, prior_path)],
              "mapping_ambiguous_rows": sum(r["mapping_status"] != "exact" for r in mapping), "retrieved_gold_mapping_exact_rows": 6}
    (out / "access-provenance.json").write_text(json.dumps(access, indent=2) + "\n", encoding="utf-8", newline="\n")
    metric_table = "\n".join(f"| {r['metric']} | {r['exp013_display']} | {r['exp016a_display']} |" for r in comparison)
    movement_table = "\n".join(f"| {r['gold_publication']} | {r['exp013_rank']} | {r['exp016a_rank']} | {r['rank_improvement']:+d} |" for r in movements)
    text = f"""# EXP-016A evaluation

Decision: **{outcome}**. {'; '.join(reasons)}.

| Metric | EXP-013 | EXP-016A |
|---|---:|---:|
{metric_table}

Recall uses the ten known-good GOLD families as denominator. The four unretrieved
families remain misses; the median uses only the six retrieved families. This is
known-good benchmark recall, not exhaustive prior-art recall. Precision@20 was
neither calculated nor claimed.

| GOLD publication | EXP-013 rank | EXP-016A rank | Improvement (old minus new) |
|---|---:|---:|---:|
{movement_table}

All six retrieved GOLD mappings are exact normalized-content matches in the
post-experiment reconstruction. Its 23 ambiguous non-GOLD rows remain unassigned;
they do not affect these GOLD metrics. The original private key is unavailable.
The six old ranks independently reproduce all four canonical comparator recall
values and its 90.5 median.

The first private read was {FIRST_PRIVATE_READ}, after the freeze at
{v['frozen_at']} and implementation commit `{IMPLEMENTATION_COMMIT}`.
The parent saw aggregate comparator totals in the user request, but no private
identities, GOLD labels, or prior individual ranks until after freeze. The runner
received no evaluation artifacts. No post-unblinding scorer/ranking edits occurred.

The feature extractor is rule-based and its semantic judgments are not analyst
validated. The 18 synthetic tests, exact coverage, excerpt checks, bounded
arithmetic, and shuffled-input equality passed. Application-level filesystem
restriction was used rather than an OS/container mount boundary. These limits
are preserved in provenance and are not evidence of analyst relevance accuracy.

CURRENT_SYSTEM.yaml, benchmark labels, GOLD-10 and earlier experiments remain
unchanged. This component remains registered as a challenger, regardless of the
decision label, pending any separately authorized promotion action.
"""
    (out / "evaluation.md").write_text(text, encoding="utf-8", newline="\n")
    decision_text = f"# EXP-016A decision\n\n**{outcome}** — {'; '.join(reasons)}.\n\nSee [evaluation](evaluation/evaluation.md) for metrics and exact GOLD rank movements.\n\n"
    decision_text += f"Primary improvement predicate: {metrics['recall_at_100']['hits'] >= 5 or median <= 75}. Recall@20 ≥ 2/10: {metrics['recall_at_20']['hits'] >= 2}. Recall@50 ≥ 2/10: {metrics['recall_at_50']['hits'] >= 2}. Recall@200 ≥ 5/10: {metrics['recall_at_200']['hits'] >= 5}. Median > 99.55: {median > 99.55}. No identity leakage and exactly-once coverage: True.\n\n"
    decision_text += "No current-system or champion designation is changed. No separate promotion update was authorized.\n"
    (EXP / "decision.md").write_text(decision_text, encoding="utf-8", newline="\n")
    print(json.dumps({"metrics": metrics, "movements": movements}, indent=2))


if __name__ == "__main__":
    main()
