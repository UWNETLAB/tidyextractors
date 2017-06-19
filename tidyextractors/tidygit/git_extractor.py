from tidyextractors import BaseExtractor
from tidyextractors.tidygit.get_log import extract_log


class GitExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):
        """
        Subclass initialization routine which runs after BaseExtractor initialization.
        Mutates get_tidy lookup table.
        :param source: A string specifying a path to a local git repository.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Populate lookup table:
        self._add_lookup('commits', self.commits)
        self._add_lookup('changes', self.changes)

        # Add lazy short form lookup table:
        self._add_lookup('cm', self.commits)
        self._add_lookup('ch', self.changes)

    def _extract(self, source, *args, **kwargs):
        """
        Extracts data from a local git repository. Mutates _data.
        :param source: A string specifying a path to a local git repository.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Extract git test_data
        self._data = extract_log(source)

        # Shorten hashes
        self._data['hexsha'] = self._data['hexsha'].apply(lambda s: s[:7])

    def commits(self):
        """
        Returns a table of git log data, with "commits" as rows/observations.

        :return: pandas.DataFrame
        """
        return self._data.set_index('hexsha')

    def changes(self):
        """
        Returns a table of git log data, with "changes" as rows/observations.

        :return: pandas.DataFrame
        """
        return self.expand_on('hexsha', 'changes', index_cols=['hash','file'], rename1='hash', rename2='file')