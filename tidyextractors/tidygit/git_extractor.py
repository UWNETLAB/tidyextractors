import tqdm
import warnings
import gitlog
import pandas as pd
from tidyextractors import BaseExtractor


class GitExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):
        pass

    def __extract__(self, source, *args, **kwargs):
        self.__data__ = gitlog.extract_log(source)

    def __compound_commits__(self):
        return self.__data__.set_index('hexsha')

    def __flat_changes__(self):
        # Use iter tuples and rebuild the dataframe
        # Sum the "total files" column to know the length.
        pass

    def __flat_commits__(self):
        # This could be generalized to drop any columns containing compound data.
        return self.__data__.drop('changes').set_index('hexsha')