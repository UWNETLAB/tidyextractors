import os
import json
import unittest
import pandas as pd
import tidyextractors as tx
import tidyextractors.tidytwitter as tm


class TestTwitterExtractor(unittest.TestCase):

    def setUp(self):

        # Get credentials
        with open(os.path.join('.','twitter_data','txrc')) as txrc:
            credentials = json.loads(txrc.read())

        # Normal setup
        self.tx = tm.TwitterExtractor(['whatifnumbers'], **credentials)
        self.tweets_df = pd.read_csv(os.path.join('.', 'twitter_data', 'twitter_tweets_test.csv'))
        self.users_df = pd.read_csv(os.path.join('.', 'twitter_data', 'twitter_users_test.csv'))
        self.raw_df = pd.read_csv(os.path.join('.', 'twitter_data', 'twitter_raw_test.csv'))

    def test_construction(self):
        self.assertEqual(isinstance(self.tx, tx.BaseExtractor), True)
        self.assertEqual(isinstance(self.tx, tm.TwitterExtractor), True)

    def test_raw(self):
        check_df = self.tx.raw()
        expect_df = self.raw_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(expect_df['id']).issubset(set(check_df['id'])), True)

    def test_users(self):
        check_df = self.tx.users()
        expect_df = self.users_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(expect_df['id']).issubset(set(check_df['id'])), True)

    def test_tweets(self):
        check_df = self.tx.tweets()
        expect_df = self.tweets_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(expect_df['id']).issubset(set(check_df['id'])), True)


if __name__ == '__main__':
    unittest.main()