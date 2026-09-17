"""Independent CSV arithmetic, coverage, and repository preservation checks."""
import csv
import hashlib
import json
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

EXP = Path(__file__).resolve().parents[1]
REPO = EXP.parents[2]
BASE = "37123c707b095757844d632c5b5cfd1b3a61239e"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    spec = json.loads((EXP / "scoring-spec.yaml").read_text(encoding="utf-8"))
    validation = json.loads((EXP / "outputs/validation.json").read_text(encoding="utf-8"))
    data = json.loads((REPO / "experiments/BC001/EXP-013/working-artifacts/input.json").read_text(encoding="utf-8"))
    with (EXP / "outputs/full-ranking.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    source = {rid: (title, abstract) for rid, title, abstract in data[1:]}
    assert len(rows) == len(source) == 3238
    assert [int(r["rank"]) for r in rows] == list(range(1, 3239))
    assert sorted(r["Record ID"] for r in rows) == sorted(source)
    for row in rows:
        assert (row["title"], row["abstract"]) == source[row["Record ID"]]
        p = Decimal(spec["domain_points"][row["domain_category"]])
        assert p == Decimal(row["domain_points"])
        for key, weight in spec["weights"].items():
            if key == "multi_primary":
                established = sum(row[f"F{i}_status"] != "A" for i in range(2, 6))
                explicit = sum(row[f"F{i}_status"] == "E" for i in range(2, 6))
                value = Decimal(4 if established == 4 and explicit >= 3 else 2 if established >= 3 and explicit >= 2 else 0)
            else:
                state = row[key + "_status"]
                multiplier = spec["relationship_multipliers" if "_to_" in key else "feature_multipliers"][state]
                value = Decimal(weight) * Decimal(str(multiplier))
                if state in ("E", "I"):
                    assert row[key + "_excerpt"] and row[key + "_excerpt"] in row[row[key + "_source"]]
                if state == "I":
                    assert row[key + "_reasoning"].strip()
            assert value == Decimal(row[key + "_points"])
            p += value
        flags = json.loads(row["noise_flags"])
        penalty = sum(spec["penalties"].get(flag, 0) for flag in flags)
        cap = min([100] + [spec["hard_caps"][flag] for flag in flags if flag in spec["hard_caps"]])
        expected = min(Decimal(cap), max(Decimal(0), min(Decimal(100), (p - penalty).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))))
        assert p == Decimal(row["raw_score"]) and expected == Decimal(row["final_score"])
        assert penalty == int(row["penalty_points"]) and cap == int(row["hard_cap"])
        if row["tracking_only"] == "True":
            assert row["F4_status"] == "A" and Decimal(row["F4_to_F3_points"]) == 0
    def key(row):
        return (-Decimal(row["final_score"]), -int(row["explicit_primary_relationships"]), -int(row["explicit_primary_features"]), {"E": 0, "I": 1, "A": 2}[row["F3_status"]], int(row["penalty_points"]), row["Record ID"])
    assert rows == sorted(rows, key=key)
    for name, expected in validation["output_hashes"].items():
        assert sha((EXP / "outputs" / name).read_bytes()) == expected
    allowed = {"Patent_AI_Experiment_Dashboard_Canonical.xlsx", "experiment_registry.csv"}
    tracked = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE], cwd=REPO, text=True).splitlines()
    unchanged = 0
    for name in tracked:
        if name in allowed:
            continue
        old = subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=REPO)
        new = (REPO / name).read_bytes()
        # Existing working tree may have Git's CRLF conversion enabled.
        assert old == new or old.replace(b"\r\n", b"\n") == new.replace(b"\r\n", b"\n"), f"Changed protected artifact: {name}"
        unchanged += 1
    old_registry = subprocess.check_output(["git", "show", f"{BASE}:experiment_registry.csv"], cwd=REPO).replace(b"\r\n", b"\n")
    current_registry = (REPO / "experiment_registry.csv").read_bytes().replace(b"\r\n", b"\n")
    assert current_registry.startswith(old_registry)
    result = {"status": "PASS", "independent_rows_verified": len(rows), "independent_arithmetic": True,
              "evidence_and_inference_checks": True, "deterministic_tie_order": True, "frozen_hashes_unchanged": True,
              "protected_preexisting_files_unchanged": unchanged, "historical_registry_rows_preserved": True}
    (EXP / "evaluation/final-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
