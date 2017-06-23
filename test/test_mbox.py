import unittest
import pandas as pd
import tidyextractors as tx
import tidyextractors.tidymbox as tm


class TestMboxExtractor(unittest.TestCase):

    def setUp(self):
        self.gx = tm.MboxExtractor('./mbox_data/')
        self.sends_df = pd.read_csv('./mbox_data/mbox_sends_test.csv')
        self.emails_df = pd.read_csv('./mbox_data/mbox_emails_test.csv')
        self.raw_df = pd.read_csv('./mbox_data/mbox_raw_test.csv')

    def test_construction(self):
        self.assertEqual(isinstance(self.gx, tx.BaseExtractor), True)
        self.assertEqual(isinstance(self.gx, tm.MboxExtractor), True)

    def test_raw(self):
        check_df = self.gx.raw()
        expect_df = self.raw_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['date']),set(expect_df['date']))

    def test_emails(self):
        check_df = self.gx.emails()
        expect_df = self.emails_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['date']),set(expect_df['date']))

    def test_sends(self):
        check_df = self.gx.sends()
        expect_df = self.sends_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['hexsha']),set(expect_df['hexsha']))


if __name__ == '__main__':
    unittest.main()