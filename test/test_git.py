import os
import unittest
import pandas as pd
import tidyextractors as tx
import tidyextractors.tidygit as tg


class TestGitExtractor(unittest.TestCase):

    def setUp(self):
        os.rename(os.path.join('.','new_git_data','git/'),os.path.join('.','new_git_data','.git/'))
        self.gx = tg.GitExtractor(os.path.join('.', 'new_git_data'))
        self.changes_df = pd.read_csv(os.path.join('.', 'new_git_data', 'git_changes_test.csv'))
        self.commits_df = pd.read_csv(os.path.join('.', 'new_git_data', 'git_commits_test.csv'))
        self.raw_df = pd.read_csv(os.path.join('.', 'new_git_data', 'git_raw_test.csv'))
        os.rename(os.path.join('.','new_git_data','.git/'),os.path.join('.','new_git_data','git/'))

    def test_construction(self):
        self.assertEqual(isinstance(self.gx, tx.BaseExtractor), True)
        self.assertEqual(isinstance(self.gx, tg.GitExtractor), True)

    def test_raw(self):
        check_df = self.gx.raw()
        expect_df = self.raw_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['hexsha']),set(expect_df['hexsha']))

    def test_commits(self):
        check_df = self.gx.commits()
        expect_df = self.commits_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['hexsha']),set(expect_df['hexsha']))

    def test_changes(self):
        check_df = self.gx.changes()
        expect_df = self.changes_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['hexsha']),set(expect_df['hexsha']))


if __name__ == '__main__':
    unittest.main()