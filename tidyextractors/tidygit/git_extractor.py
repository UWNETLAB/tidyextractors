from tidyextractors import BaseExtractor
from tidyextractors.tidygit.get_log import extract_log


class GitExtractor(BaseExtractor):

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

    def commits(self, drop_collections=True):
        """
        Returns a table of git log data, with "commits" as rows/observations.

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