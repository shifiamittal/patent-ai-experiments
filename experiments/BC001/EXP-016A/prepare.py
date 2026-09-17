"""Prepare authorized specifications and a fresh blind execution workspace."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parent
COMP = REPO / "components/relevance-scorer/rs_v0.3_feature_aware_ta"
SOURCE = Path(r"C:\Users\shifi\.codex\attachments\489ef194-1bcb-4fb5-9fa6-00c7a5f8a874\pasted-text.txt")
EXPECTED = "3a2fd18a328cbd575d1cedd05017ce3bfef2c88c3afe15e145a861fa87dba508"


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    text = SOURCE.read_text(encoding="utf-8")
    # This file is provenance, never an input to the blind runner.
    (EXP / "authoritative-request.txt").write_text(text, encoding="utf-8")
    disclosure = text[text.index("FROZEN DISCLOSURE"):text.index("EVIDENCE MULTIPLIERS")]
    ranking = text[text.index("EVIDENCE MULTIPLIERS"):text.index("PRIVATE EVALUATION")]
    (EXP / "frozen-disclosure.md").write_text(disclosure, encoding="utf-8")
    (EXP / "blind-ranking-instructions.md").write_text(ranking, encoding="utf-8")
    spec = {
        "experiment": "EXP-016A", "status": "approved challenger hypothesis, not analyst truth",
        "authority": "user-supplied 2026-09-17 specification; authoritative-request.txt",
        "input_sha256": EXPECTED,
        "feature_multipliers": {"E": 1, "I": 0.35, "A": 0},
        "relationship_multipliers": {"E": 1, "I": 0.25, "C": 0, "A": 0},
        "domain_points": {"firearm": 10, "attached_firing_control": 8, "incidental_or_ambiguous": 2, "wrong_domain": 0},
        "weights": {"F2": 12, "F3": 16, "F4": 14, "F5": 10, "F2_to_F3": 14, "F4_to_F3": 10, "F5_to_F6": 4, "multi_primary": 4, "F6": 4, "F7": 1, "F8": 1},
        "hard_caps": {"non_firearm_gun": 5, "storage_only": 15, "holster_only": 20, "incidental_firearm": 20},
        "penalties": {"generic_without_mechanism": 8, "targeting_dominates": 10, "generic_biometric_lock": 20},
        "multi_primary": {"four_established_at_least_three_explicit": 4, "at_least_three_established_at_least_two_explicit_otherwise": 2, "otherwise": 0},
        "formula": "min(hard_cap, max(0, min(100, round(raw_score - penalty_points, 1))))",
        "rounding": "decimal ROUND_HALF_UP (unspecified half-tie convention made explicit before execution)",
        "tie_breakers": ["final_score desc", "explicit_primary_relationships desc", "explicit_primary_features desc", "F3 E before I before A", "penalty_points asc", "Record ID lexical asc"],
        "primary_relationships": ["F2_to_F3", "F4_to_F3"],
        "bands": {"H": [75, 100], "M+": [55, 74.9], "M": [30, 54.9], "L": [10, 29.9], "N": [0, 9.9]},
        "evidence": "All E/I require verbatim title/abstract excerpts; all I require reasoning; unsupported evidence becomes A.",
        "tracking_only": "force F4=A and F4_to_F3=0",
        "approved_scoring_text": ranking,
    }
    write_json(EXP / "scoring-spec.yaml", spec)
    write_json(COMP / "scoring-spec.yaml", spec)
    ev = {"type": "object", "additionalProperties": False,
          "required": ["status", "source", "excerpt", "reasoning"],
          "properties": {"status": {"enum": ["E", "I", "A"]}, "source": {"enum": ["title", "abstract", ""]}, "excerpt": {"type": "string"}, "reasoning": {"type": "string"}},
          "allOf": [{"if": {"properties": {"status": {"enum": ["E", "I"]}}}, "then": {"properties": {"excerpt": {"minLength": 1}, "source": {"enum": ["title", "abstract"]}}}},
                    {"if": {"properties": {"status": {"const": "I"}}}, "then": {"properties": {"reasoning": {"minLength": 1}}}}]}
    relation = json.loads(json.dumps(ev))
    relation["properties"]["status"]["enum"].append("C")
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "EXP-016A content-only extraction", "type": "object",
              "required": ["domain_category", "domain_evidence", "features", "relationships", "noise_flags", "gate_evidence", "penalty_evidence", "tracking_only"],
              "properties": {"domain_category": {"enum": list(spec["domain_points"])}, "domain_evidence": ev,
                             "features": {"type": "object", "additionalProperties": False, "required": [f"F{i}" for i in range(2, 9)], "properties": {f"F{i}": ev for i in range(2, 9)}},
                             "relationships": {"type": "object", "additionalProperties": False, "required": ["F2_to_F3", "F4_to_F3", "F5_to_F6"], "properties": {r: relation for r in ("F2_to_F3", "F4_to_F3", "F5_to_F6")}},
                             "noise_flags": {"type": "array", "uniqueItems": True, "items": {"enum": list(spec["hard_caps"]) + list(spec["penalties"])}},
                             "gate_evidence": {"type": "object", "additionalProperties": ev}, "penalty_evidence": {"type": "object", "additionalProperties": ev}, "tracking_only": {"type": "boolean"}}}
    write_json(COMP / "extraction-schema.json", schema)
    path = REPO / "experiments/BC001/EXP-013/working-artifacts/input.json"
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != EXPECTED:
        raise RuntimeError("Input hash changed; STOP")
    write_json(EXP / "input-manifest.json", {"path": path.relative_to(REPO).as_posix(), "sha256": EXPECTED, "rows": 3238, "unique_record_ids": 3238, "columns": ["Record ID", "Title", "Abstract"], "source_baseline_commit": "37123c707b095757844d632c5b5cfd1b3a61239e", "transformations": "none; preserve 1818 placeholders, do not treat as evidence"})
    stage = Path(tempfile.mkdtemp(prefix="exp016a-blind-"))
    (stage / "input.json").write_bytes(content)
    for name in ("scorer.py", "run_blind.py", "scoring-spec.yaml", "extraction-schema.json"):
        shutil.copyfile(COMP / name, stage / name)
    shutil.copyfile(EXP / "frozen-disclosure.md", stage / "frozen-disclosure.md")
    print(stage)


if __name__ == "__main__":
    main()
