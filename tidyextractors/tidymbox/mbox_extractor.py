import pandas as pd
from tidyextractors import BaseExtractor
from tidyextractors.tidymbox.mbox_to_pandas import mbox_to_pandas


class MboxExtractor(BaseExtractor):

    def __sub_init__(self, source, *args, **kwargs):
        """
        Subclass initialization routine which runs after BaseExtractor initialization.
        Mutates get_tidy lookup table.

        :param source: A string specifying a path to one or more mbox files.
        :param args: Arbitrary arguments for extensibility.
        :param kwargs: Arbitrary keyword arguments for extensibility.
        :return: None
        """
        # Populate lookup table:
        self._add_lookup('emails',self.emails)
        self._add_lookup('sends',self.sends)

        # Add lazy short form lookup table:
        self._add_lookup('e',self.emails)
        self._add_lookup('s',self.sends)

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

    def emails(self):
        """
        Returns a table of mbox message data, with "messages" as rows/observations.

        :return: pandas.DataFrame
        """
        return self._data.set_index(['MessageID'])

    def sends(self):
        """
        Returns a table of mbox message data, with "sender/recipient" pairs as rows/observations.
        NOTE: Rows may have a recipient from either "TO" or "CC". SendType column specifies this for each row.

        :return: pandas.DataFrame
        """
        # Expand on each "to" field
        on_to_df = self.expand_on('From', 'To', ['MessageID', 'Recipient'], rename1='From', rename2='Recipient')
        on_cc_df = self.expand_on('From', 'Cc', ['MessageID', 'Recipient'], rename1='From', rename2='Recipient')

        # Specify how it was sent
        on_to_df['SendType'] = 'To'
        on_cc_df['SendType'] = 'Cc'

        # Combine dataframes
        output_df = pd.concat([on_to_df, on_cc_df])

        return self._drop_collections(output_df)
