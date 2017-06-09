import tqdm
import warnings
import numpy as np
import pandas as pd
import itertools as it


class BaseExtractor(object):

    # _data stores the main collection of extracted test_data
    _data = None

    # A lookup of 'format':<generating function> pairs used by get_tidy
    _lookup = {}

    def __init__(self, source, *args, auto_extract=True, progress_bar=True, **kwargs):

        # Extract test_data unless otherwise specified
        if auto_extract:
            self._extract(source, *args, **kwargs)

        # Store progress bar preference
        self._progress_bool = progress_bar

        # Do subclass initialization
        self.__sub_init__(source, *args, **kwargs)

        # Check invariants
        self._check_invariants()

    def __sub_init__(self, source, *args, **kwargs):
        pass

    def __len__(self):
        return len(self._data)

    def _extract(self, source, *args, **kwargs):
        self._data = pd.DataFrame()

    def _check_invariants(self):
        # Invariant 1: Columns contain only one type
        for c in self._data.columns:
            if self._col_type(c) == type(None):
                type_set = self._col_type_set(c)
                raise TypeError('Column {} contains more than one type. '
                                'Types present are {}'.format(c,type_set))


    def _add_lookup(self, key, fn):
        self._lookup[key] = fn

    def _col_type(self, col):
        type_set = self._col_type_set(col)
        assert(len(type_set) == 1)
        return type_set.pop()

    def _col_type_set(self, col):
        type_set = set()
        if self._data[col].dtype == np.dtype(object):
            for i in range(1, len(self._data[col])):
                if self._data[col][i] == np.nan:
                    continue
                else:
                    type_set.add(type(self._data[col][i]))
            return type_set
        else:
            type_set.add(self._data[col].dtype)
            return type_set

    def _drop_collections(self, df):
        all_cols = df.columns
        keep_cols = []

        # Check whether each column contains collections.
        for c in all_cols:
            if self._col_type(c) not in [dict, list, set]:
                keep_cols.append(c)
        return df[keep_cols]

    def get_tidy(self, output, drop_collections = True, *args, **kwargs):

        # If the output is in _lookup call appropriate method.
        if output in self._lookup:
            if drop_collections:
                return self._drop_collections(self._lookup[output](*args, **kwargs))
            else:
                return self._lookup[output](*args, **kwargs)

        # Otherwise, warn the user and print appropriate options.
        else:
            warnings.warn('An invalid output format was entered.' +
                          ' Valid formats are: ' +
                          str(self._lookup.keys()))
            return None

    def raw(self):
        return self._data

    def expand_on(self, col1, col2, rename1 = None, rename2 = None, drop = [], drop_compound = False):

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
                                        index=index_tuples,
                                        columns=new_column_list)

        # An expanded test_data frame containing any test_data held in value:key collections in the expanded cols
        df_2 = pd.DataFrame.from_records(new_attr_df_dicts,
                                        index=index_tuples)

        # The final expanded test_data set
        df_out = pd.concat([df_1, df_2], axis=1)

        return df_out