import unittest
import pandas as pd
import tidyextractors as tx
import tidyextractors.tidygit as tg


class TestGitExtractor(unittest.TestCase):

    def setUp(self):
        self.gx = tg.GitExtractor('./git_data/')
        self.changes_df = pd.DataFrame.from_csv('./git_data/git_changes_test.csv')
        self.commits_df = pd.DataFrame.from_csv('./git_data/git_commits_test.csv')
        self.raw_df = pd.DataFrame.from_csv('./git_data/git_commits_test.csv')

    def test_construction(self):
        self.assertEqual(isinstance(self.gx, tx.BaseExtractor), True)
        self.assertEqual(isinstance(self.gx, tg.GitExtractor), True)

    def test_raw(self):
        self.assertEqual(self.gx.raw(),self.raw_df)

if __name__ == '__main__':
    unittest.main()