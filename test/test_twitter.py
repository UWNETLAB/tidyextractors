# *********************************************************************************************
# Copyright (C) 2017 Joel Becker,  Jillian Anderson, Steve McColl and Dr. John McLevey
#
# This file is part of the tidyextractors package developed for Dr John McLevey's Networks Lab
# at the University of Waterloo. For more information, see
# http://tidyextractors.readthedocs.io/en/latest/
#
# tidyextractors is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# tidyextractors is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with tidyextractors.
# If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************************************

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
        check_df = self.tx.raw(drop_collections=False)
        expect_df = self.raw_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(expect_df['id']).issubset(set(check_df['id'])), True)

    def test_users(self):
        check_df = self.tx.users(drop_collections=False)
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