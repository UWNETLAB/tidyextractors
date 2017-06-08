import tqdm
import warnings
import pandas as pd
import itertools as it
from tidyextractors.tidygit.get_log import extract_log
from tidyextractors import BaseExtractor


class GitExtractor(BaseExtractor):

    # TODO: Add doc strings.

    def __sub_init__(self, source, *args, **kwargs):

        # Populate lookup table:
        self.__add_lookup__('commits', self.commits)
        self.__add_lookup__('changes', self.changes)

        # Add lazy short form lookup table:
        self.__add_lookup__('cm', self.commits)
        self.__add_lookup__('ch', self.changes)

    def __extract__(self, source, *args, **kwargs):
        # Extract git data
        self.__data__ = extract_log(source)

        # Shorten hashes
        self.__data__['hexsha'] = self.__data__['hexsha'].apply(lambda s: s[:7])

    def commits(self):
        return self.__data__.set_index('hexsha')

    def changes(self):

        # How many rows expected in the output?
        count = len(self.__data__)

        # How often should the progress bar be updated?
        # update_interval = max(min(count//100, 100), 5)
        update_interval = 1
        # What are the column names?
        column_list = list(self.__data__.columns)

        # Commit hash index (for itertuples)
        try:
            hash_index = column_list.index('hexsha')
        except ValueError:
            warnings.warn('Could not find "hexsha" in columns.')
            raise

        # File records  index (for itertuples)
        try:
            files_index = column_list.index('changes')
        except ValueError:
            warnings.warn('Could not find "changes" in columns.')
            raise

        # New column names:
        new_columns = ['insertions','deletions','lines']
        new_column_list = column_list[:files_index] + ['file'] + column_list[files_index+1:] + new_columns

        # List of tuples. Rows in new data frame.
        row_tuples = []

        # MultiIndex tuples
        index_tuples = []

        # Create data for output.
        with tqdm.tqdm(total=count) as pbar:
            for row in self.__data__.itertuples(index=False):
                # Enumerate commit/file pairs
                for index in it.product([row[hash_index]],row[files_index]):
                    new_row = row[:files_index] + \
                              (index[1],) + \
                              row[files_index+1:] + \
                              tuple([row[files_index][index[1]][k] for k in new_columns])
                    row_tuples.append(new_row)
                    index_tuples.append((index[0][:7],index[1]))
                    pbar.update(update_interval)

        return pd.DataFrame.from_records(row_tuples, index=index_tuples, columns=new_column_list)
