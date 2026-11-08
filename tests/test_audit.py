import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import read_rows, aggregate, audit

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.sample = Path(__file__).resolve().parents[1] / "sample_data" / "demo_meta_ads.csv"
    def test_aggregation(self):
        summaries = aggregate(read_rows(self.sample), "campaign")
        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries[0]["landing_page_views"], 305.0)
    def test_flagging(self):
        with tempfile.TemporaryDirectory() as folder:
            count, flagged = audit(self.sample, Path(folder))
            self.assertEqual((count, flagged), (4, 1))
            self.assertTrue((Path(folder)/"summary.md").exists())
if __name__ == "__main__":
    unittest.main()
