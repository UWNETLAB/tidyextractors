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

import re
import tqdm
import warnings
import petl as etl
import numpy as np
import pandas as pd
import itertools as it


class BaseExtractor(object):
    """
    BaseExtractor defines a basic interface, initialization routine, and data
    manipulation tools for extractor subclasses.
    """

    # _data stores the main collection of extracted test_data
    _data = None

    def __init__(self, source, auto_extract=True, *args, **kwargs):
        """
        Extractor initialization. Should not be overridden by extractor subclasses.

        :param source: Specifies data source. Differs by subclass.
        :param args: Arbitrary arguments permitted for extensibility.
        :param bool auto_extract: Extract data from source upon initialization?
        :param kwargs: Arbitrary keyword arguments permitted for extensibility.
        """

        # Extract test_data unless otherwise specified
        if auto_extract:
            self._extract(source, *args, **kwargs)

        # Do subclass initialization
        self.__sub_init__(source, *args, **kwargs)

    def __sub_init__(self, source, *args, **kwargs):
        """
        Subclass initialization routine. Used so that subclasses do not need to override ``BaseExtractor.__init__``.

        :param source: Specifies data source. Differs by subclass.
        :param args: Arbitrary arguments permitted for extensibility.
        :param kwargs: Arbitrary keyword arguments permitted for extensibility.
        :return: None
        """
        pass

    def __len__(self):
        """
        Length of self._data.

        :return: Integer
        """
        return len(self._data)

    def _extract(self, source, *args, **kwargs):
        """
        This method handles data extraction, and should be overridden by extractor subclasses.
         Default behaviour initializes an empty ``pandas.DataFrame``.

        :param source: Specifies data source. Differs by subclass.
        :param args: Arbitrary arguments permitted for extensibility.
        :param kwargs: Arbitrary keyword arguments permitted for extensibility.
        :return: None
        """
        self._data = pd.DataFrame()

    def _col_type_set(self, col, df):
        """
        Determines the set of types present in a DataFrame column.

        :param str col: A column name.
        :param pandas.DataFrame df: The dataset. Usually ``self._data``.
        :return: A set of Types.
        """
        type_set = set()
        if df[col].dtype == np.dtype(object):
            unindexed_col = list(df[col])
            for i in range(0, len(df[col])):
                if unindexed_col[i] == np.nan:
                    continue
                else:
                    type_set.add(type(unindexed_col[i]))
            return type_set
        else:
            type_set.add(df[col].dtype)
            return type_set

    def _drop_collections(self, df):
        """
        Drops columns containing collections (i.e. sets, dicts, lists) from a DataFrame.

        :param pandas.DataFrame df: Usually self._data.
        :return: pandas.DataFrame
        """
        all_cols = df.columns
        keep_cols = []

        # Check whether each column contains collections.
        for c in all_cols:
            if len(self._col_type_set(c, df).intersection([set, dict, list])) == 0:
                keep_cols.append(c)
        return df[keep_cols]

    def raw(self, drop_collections = False):
        """
        Produces the extractor object's data as it is stored internally.

        :param bool drop_collections: Defaults to False. Indicates whether columns with lists/dicts/sets will be dropped.

        :return: pandas.DataFrame
        """
        base_df = self._data
        if drop_collections is True:
            out_df = self._drop_collections(base_df)
        else:
            out_df = base_df
        return out_df

    def expand_on(self, col1, col2, rename1 = None, rename2 = None, drop = [], drop_collections = False):
        """
        Returns a reshaped version of extractor's data, where unique combinations of values from col1 and col2
        are given individual rows.

        Example function call from ``tidymbox``:

        .. code-block:: python

            self.expand_on('From', 'To', ['MessageID', 'Recipient'], rename1='From', rename2='Recipient')

        Columns to be expanded upon should be either atomic values or dictionaries of dictionaries. For example:

        Input Data:

        +-----------------+-------------------------------------------------------------------+
        | col1 (Atomic)   | col2 (Dict of Dict)                                               |
        +=================+===================================================================+
        | value1          | {valueA : {attr1: X1, attr2: Y1}, valueB: {attr1: X2, attr2: Y2}  |
        +-----------------+-------------------------------------------------------------------+
        | value2          | {valueC : {attr1: X3, attr2: Y3},  valueD: {attr1: X4, attr2: Y4} |
        +-----------------+-------------------------------------------------------------------+

        Output Data:

        +---------------+---------------+-------+-------+
        | col1_extended | col2_extended | attr1 | attr2 |
        +===============+===============+=======+=======+
        | value1        | valueA        | X1    | Y1    |
        +---------------+---------------+-------+-------+
        | value1        | valueB        | X2    | Y2    |
        +---------------+---------------+-------+-------+
        | value2        | valueA        | X3    | Y3    |
        +---------------+---------------+-------+-------+
        | value2        | valueB        | X4    | Y4    |
        +---------------+---------------+-------+-------+

        :param str col1: The first column to expand on. May be an atomic value, or a dict of dict.
        :param str col2: The second column to expand on. May be an atomic value, or a dict of dict.
        :param str rename1: The name for col1 after expansion. Defaults to col1_extended.
        :param str rename2: The name for col2 after expansion. Defaults to col2_extended.
        :param list drop: Column names to be dropped from output.
        :param bool drop_collections: Should columns with compound values be dropped?
        :return: pandas.DataFrame
        """

        # Assumption 1: Expanded columns are either atomic are built in collections
        # Assumption 2: New test_data columns added to rows from dicts in columns of collections.

        # How many rows expected in the output?
        count = len(self._data)

        # How often should the progress bar be updated?
        update_interval = max(min(count//100, 100), 5)

        # What are the column names?
        column_list = list(self._data.columns)

        # Determine column index (for itertuples)
        try:
            col1_index = column_list.index(col1)
        except ValueError:
            warnings.warn('Could not find "{}" in columns.'.format(col1))
            raise
        try:
            col2_index = column_list.index(col2)
        except ValueError:
            warnings.warn('Could not find "{}" in columns.'.format(col2))
            raise

        # Standardize the order of the specified columns
        first_index = min(col1_index, col2_index)
        second_index = max(col1_index, col2_index)
        first_name = column_list[first_index]
        second_name = column_list[second_index]
        first_rename = rename1 if first_index == col1_index else rename2
        second_rename = rename2 if first_index == col1_index else rename1

        # New column names:
        new_column_list = column_list[:first_index] + \
                          [first_name+'_extended' if first_rename is None else first_rename] + \
                          column_list[first_index+1:second_index] + \
                          [second_name+'_extended' if second_rename is None else second_rename] + \
                          column_list[second_index+1:]

        # Assert that there are no duplicates!
        if len(set(new_column_list)) != len(new_column_list):
            raise Exception('Duplicate columns names found. Note that you cannot rename a column with a name '
                            'that is already taken by another column.')

        # List of tuples. Rows in new test_data frame.
        old_attr_df_tuples = []
        new_attr_df_dicts = []

        # MultiIndex tuples
        index_tuples = []

        def iter_product(item1,item2):
            """
            Enumerates possible combinations of items from item1 and item 2. Allows atomic values.
            :param item1: Any
            :param item2: Any
            :return: A list of tuples.
            """
            if hasattr(item1, '__iter__') and type(item1) != str:
                iter1 = item1
            else:
                iter1 = [item1]
            if hasattr(item2, '__iter__') and type(item2) != str:
                iter2 = item2
            else:
                iter2 = [item2]
            return it.product(iter1,iter2)

        # Create test_data for output.
        with tqdm.tqdm(total=count) as pbar:
            for row in self._data.itertuples(index=False):
                # Enumerate commit/file pairs
                for index in iter_product(row[first_index],row[second_index]):

                    new_row = row[:first_index] + \
                              (index[0],) + \
                              row[first_index+1:second_index] + \
                              (index[1],) + \
                              row[second_index+1:]

                    # Add new row to list of row tuples
                    old_attr_df_tuples.append(new_row)

                    # Add key tuple to list of indices
                    index_tuples.append((index[0],index[1]))

                    # If there's test_data in either of the columns add the test_data to the new attr test_data frame.
                    temp_attrs = {}

                    # Get a copy of the first cell value for this index.
                    #  If it's a dict, get the appropriate entry.

                    temp_first = row[first_index]
                    if type(temp_first) == dict:
                        temp_first = temp_first[index[0]]
                    temp_second = row[second_index]
                    if type(temp_second) == dict:
                        temp_second = temp_second[index[1]]

                    # Get nested test_data for this index.
                    if type(temp_first) == dict:
                        for k in temp_first:
                            temp_attrs[first_name + '/' + k] = temp_first[k]
                    if type(temp_second) == dict:
                        for k in temp_second:
                            temp_attrs[second_name + '/' + k] = temp_second[k]

                    # Add to the "new test_data" records.
                    new_attr_df_dicts.append(temp_attrs)

                    # Update progress bar
                    pbar.update(update_interval)

        # An expanded test_data frame with only the columns of the original test_data frame
        df_1 = pd.DataFrame.from_records(old_attr_df_tuples,
                                        columns=new_column_list)

        # An expanded test_data frame containing any test_data held in value:key collections in the expanded cols
        df_2 = pd.DataFrame.from_records(new_attr_df_dicts)

        # The final expanded test_data set
        df_out = pd.concat([df_1, df_2], axis=1)

        # Set new index
        # index_cols has been depracated
        # df_out = df_out.set_index(index_cols)

        # Drop unwanted columns
        for col in drop:
            if col in df_out.columns:
                df_out = df_out.drop(col,1)

        if drop_collections is True:
            df_out = self._drop_collections(df_out)

        return df_out
