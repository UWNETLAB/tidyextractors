import tqdm
import warnings
import pandas as pd
import itertools as it
from tidyextractors.tidygit.get_log import extract_log
from tidyextractors import BaseExtractor


class GitExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):

        # Populate lookup table:
        self._add_lookup('commits', self.commits)
        self._add_lookup('changes', self.changes)

        # Add lazy short form lookup table:
        self._add_lookup('cm', self.commits)
        self._add_lookup('ch', self.changes)

    def _extract(self, source, *args, **kwargs):
        # Extract git data
        self._data = extract_log(source)

        # Shorten hashes
        self._data['hexsha'] = self._data['hexsha'].apply(lambda s: s[:7])

    def commits(self):
        return self._data.set_index('hexsha')

    def changes(self):
        return self.expand_on('hexsha', 'changes', rename1='hash', rename2='file')