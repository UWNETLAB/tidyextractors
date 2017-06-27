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

from tidyextractors import BaseExtractor
from tidyextractors.tidygit.get_log import extract_log


class GitExtractor(BaseExtractor):
    """
    The ``GitExtractor`` class is for extracting data from local git repositories. This class
    has methods for outputting data into the ``changes`` and ``commits`` tidy formats, and a
    raw untidy format.

    :param str source: The path to a local git repository
    :param bool auto_extract: Defaults to True. If True, data is extracted automatically.
     Otherwise, extraction must be initiated through the internal interface.
    """
    def _extract(self, source, *args, **kwargs):
        """
        Extracts data from a local git repository. Mutates _data.
        :param str source: The path to a local git repository.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.

        :return: None
        """
        # Extract git test_data
        self._data = extract_log(source)

        # Shorten hashes
        self._data['hexsha'] = self._data['hexsha'].apply(lambda s: s[:7])

    def commits(self, drop_collections=True):
        """
        Returns a table of git log data, with "commits" as rows/observations.

        :param bool drop_collections: Defaults to True. Indicates whether columns with lists/dicts/sets will be dropped.

        :return: pandas.DataFrame
        """
        base_df = self._data
        if drop_collections is True:
            out_df = self._drop_collections(base_df)
        else:
            out_df = base_df
        return out_df

    def changes(self):
        """
        Returns a table of git log data, with "changes" as rows/observations.

        .. note::

            drop_collections is not available for this method, since there are no meaningful collections to keep.

        :return: pandas.DataFrame
        """
        return self.expand_on('hexsha', 'changes', rename1='hexsha', rename2='file')