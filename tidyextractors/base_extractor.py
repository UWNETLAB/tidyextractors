import tqdm
import warnings
import pandas as pd
import itertools as it

class BaseExtractor(object):

    # TODO: Add doc strings

    def __init__(self, source, *args, auto_extract=True, progress_bar=True, **kwargs):

        # Extract data unless otherwise specified
        if auto_extract:
            self.__extract__(source, *args, **kwargs)

        # Store progress bar preference
        self.__progress_bool__ = progress_bar

        # Do subclass initialization
        self.__sub_init__(source, *args, **kwargs)

    def __sub_init__(self, source, *args, **kwargs):
        pass

    def __add_lookup__(self, key, fn):
        self.__lookup__[key] = fn

    def __extract__(self, source, *args, **kwargs):
        self.__data__ = pd.DataFrame()

    def get_tidy(self, output, *args, **kwargs):

        # If the output is in __lookup__ call appropriate method.
        if output in self.__lookup__:
            return self.__lookup__[output](*args, **kwargs)

        # Otherwise, warn the user and print appropriate options.
        else:
            warnings.warn('An invalid output format was entered.' +
                          ' Valid formats are: ' +
                          str(self.__lookup__.keys()))
            return None

    # __data__ stores the main collection of extracted data
    __data__ = None

    # A lookup of 'format':<generating function> pairs used by get_tidy
    __lookup__ = {}

    def raw(self):
        return self.__data__

    def __drop_compound__(self, df):
        all_cols = df.columns
        keep_cols = []
        for c in all_cols:
            if not hasattr(df[c].dtype, '__iter__'):
                keep_cols.extend(c)
        return df[keep_cols]

    def expand_on(self, col1, col2, rename1 = None, rename2 = None, drop = [], drop_compound = False):

        # Assumption 1: Expanded columns are either atomic or have __iter__
        # Assumption 2: New data columns added to rows from dicts in __iter__-able columns.

        # How many rows expected in the output?
        count = len(self.__data__)

        # How often should the progress bar be updated?
        # update_interval = max(min(count//100, 100), 5)
        update_interval = 1

        # What are the column names?
        column_list = list(self.__data__.columns)

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

        # New column names:
        new_column_list = column_list[:first_index] + \
                          [first_name+'_extended'] + \
                          column_list[first_index+1:second_index] + \
                          [second_name+'_extended'] + \
                          column_list[second_index+1:]

        # List of tuples. Rows in new data frame.
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

        # Create data for output.
        with tqdm.tqdm(total=count) as pbar:
            for row in self.__data__.itertuples(index=False):
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

                    # If there's data in either of the columns (i.e. it's a dict-like object
                    #  with a __getitem__ method) add the data to the new attr data frame.
                    temp_attrs = {}

                    # Get a copy of the first cell value for this index.
                    #  If it's a dict, get the appropriate entry.

                    temp_first = row[first_index]
                    if type(temp_first) == dict:
                        temp_first = temp_first[index[0]]
                    temp_second = row[second_index]
                    if type(temp_second) == dict:
                        temp_second = temp_second[index[1]]

                    # Get nested data for this index.
                    if type(temp_first) == dict:
                        for k in temp_first:
                            temp_attrs[k + '_' + first_name] = temp_first[k]
                    if type(temp_second) == dict:
                        for k in temp_second:
                            temp_attrs[k + '_' + second_name] = temp_second[k]

                    # Add to the "new data" records.
                    new_attr_df_dicts.append(temp_attrs)

                    # Update progress bar
                    pbar.update(update_interval)

        # An expanded data frame with only the columns of the original data frame
        df_1 = pd.DataFrame.from_records(old_attr_df_tuples,
                                        index=index_tuples,
                                        columns=new_column_list)

        # An expanded data frame containing any data held in value:key collections in the expanded cols
        df_2 = pd.DataFrame.from_records(new_attr_df_dicts,
                                        index=index_tuples)

        # The final expanded data set
        df_out = pd.concat([df_1, df_2], axis=1)

        return df_1, df_2, df_out