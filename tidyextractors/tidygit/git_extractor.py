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

      return self.expand_on('hexsha','changes',rename1='hash',rename2='files')
