import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluate import decision


def metrics(r20=2, r50=2, r100=4, r200=5, median=90.5):
    return {"recall_at_20": {"hits": r20}, "recall_at_50": {"hits": r50}, "recall_at_100": {"hits": r100}, "recall_at_200": {"hits": r200}, "median_rank_retrieved_gold": median}


class DecisionTests(unittest.TestCase):
    def test_reject_early_even_with_improvement(self):
        self.assertEqual(decision(metrics(r20=1, r100=5, median=70))[0], "REJECT")

    def test_reject_median_more_than_ten_percent(self):
        self.assertEqual(decision(metrics(median=99.6))[0], "REJECT")
        self.assertEqual(decision(metrics(median=99.55))[0], "HOLD / INCONCLUSIVE")

    def test_promote_either_primary_condition(self):
        self.assertEqual(decision(metrics(r100=5))[0], "PROMOTE")
        self.assertEqual(decision(metrics(median=75))[0], "PROMOTE")

    def test_late_guardrail_blocks_promotion(self):
        self.assertEqual(decision(metrics(r100=5, r200=4))[0], "HOLD / INCONCLUSIVE")

    def test_leakage_and_coverage(self):
        self.assertEqual(decision(metrics(r100=5), no_leakage=False)[0], "REJECT")
        self.assertEqual(decision(metrics(r100=5), coverage=False)[0], "HOLD / INCONCLUSIVE")

    def test_reproducibility(self):
        self.assertEqual(decision(metrics(), worse_reproducibility=True)[0], "REJECT")


if __name__ == "__main__":
    unittest.main()
