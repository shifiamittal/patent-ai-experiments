import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from decision_rule import decide

class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.b = dict(r20=2,r50=2,r100=4,r200=5,median=90.5)
        self.c = dict(r20=1,r50=2,r100=3,r200=3,median=142.5)
    def test_promote(self): self.assertEqual(decide(dict(self.b,median=89),self.b,self.c),'PROMOTE')
    def test_match_hold(self): self.assertEqual(decide(self.b,self.b,self.c),'HOLD')
    def test_mixed_hold(self): self.assertEqual(decide(dict(self.b,r100=5,r200=4),self.b,self.c),'HOLD')
    def test_early_reject(self): self.assertEqual(decide(dict(self.b,r20=1,median=80),self.b,self.c),'REJECT')
    def test_median_reject(self): self.assertEqual(decide(dict(self.b,median=100.5),self.b,self.c),'REJECT')
    def test_defect_reject(self): self.assertEqual(decide(dict(self.b,median=80),self.b,self.c,False),'REJECT')

if __name__ == '__main__': unittest.main()
