import ast
import json
from pathlib import Path
import unittest
import engine
import bc001_config as config
from scorer import extract, score


def assess(text, title='Firearm safety system'):
    return score(extract(title, text), title, text)


class RepairTests(unittest.TestCase):
    def test_failed_biometric(self):
        for outcome in ('invalid fingerprint', 'failed biometric identification', 'unsuccessful fingerprint verification'):
            x = assess(f'The controller disables the trigger when an {outcome} is detected.')
            self.assertEqual(x['features']['F2']['status'], 'E')
            self.assertEqual(x['relationships']['F2_to_F3']['status'], 'E')

    def test_success(self):
        x = assess('Successful fingerprint authentication enables firing.')
        self.assertEqual(x['relationships']['F2_to_F3']['status'], 'E')

    def test_failed_identification_preserved(self):
        x = assess('A fingerprint reader identifies the user and a controller blocks the trigger if the user is not correctly identified.')
        self.assertEqual(x['relationships']['F2_to_F3']['status'], 'E')

    def test_invalid_noncredential(self):
        x = assess('An invalid battery signal disables the trigger. A fingerprint sensor records images.')
        self.assertEqual(x['features']['F2']['status'], 'A')
        self.assertEqual(x['features']['F3']['status'], 'A')

    def test_generic_auth_no_biometric(self):
        x = assess('Successful authorization enables firearm operation.')
        self.assertEqual(x['features']['F3']['status'], 'E')
        self.assertEqual(x['features']['F2']['status'], 'A')
        self.assertEqual(x['relationships']['F2_to_F3']['status'], 'A')

    def test_functional_architecture(self):
        for text in ('An enrollment station registers firearm users.', 'A central server manages firearm locks.', 'An authentication device verifies users.', 'A control component processes identity signals.'):
            self.assertNotIn('generic_without_mechanism', assess(text)['noise_flags'])

    def test_bare_architecture(self):
        for text in ('A server and a station are included.', 'A server stands near a station.'):
            self.assertIn('generic_without_mechanism', assess(text)['noise_flags'])

    def test_physical_storage(self):
        for container in ('safe', 'cabinet', 'gun case'):
            x = assess(f'Fingerprint authentication unlocks the {container} door.', f'Firearm {container}')
            self.assertIn('storage_only', x['noise_flags'])
            self.assertEqual(x['features']['F3']['status'], 'A')

    def test_adjective_safe(self):
        for phrase in ('safe use', 'safe handling', 'safe operation'):
            self.assertNotIn('storage_only', assess(f'A system for {phrase} of a firearm.')['noise_flags'])

    def test_holster_trigger_access(self):
        x = assess('Fingerprint authentication unlocks a holster handle allowing access to the gun trigger. The holster prevents accidental firing.', 'Firearm holster')
        self.assertIn('holster_only', x['noise_flags'])
        self.assertEqual(x['features']['F3']['status'], 'A')

    def test_dual_system(self):
        x = assess('The firearm is held in a holster. Fingerprint authentication disables the trigger mechanism when verification fails.')
        self.assertNotIn('holster_only', x['noise_flags'])
        self.assertEqual(x['features']['F3']['status'], 'E')

    def test_holster_passive_protection(self):
        x = assess('The holster is molded to fit the gun, ensuring engagement and preventing accidental firing. Fingerprint authentication releases the holster handle covering the trigger.', 'Firearm holster')
        self.assertIn('holster_only', x['noise_flags'])
        self.assertEqual(x['features']['F3']['status'], 'A')

    def test_extinguishing(self):
        x = assess('Fingerprint recognition unlocks the cabinet and enables fire extinguishing.', 'Gun cabinet')
        self.assertIn('storage_only', x['noise_flags'])
        self.assertEqual(x['features']['F3']['status'], 'A')

    def test_cross_sentence_explicit(self):
        text = 'The controller verifies the fingerprint. When this result is invalid, it disables the trigger.'
        x = assess(text)
        self.assertEqual(x['relationships']['F2_to_F3']['status'], 'E')
        self.assertEqual(x['relationships']['F2_to_F3']['excerpt'], text)

    def test_cross_sentence_inferred(self):
        text = 'The authentication device verifies a fingerprint. The same device controls the trigger lock.'
        x = assess(text)
        self.assertEqual(x['relationships']['F2_to_F3']['status'], 'I')
        self.assertEqual(x['relationships']['F2_to_F3']['excerpt'], text)
        self.assertTrue(x['relationships']['F2_to_F3']['reasoning'])

    def test_unsupported_absent(self):
        for text in ('A fingerprint reader identifies users. A mechanical lever blocks the trigger.', 'The fingerprint reader identifies users; a separate switch controls firing.', 'A server authenticates users. A trigger mechanism is included.'):
            x = assess(text)
            self.assertEqual(x['features']['F3']['status'], 'A')
            self.assertEqual(x['relationships']['F2_to_F3']['status'], 'A')

    def test_architecture_inference_without_biometrics(self):
        text = 'User profiles are registered to access authentication devices coupled to firearms. The system includes a firearm lock and a server managing firearm devices.'
        x = assess(text)
        self.assertEqual(x['features']['F3']['status'], 'I')
        self.assertEqual(x['features']['F2']['status'], 'A')

    def test_unchanged_policy_ast(self):
        root = Path(__file__).resolve().parents[2]
        old = ast.parse((root/'rs_v0.3_feature_aware_ta/scorer.py').read_text())
        new = ast.parse((root/'rs_v0.4_extraction_gate_repair_ta/scorer.py').read_text())
        names = {'score', 'sanitize', 'sort_key', 'rank_records', 'validate'}
        self.assertEqual({n.name: ast.dump(n) for n in old.body if isinstance(n, ast.FunctionDef) and n.name in names}, {n.name: ast.dump(n) for n in new.body if isinstance(n, ast.FunctionDef) and n.name in names})


if __name__ == '__main__':
    unittest.main()
