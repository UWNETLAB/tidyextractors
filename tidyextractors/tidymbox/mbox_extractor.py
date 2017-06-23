import pandas as pd
from tidyextractors import BaseExtractor
from tidyextractors.tidymbox.mbox_to_pandas import mbox_to_pandas


class MboxExtractor(BaseExtractor):

    def _extract(self, source, *args, **kwargs):
        """
        Extracts data from mbox files. Mutates _data.

        :param source: A string specifying a path to one or more mbox files.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Extract data
        self._data = mbox_to_pandas(source)
        self._data['MessageID'] = pd.Series(range(0,len(self._data)))

    def emails(self, drop_collections = True):
        """
        Returns a table of mbox message data, with "messages" as rows/observations.
        :param bool drop_collections: Should columns with lists/dicts/sets be dropped?
        :return: pandas.DataFrame
        """
        base_df = self._data
        if drop_collections is True:
            out_df = self._drop_collections(base_df)
        else:
            out_df = base_df
        return out_df

    def sends(self):
        """
        Returns a table of mbox message data, with "sender/recipient" pairs as rows/observations.
        .. note::

            Rows may have a recipient from either "TO" or "CC". SendType column specifies this for each row.

        .. note::

            drop_collections is not available for this method, since there are no meaningful collections to keep.

        :return: pandas.DataFrame
        """
        # Expand on each "to" field
        on_to_df = self.expand_on('From', 'To', rename1='From', rename2='Recipient')
        on_cc_df = self.expand_on('From', 'Cc', rename1='From', rename2='Recipient')

        # Specify how it was sent
        on_to_df['SendType'] = 'To'
        on_cc_df['SendType'] = 'Cc'

        # Combine dataframes
        output_df = pd.concat([on_to_df, on_cc_df])

        return self._drop_collections(output_df)
