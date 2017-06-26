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
import unittest
import pandas as pd
import tidyextractors as tx
import tidyextractors.tidymbox as tm


class TestMboxExtractor(unittest.TestCase):

    def setUp(self):
        self.gx = tm.MboxExtractor(os.path.join('.', 'mbox_data'))
        self.sends_df = pd.read_csv(os.path.join('.', 'mbox_data', 'mbox_sends_test.csv'))
        self.emails_df = pd.read_csv(os.path.join('.', 'mbox_data', 'mbox_emails_test.csv'))
        self.raw_df = pd.read_csv(os.path.join('.', 'mbox_data', 'mbox_raw_test.csv'))

    def test_construction(self):
        self.assertEqual(isinstance(self.gx, tx.BaseExtractor), True)
        self.assertEqual(isinstance(self.gx, tm.MboxExtractor), True)

    def test_raw(self):
        check_df = self.gx.raw(drop_collections=False)
        expect_df = self.raw_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['MessageID']),set(expect_df['MessageID']))

    def test_emails(self):
        check_df = self.gx.emails(drop_collections=False)
        expect_df = self.emails_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['MessageID']),set(expect_df['MessageID']))

    def test_sends(self):
        check_df = self.gx.sends()
        expect_df = self.sends_df
        self.assertEqual(set(check_df.columns),set(expect_df.columns))
        self.assertEqual(set(check_df['MessageID']),set(expect_df['MessageID']))


if __name__ == '__main__':
    unittest.main()