"""Append EXP-016A without rewriting historical registry rows."""
import csv
import io
import json
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
REPO = EXP.parents[2]
metrics = json.loads((EXP / "evaluation/metrics.json").read_text(encoding="utf-8"))
registry = REPO / "experiment_registry.csv"
original = registry.read_bytes()
reader = csv.DictReader(io.StringIO(original.decode("utf-8-sig")))
rows = list(reader)
assert not any(r["Experiment ID"] == "EXP-016A" for r in rows)
row = dict.fromkeys(reader.fieldnames, "")
row.update({"Experiment ID": "EXP-016A", "Date": "2026-09-17", "Benchmark ID": "BC001", "Benchmark Version": "0.1-provisional",
            "Base System": "EXP-013 on RUN-012", "Challenger System": "rs_v0.3_feature_aware_ta",
            "Hypothesis / Objective": "Feature-aware title/abstract reranking of the fixed 3238-family universe",
            "Primary Component Changed": "Relevance Scorer", "From Version": "rs_v0.2_blind_ta_rerank", "To Version": "rs_v0.3_feature_aware_ta",
            "What Changed": "Deterministic feature/relationship extraction and approved scoring formula",
            "Recall@50": 0.2, "Recall@100": 0.3, "Precision@20": "N/A", "Gold in Top 10": "N/A",
            "Median Rank of Retrieved GOLD": 142.5, "Analyst Minutes": "N/A", "Model Cost USD": "N/A",
            "Guardrail / Side Effect": "Recall@20 1/10 fails 2/10 guardrail; Recall@200 3/10; median worsens >10%",
            "Learning": "Determinism did not improve retrieval ordering of known GOLD; rule extraction needs separate evaluation",
            "Decision": metrics["decision"], "Notes": "Frozen before private evaluation. Six GOLD mappings exact in reconstructed key. Challenger only; CURRENT_SYSTEM unchanged."})
buf = io.StringIO(newline="")
writer = csv.DictWriter(buf, fieldnames=reader.fieldnames, lineterminator="\n")
writer.writerow(row)
assert original.endswith(b"\n")
registry.write_bytes(original + buf.getvalue().encode("utf-8"))
component = REPO / "components/component_registry.csv"
assert not component.exists()
with component.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["component", "version", "role", "experiment", "decision", "current", "champion", "implementation"])
    writer.writeheader()
    writer.writerow({"component": "Relevance Scorer", "version": "rs_v0.3_feature_aware_ta", "role": "challenger", "experiment": "EXP-016A", "decision": metrics["decision"], "current": "false", "champion": "false", "implementation": "components/relevance-scorer/rs_v0.3_feature_aware_ta/"})
(EXP / "evaluation/dashboard-row.json").write_text(json.dumps({"headers": reader.fieldnames, "values": list(row.values())}, indent=2) + "\n", encoding="utf-8", newline="\n")
print("Appended experiment registry; created challenger-only component registry.")
