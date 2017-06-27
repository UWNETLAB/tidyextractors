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

import pandas as pd
from tidyextractors import BaseExtractor
from tidyextractors.tidymbox.mbox_to_pandas import mbox_to_pandas


class MboxExtractor(BaseExtractor):
    """
    The ``MboxExtractor`` class is for extracting data from local Mbox files. This class
    has methods for outputting data into the ``emails`` and ``sends`` tidy formats, and a
    raw untidy format.

    :param str source: The path to either a single mbox file or a directory containing multiple mbox files.
    :param bool auto_extract: Defaults to True. If True, data is extracted automatically.
     Otherwise, extraction must be initiated through the internal interface.
    """

    def _extract(self, source, *args, **kwargs):
        """
        Extracts data from mbox files. Mutates _data.

        :param str source: The path to one or more mbox files.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Extract data
        self._data = mbox_to_pandas(source)
        self._data['MessageID'] = pd.Series(range(0,len(self._data)))

    def emails(self, drop_collections = True):
        """
        Returns a table of mbox message data, with "messages" as rows/observations.

        :param bool drop_collections: Defaults to True. Indicates whether columns with lists/dicts/sets will be dropped.

        :return: pandas.DataFrame
        """
        base_df = self._data
        if drop_collections is True:
            out_df = self._drop_collections(base_df)
        else:
            out_df = base_df
        return out_df

    def sends(self):
        """
        Returns a table of mbox message data, with "sender/recipient" pairs as rows/observations.

        .. note::

            Rows may have a recipient from either "TO" or "CC". SendType column specifies this for each row.

        .. note::

            drop_collections is not available for this method, since there are no meaningful collections to keep.

        :return: pandas.DataFrame
        """
        # Expand on each "to" field
        on_to_df = self.expand_on('From', 'To', rename1='From', rename2='Recipient')
        on_cc_df = self.expand_on('From', 'Cc', rename1='From', rename2='Recipient')

        # Specify how it was sent
        on_to_df['SendType'] = 'To'
        on_cc_df['SendType'] = 'Cc'

        # Combine dataframes
        output_df = pd.concat([on_to_df, on_cc_df])

        return self._drop_collections(output_df)
