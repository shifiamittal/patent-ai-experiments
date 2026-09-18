import copy
import unittest
from scorer import evidence, extract, score, rank_records, validate


def assess(title, abstract):
    return score(extract(title, abstract), title, abstract)


class ScorerTests(unittest.TestCase):
    def test_non_firearm_caps(self):
        for kind in ("welding", "spray", "nail", "toy", "charging"):
            row = assess(f"Smart {kind} gun", f"A {kind} gun uses a fingerprint sensor to authenticate its user and unlock operation.")
            self.assertEqual(row["hard_cap"], 5)
            self.assertLessEqual(row["final_score"], 5)

    def test_storage_cap(self):
        row = assess("Biometric firearm safe", "A fingerprint sensor authenticates the user to unlock a gun cabinet door.")
        self.assertEqual(row["hard_cap"], 15)
        self.assertEqual(row["features"]["F3"]["status"], "A")

    def test_holster_cap(self):
        row = assess("Fingerprint firearm holster", "A holster uses fingerprint recognition to release the retained gun.")
        self.assertEqual(row["hard_cap"], 20)
        self.assertEqual(row["features"]["F3"]["status"], "A")

    def test_storage_mentions_do_not_cap_firing_control(self):
        row = assess("Fingerprint gun case", "A fingerprint sensor verifies the authorized user, releasing the gun safety latch and allowing firing.")
        self.assertEqual(row["hard_cap"], 100)
        self.assertEqual(row["relationships"]["F2_to_F3"]["status"], "E")

    def test_no_F4_for_tracking(self):
        row = assess("GPS firearm tracking", "A GPS sensor tracks firearm location. A fingerprint sensor authenticates its user and enables firing when matched.")
        self.assertEqual(row["features"]["F4"]["status"], "A")
        self.assertEqual(row["points"]["F4_to_F3"], 0)

    def test_geofence_causal_control(self):
        row = assess("Geofenced firearm", "The firearm is disabled when its GPS location is within a prohibited zone.")
        self.assertEqual(row["features"]["F4"]["status"], "E")
        self.assertEqual(row["points"]["F4_to_F3"], 10)

    def test_long_sentence_tracking_is_not_geofencing(self):
        row = assess("Intelligent firearm", "The fingerprint identification module controls the trigger lock according to a comparison result, and the GPS unit transmits gun geographic position information to a mobile terminal in real time.")
        self.assertEqual(row["features"]["F4"]["status"], "A")
        self.assertEqual(row["points"]["F4_to_F3"], 0)
        row = assess("Intelligent firearm", "The controller controls opening and closing of the trigger lock according to a comparison result, the gun geographic position information transmitted by the GPS unit can be inquired on a terminal.")
        self.assertEqual(row["features"]["F4"]["status"], "A")

    def test_storage_withdrawal_discharge_is_not_firing(self):
        row = assess("Fingerprint gun storage closet", "Fingerprint identification controls retrieval/discharge of a gun from the storage closet and unlocks the container.")
        self.assertEqual(row["hard_cap"], 15)
        self.assertEqual(row["features"]["F3"]["status"], "A")

    def test_non_firearm_body_does_not_change_domain(self):
        row = assess("Charging gun", "The gun body includes fingerprint recognition and a controller to authenticate the user and enable charging operation.")
        self.assertEqual(row["hard_cap"], 5)
        self.assertEqual(row["features"]["F3"]["status"], "A")

    def test_battery_alert_is_not_central_integration(self):
        row = assess("Firearm sensor", "The firearm sensor includes an alert for low battery.")
        self.assertEqual(row["features"]["F6"]["status"], "A")

    def test_incidental_machine_example_cap(self):
        row = assess("Biometric machine", "Fingerprint recognition enables the machine. The machine may also be a firearm. Fingerprint authentication allows an authorized user to fire the firearm.")
        self.assertEqual(row["hard_cap"], 20)

    def test_automobile_ignition_translation(self):
        row = assess("Automobile fingerprint ignition", "A fingerprint device enables the automobile point firearm for ignition of the oil pump.")
        self.assertEqual(row["hard_cap"], 5)

    def test_explicit_relation_outscores_inferred(self):
        title = "Biometric firearm"
        text = "Fingerprint authentication enables firing only for the authorized user."
        fields = extract(title, text)
        explicit = score(fields, title, text)
        fields["relationships"]["F2_to_F3"].update(status="I", reasoning="A test of the inferred multiplier with an exact excerpt.")
        inferred = score(fields, title, text)
        self.assertEqual(explicit["points"]["F2_to_F3"], 14)
        self.assertEqual(inferred["points"]["F2_to_F3"], 3.5)
        self.assertGreater(explicit["final_score"], inferred["final_score"])

    def test_unsupported_inference_forced_absent(self):
        for excerpt, reason in (("", "An inference"), ("invented words", "An inference"), ("A firearm.", "")):
            fields = extract("Gun", "A firearm.")
            fields["features"]["F2"] = evidence(("abstract", excerpt), "I", reason)
            row = score(fields, "Gun", "A firearm.")
            self.assertEqual(row["features"]["F2"]["status"], "A")
            self.assertEqual(row["points"]["F2"], 0)

    def test_all_weights_and_bounds(self):
        fields = extract("Firearm", "All evidence.")
        fields["tracking_only"] = False
        for ev in [*fields["features"].values(), *fields["relationships"].values()]:
            ev.update(evidence(("abstract", "All evidence.")))
        row = score(fields, "Firearm", "All evidence.")
        self.assertEqual(row["raw_score"], 100)
        self.assertEqual(row["final_score"], 100)
        fields["noise_flags"] = ["generic_biometric_lock", "targeting_dominates", "generic_without_mechanism"]
        for ev in fields["features"].values():
            ev.update(evidence())
        row = score(fields, "Firearm", "All evidence.")
        self.assertEqual(row["final_score"], 0)

    def test_strictest_cap_and_additive_penalties(self):
        fields = extract("Firearm", "A firearm.")
        fields["noise_flags"] = ["storage_only", "holster_only", "non_firearm_gun", "targeting_dominates", "generic_without_mechanism"]
        row = score(fields, "Firearm", "A firearm.")
        self.assertEqual(row["hard_cap"], 5)
        self.assertEqual(row["penalty_points"], 18)

    def test_deterministic_ties_and_id_independence(self):
        records = [("b", "Firearm", "A firearm."), ("a", "Firearm", "A firearm.")]
        rows = rank_records(records)
        self.assertEqual([r["record_id"] for r in rows], ["a", "b"])
        self.assertEqual(rows, rank_records(records[::-1]))
        self.assertEqual(rows[0]["features"], rows[1]["features"])

    def test_exactly_once(self):
        records = [("a", "Gun", "A firearm."), ("b", "Device", "A device.")]
        self.assertTrue(all(validate(records, rank_records(records)).values()))
        with self.assertRaises(ValueError):
            rank_records(records + records[:1])
        with self.assertRaises(ValueError):
            validate(records, rank_records(records)[:1])
        unknown = rank_records(records)
        unknown[1]["record_id"] = "unknown"
        with self.assertRaises(ValueError):
            validate(records, unknown)


if __name__ == "__main__":
    unittest.main()
