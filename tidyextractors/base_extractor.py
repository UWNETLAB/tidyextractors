import tqdm
import warnings
import pandas as pd


class BaseExtractor(object):

    # TODO: Add doc strings

    def __init__(self, source, *args, auto_extract = True, **kwargs):

        # Extract data unless otherwise specified
        if auto_extract:
            self.__extract__(source, *args, **kwargs)

        # Populate lookup table
        self.__lookup__['identity'] = self.__identity__

        # Do subclass initialization
        self.__sub_init__(source, *args, **kwargs)

    def __sub_init__(self, source, *args, **kwargs):
        pass

    # Text to be printed while extracting from source.
    __extract_text__ = 'No extraction source for BaseExtractor.'

    def __extract__(self, source, *args, **kwargs):
        self.__data__ = pd.DataFrame()

    def get_data(self, output, *args, **kwargs):

        # If the output is in __lookup__ call appropriate method.
        if output in self.__lookup__:
            return self.__lookup__[output](*args, **kwargs)

        # Otherwise, warn the user and print appropriate options.
        else:
            warnings.warn('An invalid output format was entered. Valid formats are: ' + str(self.__lookup__.keys()))
            return None

    # __data__ stores the main collection of extracted data
    __data__ = None

    # A lookup of 'format':<generating function> pairs used by get_data
    __lookup__ = {}

    def __identity__(self):
        return self.__data__