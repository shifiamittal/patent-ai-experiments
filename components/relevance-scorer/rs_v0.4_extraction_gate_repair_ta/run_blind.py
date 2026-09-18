"""Run only inside a staged allowlisted directory, with no evaluator reads."""
import argparse
import csv
import hashlib
import io
import json
import os
import platform
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scorer import FEATURES, RELATIONS, WEIGHTS, FM, RM, DOMAIN, CAPS, PENALTIES, rank_records, validate

EXPECTED_HASH = "3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508"
ALLOWLIST = {"engine.py", "bc001_config.py", "input.json", "scorer.py", "run_blind.py", "scoring-spec.yaml", "frozen-disclosure.md", "extraction-schema.json"}


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(row):
    out = {"Record ID": row["record_id"], "title": row["title"], "abstract": row["abstract"],
           "domain_category": row["domain_category"], "domain_source": row["domain_evidence"]["source"],
           "domain_excerpt": row["domain_evidence"]["excerpt"]}
    for key, ev in {**row["features"], **row["relationships"]}.items():
        for field, value in ev.items():
            out[f"{key}_{field}"] = value
    for key in ("multi_primary_status", "tracking_only", "hard_cap", "penalty_points", "raw_score", "final_score", "predicted_relevance", "explicit_primary_relationships", "explicit_primary_features", "rank"):
        out[key] = row[key]
    for key in ("noise_flags", "gate_evidence", "penalty_evidence"):
        out[key] = json.dumps(row[key], ensure_ascii=False, sort_keys=True)
    for key, value in row["points"].items():
        out[f"{key}_points"] = value
    return out


def csv_bytes(rows):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    # Refuse a repo checkout or unexpected files. Standard-library modules are loaded above.
    present = {p.name for p in ROOT.iterdir()}
    if present != ALLOWLIST:
        raise RuntimeError(f"Workspace allowlist mismatch: {present ^ ALLOWLIST}")
    accessed = []
    def audit(event, arguments):
        if event == "open" and not isinstance(arguments[0], int):
            path = Path(arguments[0]).resolve()
            if not path.is_relative_to(ROOT):
                raise PermissionError("Blind runner denied filesystem access outside allowlist workspace")
            relative = path.relative_to(ROOT).as_posix()
            if relative not in ALLOWLIST and not relative.startswith("outputs/"):
                raise PermissionError("Blind runner denied non-allowlisted file")
            accessed.append(relative)
        if event.startswith(("socket.", "subprocess.", "os.system", "os.exec", "os.spawn")):
            raise PermissionError("Blind runner denied network/process creation")
    sys.addaudithook(audit)
    started = utc()
    before = {name: digest(ROOT / name) for name in sorted(ALLOWLIST)}
    if before["input.json"] != EXPECTED_HASH:
        raise RuntimeError("Input hash changed; STOP")
    spec = json.loads((ROOT / "scoring-spec.yaml").read_text(encoding="utf-8"))
    assert WEIGHTS == {k: v for k, v in spec["weights"].items() if k != "multi_primary"}
    assert {k: float(v) for k, v in FM.items()} == spec["feature_multipliers"]
    assert {k: float(v) for k, v in RM.items()} == spec["relationship_multipliers"]
    assert DOMAIN == spec["domain_points"] and CAPS == spec["hard_caps"] and PENALTIES == spec["penalties"]
    data = json.loads((ROOT / "input.json").read_text(encoding="utf-8"))
    assert data[0] == ["Record ID", "Title", "Abstract"]
    records = data[1:]
    assert len(records) == 3238 and len({r[0] for r in records}) == 3238
    assert all(len(r) == 3 and all(isinstance(value, str) for value in r) for r in records)
    rows = rank_records(records)
    checks = validate(records, rows)
    shuffled = list(records)
    random.Random(16016).shuffle(shuffled)
    checks["shuffled_input_identical_ranking"] = rows == rank_records(shuffled)
    assert all(checks.values())
    if args.dry_run:
        print(json.dumps({"checks": checks, "feature_counts": {f: {s: sum(row["features"][f]["status"] == s for row in rows) for s in ("E", "I", "A")} for f in FEATURES},
                          "F4_credits": [{"title": row["title"], "evidence": row["features"]["F4"]} for row in rows if row["features"]["F4"]["status"] != "A"],
                          "top_candidates": [{"title": row["title"], "abstract": row["abstract"], "features": row["features"], "relationships": row["relationships"], "score": row["final_score"]} for row in rows[:25]]}, ensure_ascii=True))
        return
    output = ROOT / "outputs"
    output.mkdir()
    flat = [flatten(row) for row in rows]
    files = {"full-ranking.csv": csv_bytes(flat),
             "structured-feature-extraction.csv": csv_bytes(sorted(flat, key=lambda r: r["Record ID"])),
             "top-100-evidence.csv": csv_bytes(flat[:100])}
    for name, content in files.items():
        (output / name).write_bytes(content)
    hashes = {name: digest(output / name) for name in files}
    validation = {"status": "PASS", "checks": checks, "record_count": len(rows), "input_sha256": EXPECTED_HASH,
                  "ranking_sha256": hashes["full-ranking.csv"], "output_hashes": hashes,
                  "allowlisted_input_hashes": before, "accessed_paths": sorted(set(accessed)),
                  "started_at": started, "frozen_at": utc(), "extraction_method": "deterministic content rules; no record-specific overrides",
                  "model_identifier": "N/A (no model inference during execution)", "implementation_author_model": "GPT-6 (system-provided family; exact deployment identifier N/A)",
                  "runtime": platform.python_version(), "platform": sys.platform, "temperature": "N/A", "determinism": "fixed rules, Decimal ROUND_HALF_UP, total lexical tie-break",
                  "batch_size": 3238, "token_usage": "N/A", "API_cost": "N/A", "retries": 0, "failed_batches": 0,
                  "feature_counts": {f: {s: sum(row["features"][f]["status"] == s for row in rows) for s in ("E", "I", "A")} for f in FEATURES}}
    (output / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "FROZEN", "rows": len(rows), "hashes": hashes, "frozen_at": validation["frozen_at"]}))


if __name__ == "__main__":
    main()
