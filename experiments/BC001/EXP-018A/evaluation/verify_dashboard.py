"""Read-only checks that the scoped Artifact Tool edit preserves prior content."""
import copy
import json
import os
from pathlib import Path
import openpyxl

EXP = Path(__file__).resolve().parents[1]
REPO = EXP.parents[2]
source = REPO / "Patent_AI_Experiment_Dashboard_Canonical.xlsx"
staged = REPO / "outputs/exp018a-dashboard/dashboard-updated.xlsx"
a = openpyxl.load_workbook(source)
b = openpyxl.load_workbook(staged)
assert a.sheetnames == b.sheetnames
count = 0
for s in a:
    t = b[s.title]
    assert s.freeze_panes == t.freeze_panes
    assert str(s.data_validations) == str(t.data_validations)
    assert {str(r) for r in s.merged_cells.ranges} <= {str(r) for r in t.merged_cells.ranges}
    assert list(s.tables) == list(t.tables)
    for name in s.tables:
        assert s.tables[name].ref == t.tables[name].ref
    for row in s:
        for c in row:
            if (s.title == "Dashboard" and c.coordinate in ("B6", "B7", "B8")) or (s.title == "Experiment Log" and c.row == 21) or (s.title == "Component Versions" and c.row == 10):
                continue
            d = t[c.coordinate]
            assert c.value == d.value, (s.title, c.coordinate, "value/formula")
            for attr in ("font", "fill", "alignment", "border", "protection"):
                assert copy.copy(getattr(c, attr)) == copy.copy(getattr(d, attr)), (s.title, c.coordinate, attr)
            assert c.number_format == d.number_format
            count += 1
    for name, dimension in s.column_dimensions.items():
        other = t.column_dimensions[name]
        assert dimension.width == other.width and dimension.hidden == other.hidden and dimension.outlineLevel == other.outlineLevel
    for index, dimension in s.row_dimensions.items():
        if (s.title == "Experiment Log" and index == 21) or (s.title == "Component Versions" and index == 10):
            continue
        other = t.row_dimensions[index]
        assert dimension.height == other.height and dimension.hidden == other.hidden and dimension.outlineLevel == other.outlineLevel
assert b["Experiment Log"]["A21"].value == "EXP-018A"
assert b["Experiment Log"]["N21"].value == "N/A"
assert b["Experiment Log"]["U21"].value == "PROMOTE"
assert b["Component Versions"]["F10"].value == "Yes"
cached = openpyxl.load_workbook(staged, data_only=True)
assert cached["Dashboard"]["E5"].value == 20
assert cached["Dashboard"]["E6"].value == 1
assert cached["Dashboard"]["E10"].value == 55
assert cached["Dashboard"]["E127"].value == .2
assert cached["Dashboard"]["E128"].value == .2
assert cached["Dashboard"]["E129"].value == .4
assert cached["Dashboard"]["E130"].value == .5
assert cached["Dashboard"]["E131"].value == 55
assert cached["Dashboard"]["E90"].value == -10
assert cached["Dashboard"]["E94"].value == 52
assert cached["Dashboard"]["D94"].value == 142.5
result = {"status": "PASS", "preexisting_cells_values_formulas_styles_verified": count,
          "sheet_names_tables_and_validations_preserved": True, "existing_row_column_dimensions_preserved": True,
          "experiment_row": 21, "component_champion_row": 10, "dashboard_result_range": "A123:H138",
          "new_metric_cached_values_verified": True, "rendered_views": ["Dashboard", "Experiment Log", "Component Versions"]}
(EXP / "evaluation/dashboard-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(result))
